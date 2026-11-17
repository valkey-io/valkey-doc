---
title: "Valkey Large Object - Overview"
description: Valkey Large Object Module Overview
---

> **Note:** [valkey-large-object](https://github.com/valkey-io/valkey-large-object) is at version 0.x.
> Commands, arguments, replies, and configuration can change before version 1.0.

The [valkey-large-object](https://github.com/valkey-io/valkey-large-object) module (BSD-3-Clause) adds a data type and commands to store large binary values in Valkey.
Typical values are blocks of a machine learning KV cache, tensors, embeddings, and other blobs that are megabytes or larger in size.
The module keeps objects in DRAM, or in a tiered layout where NVMe holds each object and DRAM is a read cache.
Clients can transfer values over the normal Valkey connection (TCP), or over RDMA with [libfabric](https://ofiwg.github.io/libfabric/).
With RDMA, the server writes object bytes directly into client memory and reads them directly from client memory, for example with an Elastic Fabric Adapter (EFA) (see [Providers](large-object-rdma.md#providers)).

The module registers with the name `largeobj`.
Its value type is `largeob-k`.

## Key concepts

### Operating modes

The `largeobj.operating-mode` configuration selects one of two modes when the module loads.

* `Dram` (default) - All objects are in a DRAM pool.
  The pool is a set of pre-allocated segments.
  The mode does no disk I/O.
* `Tiered` - The module writes each object to a file on NVMe in `largeobj.disk-dir`.
  DRAM is a read cache.
  By default, the first read of an object promotes it into DRAM (see `largeobj.promote-min-hits` and `largeobj.max-promote-size`).
  When the cache is full, the module drops cached copies with the lowest LFU score.
  The module uses io_uring with `O_DIRECT` for disk I/O.

### Segments and maximum object size

The module allocates memory in fixed-size segments (`largeobj.segment-size`, from 1MB to 1GB).
In `Dram` mode, an object must fit in a single segment.
Thus an object of `largeobj.max-object-size` bytes, plus a small overhead for each chunk, must fit in one segment, and the largest object in `Dram` mode is less than 1GB.
The module also divides objects into chunks (`largeobj.chunk-size`) for streaming I/O.
Each chunk adds a small allocation overhead in the segment.
Each pool has at most 16384 segments, so the DRAM pool does not grow past 16384 x `largeobj.segment-size` (1TB with 64MB segments), also when `maxmemory` is larger.

The default `largeobj.max-object-size` is 512MB.
The smallest object is 1 byte.
See [Cross-configuration rules](large-object-configuration.md#cross-configuration-rules) for the rules that relate these values.

### Transports

* TCP - [`BLOB.TCP_SET`](../commands/blob.tcp_set.md) and [`BLOB.TCP_GET`](../commands/blob.tcp_get.md) send the value in the RESP command and reply.
  These commands are always available and work with any Valkey client.
* RDMA - [`BLOB.RDMA_SET`](../commands/blob.rdma_set.md) and [`BLOB.RDMA_GET`](../commands/blob.rdma_get.md) send only the key and a list of client memory regions.
  The server reads or writes the value bytes with libfabric.
  The client must first open a session with [`BLOB.RDMA_HELLO`](../commands/blob.rdma_hello.md).

If the fabric does not start, the module still loads, and only the TCP commands are available.
See [Valkey Large Object - RDMA Transfers](large-object-rdma.md) for the full RDMA model.

### CRC32C checksum

The server calculates a CRC32C (Castagnoli) checksum of each object when it stores the object.
[`BLOB.INFO`](../commands/blob.info.md) and [`BLOB.RDMA_GET`](../commands/blob.rdma_get.md) return this value.
On [`BLOB.RDMA_SET`](../commands/blob.rdma_set.md), a client can send its own CRC32C value.
The server then rejects the write if the checksum of the transferred bytes is different.

## Supported commands

* [`BLOB.TCP_SET`](../commands/blob.tcp_set.md) - stores an object that is sent in the command.
* [`BLOB.TCP_GET`](../commands/blob.tcp_get.md) - returns an object as a bulk string.
* [`BLOB.RDMA_HELLO`](../commands/blob.rdma_hello.md) - opens an RDMA session on the connection.
* [`BLOB.RDMA_SET`](../commands/blob.rdma_set.md) - stores an object that the server reads from client memory.
* [`BLOB.RDMA_GET`](../commands/blob.rdma_get.md) - writes an object into client memory.
* [`BLOB.INFO`](../commands/blob.info.md) - returns the length, CRC32C, and storage tier of an object.

See the [complete list of large object commands](../commands/#large-object).

Core commands also operate on large object keys.
`DEL`, `UNLINK`, overwrite, expiry, and eviction free the object storage in the background.
See [Core commands on large object keys](#core-commands-on-large-object-keys).
`MEMORY USAGE` counts the payload only when the payload is in DRAM.

When `notify-keyspace-events` includes module key type events (`d`), the module sends `largeobj.create` when a write creates a key and `largeobj.update` when a write replaces a value.

## Limitations

The current version has these limitations:

* No persistence.
  The module does not save object data to RDB or AOF.
  Objects do not survive a server restart.
  In `Tiered` mode, the module deletes `largeobj.disk-dir` at startup and shutdown (see [Disk directory](large-object-configuration.md#disk-directory)).
  See [Persistence behavior](#persistence-behavior).
* No replication.
  Replicas are not supported for large object data.
  See [Replication](#replication).
* In cluster mode, slots that have large object keys cannot move.
  See [Cluster mode](#cluster-mode).
* `BLOB.TCP_SET`, `BLOB.TCP_GET`, `BLOB.RDMA_SET`, and `BLOB.RDMA_GET` are blocking commands, so they cannot run in transactions, scripts, functions, or module calls.
* The module cannot be unloaded with `MODULE UNLOAD`.
  Restart the server to remove it.
  To stop users from using the module without a restart, use ACLs, for example `ACL SETUSER <user> -@largeobj` (see [ACL](large-object-configuration.md#acl)).
* Active defragmentation is not implemented for large object memory.
* RDMA transfers have no server-side timeout other than a 1-second limit to post a transfer (see [Cancel and timeout](large-object-rdma.md#cancel-and-timeout)).

### Persistence behavior

These operations work while large object keys exist, but they do not keep the object data:

* `SAVE`, `BGSAVE`, `SHUTDOWN` with save points, and the automatic RDB snapshots save the key names without the object data.
* `BGREWRITEAOF` keeps no object data.
  With `aof-use-rdb-preamble yes` (the default), the rewritten AOF has the key names, as with `SAVE`.
  With `aof-use-rdb-preamble no`, it has no large object keys.
* When the server loads an RDB file (at startup, with `DEBUG RELOAD`, or on a replica full synchronization), each large object key reads as missing.
  The module starts to delete these keys within `largeobj.scaling-poll-ms` (default 2.5 seconds) after the load.
  With many keys, this can take longer.
  Until then, `EXISTS` and `DBSIZE` still count them.
  For example, `EXISTS` still returns `1` directly after a `BLOB.TCP_GET` of the key returns nil, and returns `0` a few seconds later.
* `DUMP` returns a value without the object data.
  `RESTORE` of that value fails with `ERR Bad data format`, so `MIGRATE` fails (see [Cluster mode](#cluster-mode)).

The server log shows a warning, for example `largeobj: persistence is not supported: blobs are saved to RDB/DUMP without their data`, the first time that each case occurs.

### Replication

The module does not replicate large objects:

* A large object write on the primary is not sent to the replica.
  The replica does not have the key.
* At a full synchronization, the replica loads the large object keys without their data.
  They read as missing, and the replica deletes them a few seconds later, as after an RDB load.
* In that time, a `COPY` from the primary of such a key fails on the replica.
  The replica log then shows `This replica is sending an error to its primary: 'module key failed to copy'`.
* If a replica becomes the primary, it has no large objects.

### Cluster mode

The module loads on each node of a cluster.
Each command uses a single key (or no key for `BLOB.RDMA_HELLO`), so cluster clients can route commands by slot.

* An RDMA session belongs to one connection to one node.
  Send `BLOB.RDMA_HELLO` on each connection to each node, and add the server addresses of each node to the address vector.
  Each node replies with its own server addresses.
* You cannot move a slot that has large object keys.
  `MIGRATE` uses `DUMP` and `RESTORE`, which do not keep object data.
  The key stays on the source node:

  ```
  127.0.0.1:7395> MIGRATE 127.0.0.1 7394 foo 0 5000
  (error) ERR Target instance replied with error: ERR Bad data format
  ```

  Atomic slot migration (`CLUSTER MIGRATESLOTS`) is refused with `ERR The module largeobj does not support atomic slot migrations. Please ensure all modules have declared support for atomic slot migration and try again`.
* To add capacity, raise `maxmemory` (`Dram` mode) or `largeobj.disk-maxmemory` (`Tiered` mode) on the nodes, if the hosts have the memory or disk.
  Both are mutable with `CONFIG SET`.
  Else move a slot to a new node only when the slot has no large object keys: delete the large object keys in the slot first (or let them expire), move the slot, and then write the objects again.
  Or make a new, larger cluster and write the objects to it.
* After a `MOVED` or `ASK` redirect, the client sends the command on a connection to the other node.
  If that connection has no RDMA session, `BLOB.RDMA_SET` and `BLOB.RDMA_GET` fail with `ERR no RDMA session (call BLOB.RDMA_HELLO first)`.
  Send `BLOB.RDMA_HELLO` on that connection first.

### Core commands on large object keys

These results are the same in `Dram` and `Tiered` mode.

| Command | Result |
|:--------|:-------|
| `COPY` | Works. The copy has its own data. |
| `RENAME`, `RENAMENX` | Work. |
| `MOVE`, `SWAPDB` | Work. |
| `EXPIRE`, `PEXPIRE`, `TTL`, `PERSIST` | Work. |
| `TYPE` | Returns `largeob-k`. |
| `OBJECT ENCODING` | Returns `raw`. |
| `DUMP` | Returns a value without the object data. |
| `RESTORE` | Fails with `ERR Bad data format`. |
| `DEL`, `UNLINK` | Work. The module frees the storage in the background. |
| `FLUSHALL`, `FLUSHALL ASYNC` | Work. |

## Topics

* [Valkey Large Object - Getting Started](large-object-getting-started.md) - build the module, load it, and run your first commands.
* [Valkey Large Object - Use Cases and Examples](large-object-use-cases.md) - common patterns with worked examples.
* [Valkey Large Object - RDMA Transfers](large-object-rdma.md) - sessions, memory regions, checksums, and errors.
* [Valkey Large Object - Configuration and Monitoring](large-object-configuration.md) - configuration parameters, ACL, and `INFO` fields.

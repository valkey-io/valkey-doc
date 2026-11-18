---
title: "Valkey Large Object - Configuration and Monitoring"
description: Configuration parameters, ACL category, and INFO fields of the Valkey Large Object module
---

> **Note:** [valkey-large-object](https://github.com/valkey-io/valkey-large-object) is at version 0.x.
> Commands, arguments, replies, and configuration can change before version 1.0.

## Set configurations

The configuration names have the `largeobj.` prefix, for example `largeobj.segment-size`.
Set the configurations when the module loads, with the full names.
Memory sizes can have units, such as `64mb` and `1gb`.

In `valkey.conf`, put each configuration on its own line:

```
loadmodule /path/to/libvalkey_large_object.so
largeobj.operating-mode Dram
largeobj.segment-size 64mb
largeobj.max-object-size 32mb
```

On the command line:

```bash
valkey-server --loadmodule /path/to/libvalkey_large_object.so \
  --largeobj.operating-mode Dram \
  --largeobj.segment-size 64mb \
  --largeobj.max-object-size 32mb
```

With [`MODULE LOADEX`](../commands/module-loadex.md):

```
MODULE LOADEX /path/to/libvalkey_large_object.so CONFIG largeobj.operating-mode Dram CONFIG largeobj.segment-size 64mb CONFIG largeobj.max-object-size 32mb
```

The configurations with `No` in the Mutable column can be set only when the module loads.
A lower `largeobj.max-object-size` does not change objects that are already stored.

## Disk directory

> **Warning:** In `Tiered` mode, the module deletes the `largeobj.disk-dir` directory and all its contents at startup and at shutdown, then creates it again, empty.
> Set `largeobj.disk-dir` to a new, empty directory that only this module uses, below the mount point (for example `/mnt/nvme/largeobj`).
> Never use a directory that has other data, or a mount point.

## Configuration parameters

This table shows the configurations that you are most likely to set.
For the full list, see the [module repository](https://github.com/valkey-io/valkey-large-object).

| Name | Type | Default | Range | Mutable | Description |
|:-----|:-----|:--------|:------|:--------|:------------|
| `largeobj.operating-mode` | enum | `Dram` | `Dram`, `Tiered` | No | `Dram`: objects are in DRAM only. `Tiered`: objects are on NVMe and DRAM is a read cache. |
| `largeobj.disk-dir` | string | `""` | - | No | Directory for object files. Necessary in `Tiered` mode. Must be on XFS, the only supported file system, with `O_DIRECT` and user extended attributes, and a writable parent. **Deleted at startup and shutdown: see [Disk directory](#disk-directory).** |
| `largeobj.disk-dir-shards` | integer | `1024` | 1 to 65536 | No | `Tiered`: number of subdirectories of `largeobj.disk-dir` for the object files. More subdirectories let file creates and deletes run in parallel. |
| `largeobj.segment-size` | memory | `1gb` | 1mb to 1gb | No | Size of each DRAM pool segment and disk staging segment. Must be at least two times `largeobj.chunk-size`. The pool grows in segments; in `Tiered` mode it also shrinks. Each pool has at most 16384 segments: the DRAM pool stops at 16384 x `largeobj.segment-size`, and `largeobj.disk-staging-size` / `largeobj.segment-size` must not be more than 16384. |
| `largeobj.disk-staging-size` | memory | `1gb` | 1mb to 2^63-1 | No | `Tiered`: total size of the DRAM staging buffers for disk I/O. |
| `largeobj.disk-maxmemory` | memory | `0` | 0 to 2^63-1 | Yes | Maximum disk use in `largeobj.disk-dir`. Each file counts as its length rounded up to 4KB, or, on a striped XFS, to the stripe unit for files of at least one stripe unit. On XFS, each file also counts its inode. A file also counts the metadata blocks that it uses outside its inode (see `disk_metadata_spills`). `0` is unlimited. |
| `largeobj.max-object-size` | memory | `512mb` | 1 to 2^63-1 | Yes | Maximum object size for `BLOB.TCP_SET` and `BLOB.RDMA_SET`. `BLOB.TCP_SET` is also limited by the core `proto-max-bulk-len` (default 512MB). |
| `largeobj.max-promote-size` | memory | `256mb` | 0 to 2^63-1 | Yes | `Tiered`: maximum size of an object that is promoted from disk to DRAM. `0` disables promotion. |
| `largeobj.chunk-size` | memory | `1mb` | 4096 to 256mb | No | Chunk size for streaming I/O. Must be a multiple of 4096. |
| `largeobj.max-buffers-per-op` | integer | `64` | 2 to 1024 | Yes | Maximum number of `largeobj.chunk-size` buffers that one streaming operation holds. In `Tiered` mode, a lower value lets more disk operations share the disk staging buffers. |
| `largeobj.min-buffers-per-op` | integer | `2` | 1 to 1024 | Yes | `Tiered`: minimum number of `largeobj.chunk-size` buffers that a disk operation must get to start. If fewer buffers are free, the operation fails with `ERR disk staging buffer pool exhausted; retry later`. Must not be more than `largeobj.max-buffers-per-op`. |
| `largeobj.worker-threads` | integer | `8` | 1 to 32 | No | Number of worker threads for asynchronous I/O. |
| `largeobj.scaling-shrink-watermark` | integer (%) | `90` | 50 to 95 | Yes | Server `used_memory` / `maxmemory`, in percent, above which the DRAM pool does not expand. In `Tiered` mode, the pool also releases segments above this value (the objects stay on disk). |
| `largeobj.promote-min-hits` | integer | `1` | 1 to 255 | Yes | `Tiered`: number of disk reads of an object; the read that reaches this number promotes the object to DRAM. `1` promotes on the first read. |
| `largeobj.fabric-provider` | enum | `EfaDirect` | `EfaDirect`, `Emulated` | No | libfabric provider for RDMA. `EfaDirect`: EFA hardware (see [Providers](large-object-rdma.md#providers)). `Emulated`: libfabric over TCP sockets, for development and tests only. |
| `largeobj.fabric-interfaces` | string | `""` | - | No | Comma-separated list of fabric domains to use. Empty uses all domains that the provider finds. |
| `largeobj.fabric-crc-pool-threads` | integer | `2` | 1 to 1024 | No | Number of threads that calculate checksums for `BLOB.RDMA_SET` transfers. |
| `largeobj.max-rdma-registered-bytes` | memory | `380gb` | 0 to 2^63-1 | Yes | Maximum bytes of DRAM pool and disk staging segments that are registered with the fabric. The pool does not expand above this value. `0` is unlimited. No effect when the fabric is not available. |
| `largeobj.enabled` | bool | `yes` | `yes`, `no` | Yes | `no` rejects all large object commands with `DISABLED largeobj module is disabled`. Stored keys stay, and core commands such as `DEL` still work on them. |

## Cross-configuration rules

The module checks these rules when it loads.
It checks them again when `CONFIG SET` changes `largeobj.disk-maxmemory`, `largeobj.max-object-size`, `largeobj.max-promote-size`, `largeobj.max-buffers-per-op`, or `largeobj.min-buffers-per-op`.
If a rule is not satisfied, the module does not load, or `CONFIG SET` fails with the error in the table.

| Rule | Mode | Error |
|:-----|:-----|:------|
| `largeobj.disk-maxmemory` is `0` or equal to or larger than `largeobj.max-object-size` | `Tiered` | `ERR largeobj.disk-maxmemory must be >= largeobj.max-object-size in Tiered mode` |
| `largeobj.disk-staging-size` is equal to or larger than `largeobj.segment-size` | `Tiered` | `ERR largeobj.disk-staging-size must be >= largeobj.segment-size` |
| `largeobj.segment-size` is equal to or larger than two times `largeobj.chunk-size` | All | `ERR largeobj.segment-size must be >= 2 * largeobj.chunk-size` |
| `largeobj.chunk-size` is a multiple of 4096 | All | `ERR largeobj.chunk-size must be a multiple of 4096` |
| `largeobj.max-buffers-per-op` is equal to or larger than `largeobj.min-buffers-per-op` | All | `ERR largeobj.max-buffers-per-op must be >= largeobj.min-buffers-per-op` |
| An object of `largeobj.max-object-size` fits in one segment | `Dram` | `ERR largeobj.segment-size is insufficient for largeobj.max-object-size` |
| An object of `largeobj.max-promote-size` fits in one segment | `Tiered` | `ERR largeobj.segment-size is insufficient for largeobj.max-promote-size` |

An object "fits in one segment" when its chunks, plus 4KB of overhead for each chunk, plus 4KB, are not larger than `largeobj.segment-size`.
Thus `largeobj.max-object-size` must be a little smaller than `largeobj.segment-size` in `Dram` mode.
For example, with 64MB segments and the default `largeobj.chunk-size`, the largest `largeobj.max-object-size` is 66842624 bytes (`largeobj.segment-size` minus 260KB).
In `Tiered` mode, `largeobj.max-promote-size` (default 256MB) must fit in one segment, with the same overhead as `largeobj.max-object-size` (with 64MB segments, at most 66842624).
The default values (`largeobj.segment-size` `1gb`, `largeobj.max-object-size` `512mb`, `largeobj.chunk-size` `1mb`) satisfy all rules.

## Memory and eviction

The DRAM limit is the core Valkey `maxmemory` setting, together with `largeobj.scaling-shrink-watermark`.
When the fabric is available, `largeobj.max-rdma-registered-bytes` also limits the DRAM pool.
The maximum number of segments also limits the DRAM pool (see `largeobj.segment-size` in [Configuration parameters](#configuration-parameters)).

A write can evict other large objects to make space.
The core `maxmemory-policy` setting controls which objects the module can evict:

* `allkeys-*` policies - any large object.
* `volatile-*` policies - only large object keys that have a TTL.
* `noeviction` - no object.
  The write fails with an `OOM` error.

The module evicts in least recently used (LRU) order for all policies.
A read and a TTL change count as a use.
For the `*-lfu`, `*-random`, and `volatile-ttl` policies, the module also uses LRU order, and the server log shows a warning.

* `Dram` mode - Eviction occurs only when `maxmemory` is set.
* `Tiered` mode - Eviction removes object files when `largeobj.disk-maxmemory` is larger than `0`.
  `maxmemory` is not necessary for disk eviction.
  When the DRAM cache is full, the module drops cached copies with the lowest LFU score (demotion).
  The objects stay on disk.

An evicted key stays in the keyspace until the module deletes it, within a few milliseconds when the backlog is small.
Until then, a read returns nil, but `EXISTS` and `DBSIZE` still count the key.
`pending_evictions` shows how many evicted keys wait to be deleted.

## ACL

The module adds the ACL category `@largeobj`.
All large object commands are in this category, and no other commands are.

| Command | @largeobj | @read | @write | @connection | @fast |
|:--------|:----------|:------|:-------|:------------|:------|
| `BLOB.TCP_SET` | y | | y | | y |
| `BLOB.TCP_GET` | y | y | | | y |
| `BLOB.RDMA_HELLO` | y | | | y | y |
| `BLOB.RDMA_SET` | y | | y | | y |
| `BLOB.RDMA_GET` | y | y | | | y |
| `BLOB.INFO` | y | y | | | y |

For example, this user can use all large object commands on keys that start with `kv:`:

```
127.0.0.1:6379> ACL SETUSER cache-client on >password +@largeobj ~kv:*
OK
```

`DEL` and `UNLINK` are not in `@largeobj`, so a user that must delete large object keys also needs these commands, for example `+@largeobj +del +unlink`.

To stop a user from using the module, remove the category from the user, for example `ACL SETUSER <user> -@largeobj`.

## Security

* The TCP commands carry the object data on the normal Valkey connection.
  If you use Valkey TLS, TLS also protects this data.
* The RDMA commands carry only the command, the key, the client memory regions, and the reply on the Valkey connection.
  The object data moves directly between client memory and server memory over the fabric, not through the Valkey connection.
  Valkey TLS does not protect this data, and the module does not encrypt it.
* In `Tiered` mode, the module does not encrypt the object files in `largeobj.disk-dir`.
  If you need encryption at rest, use file system or disk encryption.
* For an RDMA transfer, the server reads or writes only the client memory regions that the command names, at the client endpoint of the session of that connection.
* The server registers its own memory for local access only.
  A client cannot read or write server memory directly; the server starts every transfer.

## What to watch

The field names in this table are without the `largeobj_` prefix (see [INFO fields](#info-fields)).

| Field | What it tells you | Action |
|:------|:------------------|:-------|
| `evictions` | Large object keys evicted to make space. | If it grows fast, add memory or disk, or store fewer objects. |
| `pending_evictions` | Evicted keys that the module did not delete yet. | If it stays high, the module cannot delete keys as fast as it evicts them. |
| `dram_pool_exhausted`, `disk_capacity_exceeded` | Writes that the module failed with `OOM`. A write that core Valkey rejects with `OOM` before the module runs is not counted. | Raise `maxmemory` or `largeobj.disk-maxmemory`, or use a `maxmemory-policy` that permits eviction. |
| `disk_staging_buffer_exhausted` | `Tiered` disk operations that failed because of too much concurrency. | Raise `largeobj.disk-staging-size`, lower `largeobj.max-buffers-per-op`, or send fewer concurrent operations. |
| `disk_write_errors`, `disk_read_errors` | Failed disk I/O. | Look at the server log and the disk health. |
| `rdma_read_errors`, `rdma_write_errors`, `crc_mismatch` | Failed RDMA transfers. | Look at the client: registered regions, endpoint, and checksum. |

The core `evicted_keys` field in `INFO stats` does not count large objects that the module evicts.
The module deletes the evicted keys itself (with an unlink), not through core eviction.
Use `evictions` in `INFO largeobj` instead.

## INFO fields

Use `INFO largeobj` to see the module metrics.
When `largeobj.enabled` is `no` and no large objects are stored, `INFO largeobj` returns no sections.
Valkey adds the `largeobj_` prefix to each section name and field name, for example section `largeobj_core_metrics` and field `largeobj_num_objects`.
The tables below show the names without the prefix.
They show only the most important fields.
For the full list, see the [module repository](https://github.com/valkey-io/valkey-large-object).

### `core_metrics`

| Field | Description |
|:------|:------------|
| `num_objects` | Number of large objects. |
| `inflight_requests` | Number of large object commands that are in progress. |

### `evictions`

| Field | Description |
|:------|:------------|
| `evictions` | Number of objects evicted to make space for a write. `Tiered` cache drops are demotions and are not counted. |
| `pending_evictions` | Number of evicted keys that the module did not finish deleting. These keys read as missing. |

### `dram`

| Field | Description |
|:------|:------------|
| `dram_segments` | Number of DRAM pool segments. |
| `dram_allocated_bytes` | Bytes allocated in the DRAM pool. |
| `dram_capacity_bytes` | Pool capacity: (segments minus draining segments) multiplied by the segment size. |
| `dram_utilization_pct` | DRAM pool use in percent. |
| `dram_objects` | Number of objects in DRAM. |
| `cache_hits` | `Tiered` only: reads served from the DRAM cache. |
| `cache_misses` | `Tiered` only: reads served from disk. |
| `cache_promotions` | `Tiered` only: objects promoted to the DRAM cache. |
| `cache_demotions` | `Tiered` only: cached copies dropped from DRAM. |
| `dram_rdma_registered_segments` | DRAM pool segments registered with the fabric. `0` when the fabric is not available. |

### `disk`

This section is only in `Tiered` mode.

| Field | Description |
|:------|:------------|
| `disk_used_bytes` | Bytes used in `largeobj.disk-dir`, counted as for `largeobj.disk-maxmemory`. |
| `disk_utilization_pct` | `disk_used_bytes` as a percent of `largeobj.disk-maxmemory`. `0.00` when `largeobj.disk-maxmemory` is `0`. |
| `disk_metadata_spills` | Number of object files that use disk blocks outside their inode, in addition to their data. For example, a file that has more extents than its inode can list uses one more block. These blocks count in `disk_used_bytes`. |

### `rdma`

| Field | Description |
|:------|:------------|
| `rdma_sessions` | Number of open RDMA sessions. |
| `rdma_read_bytes` | Bytes that the server read from client memory (`BLOB.RDMA_SET`). |
| `rdma_write_bytes` | Bytes that the server wrote into client memory (`BLOB.RDMA_GET`). |

### `error_metrics`

| Field | Description |
|:------|:------------|
| `disk_read_errors` | Failed disk reads. |
| `disk_write_errors` | Failed disk writes. |
| `rdma_read_errors` | Failed RDMA reads from client memory. |
| `rdma_write_errors` | Failed RDMA writes into client memory. |
| `dram_pool_exhausted` | Writes that could not get DRAM pool memory. |
| `disk_staging_buffer_exhausted` | `Tiered` disk reads and writes that failed with `ERR disk staging buffer pool exhausted; retry later`, because too many disk operations ran at the same time for the disk staging buffers. |
| `disk_capacity_exceeded` | Writes that failed because of `largeobj.disk-maxmemory`. |
| `crc_mismatch` | `BLOB.RDMA_SET` writes rejected because the `CRC` value did not agree. |

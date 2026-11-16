---
title: "Valkey Large Object - RDMA Transfers"
description: How RDMA transfers work in the Valkey Large Object module
---

> **Note:** [valkey-large-object](https://github.com/valkey-io/valkey-large-object) is at version 0.x.
> Commands, arguments, replies, and configuration can change before version 1.0.

The RDMA commands move object bytes between the server and client memory with [libfabric](https://ofiwg.github.io/libfabric/).
The value bytes do not go through the Valkey connection.
The Valkey connection carries only the command, the key, a list of memory regions, and a short reply.

## Comparison with Valkey RDMA connections

Valkey also has its own [RDMA support](RDMA.md), which is a connection type for the full RESP protocol.
The two features are different and independent.

| | Valkey RDMA connection | Large object RDMA commands |
|:--|:--|:--|
| What RDMA carries | All commands and replies, in place of TCP | Only the object payload of `BLOB.RDMA_SET` and `BLOB.RDMA_GET` |
| Commands and replies | Over RDMA | Over the normal Valkey connection, usually TCP |
| How to turn it on | Load `valkey-rdma.so` with `bind` and `port` (see [RDMA support](RDMA.md)) | Load the module and set `largeobj.fabric-provider` |
| RDMA interface | RDMA verbs with reliable connection (RC) queue pairs | libfabric, with the `EfaDirect` or `Emulated` provider |
| Data movement | Each side writes the RESP byte stream into a receive buffer of the other side | The server does one-sided RDMA reads and writes between registered client memory and its DRAM segments |
| Session setup | RDMA connection setup and feature negotiation | `BLOB.RDMA_HELLO` one time on each Valkey connection |
| Payload checksum | Not part of the protocol | CRC32C of each object |
| Status | Experimental | Version 0.x; can change before version 1.0 |

The module does not use the Valkey RDMA connection type.
The large object commands are not supported on a Valkey RDMA connection.

## Roles

The server is the RDMA initiator, and the client is passive during the transfer.

* For [`BLOB.RDMA_GET`](../commands/blob.rdma_get.md), the server does RDMA writes (`fi_write`) into client memory.
* For [`BLOB.RDMA_SET`](../commands/blob.rdma_set.md), the server does RDMA reads (`fi_read`) from client memory.

The client memory is memory that the client registers with its libfabric domain, usually host memory.
Client device memory, for example GPU memory (`FI_HMEM`), is not supported.

Client requirements:

* The libfabric provider of the client must support RMA (`FI_RMA`) with remote read and remote write, because the server reads from and writes into client memory.
* The client registers its buffers with `fi_mr_reg`, which counts against the locked-memory limit (`RLIMIT_MEMLOCK`) of the client process.
  Set the client limit to at least the total size of its registered buffers, or to `unlimited`.

The server registers only host memory.
When the module loads, it sets the libfabric environment variable `FI_HMEM` to `system`, unless `FI_HMEM` is already set.
Thus libfabric on the server does not start device memory interfaces, for example CUDA on a GPU host.

## Session model

An RDMA session belongs to one Valkey connection.
In cluster mode, a client that follows a `MOVED` or `ASK` redirect to another node must send `BLOB.RDMA_HELLO` on that connection first.
Else `BLOB.RDMA_SET` and `BLOB.RDMA_GET` fail with `ERR no RDMA session (call BLOB.RDMA_HELLO first)`.

1. The client opens a libfabric endpoint and gets its endpoint address with `fi_getname`.
2. The client registers each buffer that it will use with `fi_mr_reg`.
   Each registration gives a remote key (`rkey`).
3. The client sends [`BLOB.RDMA_HELLO`](../commands/blob.rdma_hello.md) with its endpoint address as a hexadecimal string, one time on the connection.
4. The server adds the client address to the address vector of each of its fabric services.
   The reply is an array with one hexadecimal server address for each fabric service.
5. The client adds every returned server address to its own address vector with `fi_av_insert`.
6. The client sends `BLOB.RDMA_SET` and `BLOB.RDMA_GET` commands on the same connection.
7. The session ends when the connection closes.

The session keeps only the address routing information.
It does not keep memory regions or remote keys.
The client sends the regions in each command, so it can use a different buffer for each request.

A second `BLOB.RDMA_HELLO` on the same connection fails with `ERR RDMA session already established`.
To start a new session, open a new connection.

The server does not check the session for a missing key.
Thus `BLOB.RDMA_GET` on a missing key returns nil also when the connection has no session.

## HELLO handshake

```
BLOB.RDMA_HELLO client-rdma-address
```

* When `largeobj.fabric-provider` is `EfaDirect`, the decoded address must be exactly 32 bytes.
* When `largeobj.fabric-provider` is `Emulated`, the decoded address must be a socket address: 16 bytes for IPv4 (`sockaddr_in`) or 28 bytes for IPv6 (`sockaddr_in6`).

```
127.0.0.1:6379> BLOB.RDMA_HELLO <client address in hex>
1) "<server address 0 in hex>"
2) "<server address 1 in hex>"
```

## Memory region triples

`BLOB.RDMA_SET` and `BLOB.RDMA_GET` describe client memory as one or more triples:

```
rkey addr len [rkey addr len ...]
```

* `rkey` - the remote key from the client memory registration.
* `addr` - the address of the region in client memory.
  This is a virtual address, or an offset in the registered buffer when the provider does not use virtual addresses (`FI_MR_VIRT_ADDR`).
  `0` is a valid value.
* `len` - the length of the region in bytes.
  `0` is not valid.

All three values are unsigned decimal integers.
Hexadecimal and negative values are rejected.
The number of arguments after the fixed arguments must be a multiple of 3.
A command can have a maximum of 256 triples.

The server fills or reads the regions in the order of the command.
A chunk of the object can continue from the end of one region into the next region.
Thus one object can span buffers on several devices, or several buffers on one device.

## Length rules

* The sum of all region lengths must be equal to or larger than the object length.
  For `BLOB.RDMA_SET`, the object length is the `total-len` argument.
  For `BLOB.RDMA_GET`, it is the length of the stored object.
* Surplus region space is permitted.
  For `BLOB.RDMA_GET`, the reply gives the object length, which shows where the valid data ends.
* `total-len` must be larger than 0 and not larger than `largeobj.max-object-size`.

## CRC behavior

The server calculates a CRC32C (Castagnoli) checksum of the bytes of each stored object.

* `BLOB.RDMA_SET` can include `CRC <crc32c>` directly after `total-len`.
  The keyword is not case-sensitive, and the value is an unsigned 32-bit decimal integer.
  The server calculates the checksum of the bytes that it read.
  If the two values are different, the command fails with `ERR CRC mismatch after transfer` and the server does not store the object.
* `BLOB.RDMA_GET` replies with a two-element array, `[obj_len, crc32c]`, after all RDMA writes are complete.
  To make sure that the data is correct end to end, calculate the CRC32C of the first `obj_len` bytes in your regions and compare it with the reply.
* [`BLOB.INFO`](../commands/blob.info.md) returns the stored checksum with the `CRC` field.

The `largeobj.fabric-crc-pool-threads` configuration sets the number of server threads that calculate checksums of the data that `BLOB.RDMA_SET` transfers.

## Providers

The `largeobj.fabric-provider` configuration selects the libfabric provider when the module loads.

| Provider | Use | Address |
|:---------|:----|:--------|
| `EfaDirect` (default) | [Elastic Fabric Adapter (EFA)](https://aws.amazon.com/hpc/efa/) hardware RDMA | 32 bytes |
| `Emulated` | libfabric over TCP sockets, for development and tests only | 16 or 28 bytes (socket address) |

Use `Emulated` to develop and test RDMA client code (the `BLOB.RDMA_*` flow) on a host without RDMA hardware.
It runs libfabric over TCP sockets, so it is not for production and it is not faster than `BLOB.TCP_SET` and `BLOB.TCP_GET`.
In production on hosts without RDMA hardware, use the TCP commands.
For a test on one host, you can also set `largeobj.fabric-interfaces` to `lo` to serve only on the loopback interface.

If the provider does not start, the module loads and only the TCP commands are available.
`BLOB.RDMA_HELLO` then fails with `ERR RDMA provider unavailable on this instance`.

## Multiple fabric interfaces

A host can have more than one fabric interface (domain).
By default, the module starts one fabric service on each domain that the provider finds.
To use only some domains, set `largeobj.fabric-interfaces` to a comma-separated list of domain names.

The `BLOB.RDMA_HELLO` reply has one server address for each fabric service.
The client must add all of them, because the server can send a transfer from any of its fabric services.
For each transfer, the server picks two fabric services at random and uses the one with fewer transfers in progress.

At startup, the server log shows each service address as `largeobj: fabric service <i> rdma address <hex>`.

All DRAM pool segments, and in `Tiered` mode all disk staging segments, are registered with the fabric when the module starts and when the pool expands.
The `largeobj.max-rdma-registered-bytes` configuration (default 380GB) limits the total size of registered segments, so that the pool stays below the registration limit of the device.
The pool does not expand above this limit.
The `dram_rdma_registered_segments` field in `INFO largeobj` shows the number of registered DRAM pool segments.

## Cancel and timeout

If the server cannot post a transfer for 1 second (for example, because the client endpoint is gone), the command fails with `ERR RDMA read failed` or `ERR RDMA write failed`.
There is no other server-side timeout or abort for a transfer.
To stop a transfer, close the connection.
The client must keep its registered regions valid until it receives the reply.

## Errors

These are the RDMA errors that you are most likely to see.
For the full list, see the [module repository](https://github.com/valkey-io/valkey-large-object).

| Error | Cause |
|:------|:------|
| `ERR RDMA provider unavailable on this instance` | The fabric did not start. |
| `ERR rdma address must be 32 bytes`, `ERR rdma address is not a valid sockaddr` | The `BLOB.RDMA_HELLO` address does not agree with the fabric provider. |
| `ERR RDMA session already established` | A second `BLOB.RDMA_HELLO` on the same connection. |
| `ERR no RDMA session (call BLOB.RDMA_HELLO first)` | `BLOB.RDMA_SET` or `BLOB.RDMA_GET` without a session. |
| `ERR memory address args must be rkey, addr, len triples` | The region arguments are not a multiple of 3. |
| `ERR client memory address length <sum> smaller than object length <obj_len>` | The regions are too small for the object. |
| `ERR max object size exceeded` | `total-len` is larger than `largeobj.max-object-size`. |
| `ERR CRC mismatch after transfer` | The checksum of the transferred bytes is not equal to the `CRC` value. Nothing is stored. |
| `ERR RDMA read failed`, `ERR RDMA write failed` | An RDMA transfer from or into client memory failed. |

Both commands return `WRONGTYPE` when the key holds a different data type.
`BLOB.RDMA_SET` can also return the same storage errors as [`BLOB.TCP_SET`](../commands/blob.tcp_set.md), for example the `OOM` errors.

For the RDMA fields in `INFO largeobj`, see [What to watch](large-object-configuration.md#what-to-watch) and [`rdma`](large-object-configuration.md#rdma).

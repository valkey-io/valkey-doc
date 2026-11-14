---
title: "Valkey Large Object - Getting Started"
description: How to build, load, and try the Valkey Large Object module
---

> **Note:** [valkey-large-object](https://github.com/valkey-io/valkey-large-object) is at version 0.x.
> Commands, arguments, replies, and configuration can change before version 1.0.

This page shows how to build the module from source, load it into Valkey, and run your first commands.

## Requirements

* Valkey - Valkey 8.0 or later.
* Linux on `x86_64` or `aarch64` - The module has no architecture-specific code.
* Linux 5.1 or later (`Tiered` mode only) - The module uses io_uring for disk I/O, with the operations `IORING_OP_READV`, `IORING_OP_WRITEV`, `IORING_OP_READ_FIXED`, and `IORING_OP_WRITE_FIXED`, and with registered buffers (`IORING_REGISTER_BUFFERS`).
  These are in Linux 5.1 and later.
* Rust - A recent stable Rust toolchain with `cargo`, for example from [rustup](https://rustup.rs/).
* Build tools - `clang` and its development files (for example `libclang-dev`), `gcc`, `make`, `git`, and `pkg-config`.
* libfabric - libfabric 2.0 or later and its development files are necessary at build time, also when you use only TCP.
  The module uses the libfabric 2.0 interface (symbol version `FABRIC_1.8`), and the build needs the header `rdma/fi_collective.h`.
  An older libfabric, for example 1.8.0, fails.
  The build finds libfabric with `pkg-config`; check with `pkg-config --modversion libfabric`.
  If libfabric is in a different location, or the default libfabric is older than 2.0, set `PKG_CONFIG_PATH` to the `lib/pkgconfig` directory of the newer one.
  Then also set `LD_LIBRARY_PATH` to its `lib` directory when you run `valkey-server` or `build.sh`.
* EFA (optional) - The default fabric provider, `EfaDirect`, uses Elastic Fabric Adapter (EFA) hardware for RDMA.
  Without RDMA hardware, use the TCP commands.
  To develop and test RDMA client code without RDMA hardware, set `largeobj.fabric-provider` to `Emulated` (see [Providers](large-object-rdma.md#providers)).
* Locked memory - The module registers (pins) each segment one time for each fabric domain, and one more time for io_uring in `Tiered` mode.
  This counts against `RLIMIT_MEMLOCK`.
  Set the limit to `unlimited` (for example `ulimit -l unlimited`, or `LimitMEMLOCK=infinity` in a systemd unit), or to at least the total segment bytes times the number of registrations.
* RDMA clients - The libfabric provider of the client must support RMA (`FI_RMA`) with remote read and remote write, and the client needs a locked-memory limit for its registered buffers (see [Roles](large-object-rdma.md#roles)).
* XFS (`Tiered` mode only) - XFS is the only supported file system for `largeobj.disk-dir`, for example XFS on a local NVMe disk.
  The module needs `O_DIRECT` and user extended attributes (`user.*` attributes): it stores a small header for each object file in the `user.lobj` extended attribute.
  Other file systems, for example ext4, are not supported, also when they have these features.
  On such a file system, the module loads with a warning in the log.
  The module does not check for `O_DIRECT` and extended attributes when it loads.
  On a file system without them, every write fails with `ERR disk write failed`.

## Build from source

```bash
git clone https://github.com/valkey-io/valkey-large-object
cd valkey-large-object
cargo build --release
```

The build writes the module library to `target/release/libvalkey_large_object.so`.

The repository also has a `build.sh` script.
`./build.sh build` runs format and lint checks, the release build, and the unit tests.
`./build.sh` with no arguments also runs the integration tests against a Valkey server.

If `bindgen` cannot find the standard C headers (for example `stddef.h`), add the GCC include directory:

```bash
BINDGEN_EXTRA_CLANG_ARGS="-I$(gcc -print-file-name=include)" cargo build --release
```

## Load the module

Set the module configurations with their full `largeobj.` names after `--loadmodule`.
Memory sizes can have units, such as `64mb`.
To load the module from `valkey.conf` or with `MODULE LOADEX`, see [Set configurations](large-object-configuration.md#set-configurations).
For all parameters, see [Valkey Large Object - Configuration and Monitoring](large-object-configuration.md).

### Dram mode

This example loads the module in `Dram` mode with 64MB segments.
`largeobj.max-object-size` must fit in one segment, so this example sets it to 32MB.

```bash
valkey-server --port 6379 \
  --maxmemory 4gb \
  --maxmemory-policy allkeys-lru \
  --loadmodule ./target/release/libvalkey_large_object.so \
  --largeobj.operating-mode Dram \
  --largeobj.segment-size 64mb \
  --largeobj.max-object-size 32mb
```

In `Dram` mode, `maxmemory` is the DRAM limit, and `largeobj.max-rdma-registered-bytes` and the maximum number of segments also limit the DRAM pool.
With `allkeys-lru`, a write evicts the least recently used large objects when the module is full, and does not fail with `OOM`.
See [Memory and eviction](large-object-configuration.md#memory-and-eviction).

### Tiered mode

> **Warning:** In `Tiered` mode, the module deletes the `largeobj.disk-dir` directory and all its contents at startup and at shutdown, then creates it again, empty.
> Set `largeobj.disk-dir` to a new, empty directory that only this module uses, below the mount point (for example `/mnt/nvme/largeobj`).
> Never use a directory that has other data, or a mount point.

This example stores objects on NVMe in `/mnt/nvme/largeobj` and uses DRAM as a read cache.
It uses 64MB segments, a 32MB maximum object size and promotion size, a 10GB disk limit, and 64MB of disk staging buffers.

```bash
valkey-server --port 6379 \
  --maxmemory 4gb \
  --maxmemory-policy allkeys-lru \
  --loadmodule ./target/release/libvalkey_large_object.so \
  --largeobj.operating-mode Tiered \
  --largeobj.disk-dir /mnt/nvme/largeobj \
  --largeobj.segment-size 64mb \
  --largeobj.max-object-size 32mb \
  --largeobj.max-promote-size 32mb \
  --largeobj.disk-maxmemory 10gb \
  --largeobj.disk-staging-size 64mb
```

The module puts the object files in `largeobj.disk-dir-shards` subdirectories of `largeobj.disk-dir` (default 1024, named `0000` to `03ff`), and makes these subdirectories when it starts.

### Load failures

The module does not load if a configuration value is out of range, if the cross-configuration rules are not satisfied, or if the storage cannot start (for example, in `Tiered` mode, a `largeobj.disk-dir` that the module cannot create or clean).
The server log shows the cause.

These are log messages that you are most likely to see when the module does not load:

| Log message | Cause and fix |
|:------------|:--------------|
| ``libfabric.so.1: version `FABRIC_1.8' not found`` | An older libfabric is loaded at run time. Set `LD_LIBRARY_PATH` to the `lib` directory of libfabric 2.0 or later. |
| `fatal error: fi_collective.h: No such file or directory` (at build time) | The libfabric that `pkg-config` finds is older than 2.0. Set `PKG_CONFIG_PATH` to a newer libfabric. |
| `largeobj.segment-size is insufficient for largeobj.max-object-size` or `largeobj.max-promote-size` | See [Cross-configuration rules](large-object-configuration.md#cross-configuration-rules). |
| `largeobj: startup failed to reset disk-dir <dir>: Device or resource busy (os error 16); aborting module load` | `Tiered` mode: `largeobj.disk-dir` is a mount point. The module deletes the contents of the mounted file system, then cannot remove the mount point. Use a dedicated subdirectory of the mount for `largeobj.disk-dir`. |
| `largeobj: startup failed to reset disk-dir <dir>: <error>; aborting module load`, with an error such as `Permission denied` or `Read-only file system` | `Tiered` mode: the module deletes and creates `largeobj.disk-dir` at startup, and it could not. Make the parent directory of `largeobj.disk-dir` and the file system writable by the server user. |
| `largeobj: startup failed to reset disk-dir : disk-dir is required in Tiered operating mode; aborting module load` | `Tiered` mode: `largeobj.disk-dir` is not set. Set `largeobj.disk-dir` to a directory on the disk. |
| `largeobj: storage init failed: failed to create disk-dir shards under <dir>: <error>` | `Tiered` mode: the module could not create the `largeobj.disk-dir-shards` subdirectories, for example because the file system is full or read-only. Free space or fix the mount. |
| `largeobj: storage init failed: disk-dir <dir> has a block size of <N> B, which does not divide the 4096 B I/O alignment; ...` | `Tiered` mode: the file system block size does not divide 4096, for example 64KB blocks. The module cannot count disk use exactly, so it does not load. Put `largeobj.disk-dir` on a file system with a block size of 4096 B or less. |
| `largeobj: storage init failed: cannot read disk-dir <dir> XFS geometry: <error>`, or `cannot open disk-dir <dir>: <error>`, or `cannot statfs disk-dir <dir>: <error>` | `Tiered` mode: the module could not read the file system geometry that it needs to count disk use, so it does not load. Make sure that the mount is healthy and that the server can read `largeobj.disk-dir`. |
| `largeobj: storage init failed: too many segments (DRAM <n>, NVMe <m>). Max 16384 per pool. Increase segment-size or decrease disk-staging-size` | `Tiered` mode: `largeobj.disk-staging-size` divided by `largeobj.segment-size` is more than 16384. Make `largeobj.segment-size` larger or `largeobj.disk-staging-size` smaller. |
| `IORING_REGISTER_BUFFERS failed: Cannot allocate memory (os error 12)` | `Tiered` mode: the locked-memory limit is too low. Raise `RLIMIT_MEMLOCK` (see [Requirements](#requirements)). |
| `EFA registration of segment at ... failed (fatal)` | The server aborts, because a segment cannot be registered with the fabric. Raise the locked-memory limit (`ulimit -l`, `LimitMEMLOCK`), or set a lower `largeobj.max-rdma-registered-bytes`. |

If the fabric provider does not start, the module loads and only the TCP commands are available.
The server log then shows `largeobj: fabric unavailable, RDMA path disabled`.

If `largeobj.disk-dir` is not on XFS, the module loads, and the log shows `largeobj: disk-dir <dir> is not on XFS; disk usage is charged in 4096 B blocks`.
Only XFS is supported.
If `largeobj.disk-dir` does not support `O_DIRECT` or user extended attributes, the module loads, but every `Tiered` write fails with `ERR disk write failed`.

In `Tiered` mode, for all features the module needs an open-file limit of at least `2 x maxclients + 128 + largeobj.max-cached-fds`.
With the defaults (`maxclients` 10000, `largeobj.max-cached-fds` 16384), this is 36512.
Raise the limit with `ulimit -n` or `LimitNOFILE`, or set a lower `maxclients`.
With the default `largeobj.fd-reserve` value `Lenient`, the module also loads with a lower limit:

* Below `2 x maxclients + 128`, the file descriptor cache is off.
  With the default `maxclients` 10000, the log shows, for example, `fd placement and the fd cache are off; set LimitNOFILE to at least 20128 to turn them on`.
* Between that value and the full value, the file descriptor cache is smaller.
  With `maxclients` 1000 and an open-file limit of 10240, the log shows, for example, `the fd cache holds 8112; set LimitNOFILE to at least 18512 to cache all`.

With `largeobj.fd-reserve` set to `Strict`, the module does not load if the full limit is not available.

### Errors at run time

| Error | Cause and fix |
|:------|:--------------|
| `OOM command not allowed when used memory > 'maxmemory'.` | The DRAM pool is full, and eviction cannot free space. Use `allkeys-lru` or `volatile-lru`, or raise `maxmemory`. |
| `OOM command not allowed when used disk space > 'largeobj.disk-maxmemory'.` | `Tiered` mode: the disk limit is reached, and eviction cannot free space. Use a policy that permits eviction, or raise `largeobj.disk-maxmemory`. |
| `ERR disk staging buffer pool exhausted; retry later` | `Tiered` mode: too many concurrent disk operations for the disk staging buffers, not a lack of DRAM for data. A retry later can succeed. Raise `largeobj.disk-staging-size`, lower `largeobj.max-buffers-per-op`, or send fewer concurrent operations. |
| `ERR max object size exceeded` | The object is larger than `largeobj.max-object-size`. |
| `ERR failed to set key` | Rare: the server could not store the key after the write. Retry. |
| `ERR Protocol error: invalid bulk length`, and the connection closes | A `BLOB.TCP_SET` value is larger than the core `proto-max-bulk-len` (default 512MB). Raise `proto-max-bulk-len`, or use `BLOB.RDMA_SET`. |
| `ERR no RDMA session (call BLOB.RDMA_HELLO first)` | The connection has no RDMA session, for example a new connection after a cluster redirect. Send `BLOB.RDMA_HELLO` on it. |
| `ERR RDMA read failed`, `ERR RDMA write failed` | The transfer to or from client memory failed, for example because the client endpoint is gone or a region is not registered. |
| `ERR disk write failed`, `ERR disk read failed` | `Tiered` mode: disk I/O failed. Look at the server log. If every write fails, `largeobj.disk-dir` does not support `O_DIRECT` or user extended attributes. |
| `ERR command not allowed in MULTI, scripts or module calls` | The data commands are blocking commands. See [Limitations](large-object.md#limitations). |
| `DISABLED largeobj module is disabled` | `largeobj.enabled` is `no`. |

## Verify the module

Use `MODULE LIST` to make sure that the module is loaded.
The module name is `largeobj`.

```
127.0.0.1:6379> MODULE LIST
1) 1) "name"
   2) "largeobj"
   3) "ver"
   4) (integer) 1
   ...
```

To see the module commands, filter by the module ACL category:

```
127.0.0.1:6379> COMMAND LIST FILTERBY ACLCAT largeobj
1) "BLOB.TCP_SET"
2) "BLOB.TCP_GET"
3) "BLOB.RDMA_SET"
4) "BLOB.RDMA_GET"
5) "BLOB.INFO"
6) "BLOB.RDMA_HELLO"
```

The order of the list can be different.
`ver` is the version number that the module registers: 1 for version 0.1.0.

## First commands

Store a value, read it, and get its metadata with `valkey-cli`:

```
127.0.0.1:6379> BLOB.TCP_SET greeting hello
OK
127.0.0.1:6379> BLOB.TCP_GET greeting
"hello"
127.0.0.1:6379> BLOB.INFO greeting
1) len
2) (integer) 5
3) crc
4) (integer) 2591144780
5) tier
6) dram
127.0.0.1:6379> BLOB.INFO greeting LEN
(integer) 5
127.0.0.1:6379> BLOB.TCP_GET missing
(nil)
```

The `crc` value is the CRC32C checksum of the bytes `hello`.

To store a file as an object, use the `-x` option of `valkey-cli`, which reads the last argument from standard input:

```bash
valkey-cli -x BLOB.TCP_SET model:embeddings:v1 < embeddings.bin
```

Look at the module metrics:

```
127.0.0.1:6379> INFO largeobj
# largeobj_core_metrics
largeobj_num_objects:1
largeobj_inflight_requests:0

# largeobj_evictions
largeobj_evictions:0
largeobj_pending_evictions:0
...
```

Delete the object with the core `DEL` command:

```
127.0.0.1:6379> DEL greeting
(integer) 1
127.0.0.1:6379> BLOB.INFO greeting
(nil)
```

## Unload and clean up

You cannot unload the module with `MODULE UNLOAD`, because it registers a data type.
To remove the module, stop the server and start it again without the module.

All large objects are lost when the server stops (see [Persistence behavior](large-object.md#persistence-behavior)).
In `Tiered` mode, the module deletes `largeobj.disk-dir` at shutdown, or at the next startup after the server stops unexpectedly (see [Disk directory](large-object-configuration.md#disk-directory)).

## Next steps

* [Valkey Large Object - Use Cases and Examples](large-object-use-cases.md)
* [Valkey Large Object - RDMA Transfers](large-object-rdma.md)
* [Valkey Large Object - Configuration and Monitoring](large-object-configuration.md)
* [Large object command reference](../commands/#large-object)

Stores a large object at `key`.
The client sends the payload inline in the command, over the normal Valkey connection.
The object length is the byte length of `value`.

If `key` does not exist, the command creates it.
If `key` already holds a large object, the command replaces it, and the server frees the storage of the old object.
If `key` holds a value of a different type, the command returns a `WRONGTYPE` error and does not change the key.

The object must contain at least 1 byte.
The object length must not be more than the `largeobj.max-object-size` configuration (default 512MB).
The object length is also limited by the core `proto-max-bulk-len` configuration (default 512MB).
For a larger value, the server replies `ERR Protocol error: invalid bulk length` and closes the connection.
For the size limits and the memory configuration, see [Valkey Large Object - Configuration and Monitoring](../topics/large-object-configuration.md).

The server calculates a CRC32C (Castagnoli) checksum of the payload and stores it with the object.
Use [`BLOB.INFO`](blob.info.md) to read the length and the checksum.

In the `Dram` operating mode, the server stores the object in DRAM and then replies.
In the `Tiered` operating mode, the server writes the object to a file in `largeobj.disk-dir`, and replies only after the disk write is complete.
If too many disk operations run at the same time for the disk staging buffers, the command returns `ERR disk staging buffer pool exhausted; retry later`.
This is a limit on concurrent disk operations, not a lack of DRAM for data.
The error is temporary: a retry later can succeed, after operations in progress finish.
Raise `largeobj.disk-staging-size` (needs a restart), lower `largeobj.max-buffers-per-op`, or send fewer concurrent disk operations.
When there is not sufficient space, the server can evict other large objects to make room, if the eviction configuration permits it.

When two writes to the same key run at the same time, the write that the server received last is kept.
The server also replies `OK` to the write that it discards.

After a successful write, the server publishes the keyspace event `largeobj.create` (new key) or `largeobj.update` (replaced key), of type module, when `notify-keyspace-events` includes module key type events (`d`).
The server does not publish an event when the write fails.

The module does not replicate large objects or save their data to RDB or AOF.
This is a blocking command, so it cannot run in transactions, scripts, functions, or module calls.
For more information, see [Limitations](../topics/large-object.md#limitations).

To read the object back over TCP, use [`BLOB.TCP_GET`](blob.tcp_get.md).
To send the payload with RDMA instead of inline in the command, use [`BLOB.RDMA_SET`](blob.rdma_set.md).

## Reply

`OK` after the server stores the object.

An error occurs if the value is empty or larger than `largeobj.max-object-size`, if there is not sufficient memory or disk space, if a disk write fails, if the command runs in a transaction or a script, or if the key holds a value of a different type. See [Errors at run time](../topics/large-object-getting-started.md#errors-at-run-time) for all errors.

## Examples

```
127.0.0.1:6379> BLOB.TCP_SET mykey "hello world"
OK
127.0.0.1:6379> BLOB.TCP_GET mykey
"hello world"
127.0.0.1:6379> BLOB.TCP_SET mykey "123456789"
OK
127.0.0.1:6379> BLOB.INFO mykey LEN
(integer) 9
127.0.0.1:6379> BLOB.TCP_SET mykey ""
(error) ERR object length must be > 0
127.0.0.1:6379> SET mystring "abc"
OK
127.0.0.1:6379> BLOB.TCP_SET mystring "hello world"
(error) WRONGTYPE Operation against a key holding the wrong kind of value
```

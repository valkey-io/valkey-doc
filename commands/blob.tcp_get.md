Returns the payload of the large object stored at `key`.
The server sends the payload inline in the reply, over the normal Valkey connection.

If `key` does not exist, the command returns nil.
If `key` holds a value of a different type, the command returns a `WRONGTYPE` error.

The reply does not include the checksum.
To get the length and the CRC32C checksum of the object, use [`BLOB.INFO`](blob.info.md).

In the `Dram` operating mode, the server reads the object from DRAM.
In the `Tiered` operating mode, the server reads the object from the DRAM cache if a cached copy is ready.
Otherwise, the server reads the object from disk.
If too many disk operations run at the same time for the disk staging buffers, the command returns `ERR disk staging buffer pool exhausted; retry later`.
The error is temporary: a retry later can succeed, after operations in progress finish.
When an object gets sufficient reads, the server can copy it into the DRAM cache.
For the cache configuration, see [Valkey Large Object - Configuration and Monitoring](../topics/large-object-configuration.md).

This is a blocking command, so it cannot run in transactions, scripts, functions, or module calls (see [Limitations](../topics/large-object.md#limitations)).

To store an object over TCP, use [`BLOB.TCP_SET`](blob.tcp_set.md).
To write the payload directly into client memory with RDMA, use [`BLOB.RDMA_GET`](blob.rdma_get.md).

## Reply

One of the following:

* String: the payload of the object.
* Null: if the key does not exist.

An error occurs if a disk read fails, if `Tiered` mode has no free disk staging buffers, if the command runs in a transaction or a script, or if the key holds a value of a different type. See [Errors at run time](../topics/large-object-getting-started.md#errors-at-run-time) for all errors.

## Examples

```
127.0.0.1:6379> BLOB.TCP_SET mykey "Hello, large object!"
OK
127.0.0.1:6379> BLOB.TCP_GET mykey
"Hello, large object!"
127.0.0.1:6379> BLOB.TCP_GET nosuchkey
(nil)
```

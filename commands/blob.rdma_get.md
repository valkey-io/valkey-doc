Writes the payload of the large object stored at `key` directly into client memory with RDMA.
The payload does not go through the Valkey connection.

The connection must have an RDMA session.
To start a session, use [`BLOB.RDMA_HELLO`](blob.rdma_hello.md).

Each `region` is a triple that identifies a client memory region that the client registered with its libfabric endpoint:

* `rkey` - The remote key of the registered memory region.
* `addr` - The start address in the region.
  This is a virtual address, or an offset into the registered memory when the fabric provider does not use virtual addresses.
  `0` is a valid value.
* `len` - The number of bytes that the server can write into the region.
  The value must be more than `0`.

All values are unsigned decimal integers.
You can give up to 256 regions.
The server writes the object bytes into the regions in the order that you give them, and fills each region before it continues to the next one.

The total length of all the regions must be equal to or more than the object length.
The regions can be larger than the object.
The reply gives the object length, so that the client knows where the valid data ends.

The server replies only after all the RDMA writes are complete.
The reply is a two-element array: the object length in bytes, and the CRC32C (Castagnoli) checksum that the server stored for the object.
The client can calculate the checksum of the received bytes and compare it with this value.

If `key` does not exist, the command returns nil.
The server looks up the key before it parses the regions and before it checks the session.
Thus, a missing key returns nil even when the connection has no RDMA session.
In `Tiered` mode, if too many disk operations run at the same time for the disk staging buffers, the command returns `ERR disk staging buffer pool exhausted; retry later`.
The error is temporary: a retry later can succeed, after operations in progress finish.
If `key` holds a value of a different type, the command returns a `WRONGTYPE` error.

This is a blocking command, so it cannot run in transactions, scripts, functions, or module calls (see [Limitations](../topics/large-object.md#limitations)).

To read the payload over TCP instead, use [`BLOB.TCP_GET`](blob.tcp_get.md).
To get only the length and checksum, use [`BLOB.INFO`](blob.info.md).
If the server cannot post the transfer for 1 second (for example, because the client endpoint is gone), the command fails with `ERR RDMA write failed`.
There is no other server-side timeout for the transfer.
To stop a transfer, close the connection.
For more information, see [Valkey Large Object - RDMA Transfers](../topics/large-object-rdma.md).

## Reply

One of the following:

* Array: a two-element array, after all the RDMA writes are complete: the object length in bytes as an integer, and the CRC32C checksum of the object as an integer.
* Null: if the key does not exist.

An error occurs if the memory regions are not valid or are too small for the object, if the connection has no RDMA session, if the RDMA write or a disk read fails, or if the key holds a value of a different type. See [Errors](../topics/large-object-rdma.md#errors) for all errors.

## Examples

You cannot do the transfer from `valkey-cli`.
The command needs a client that has a libfabric endpoint and registered memory, and that has an RDMA session on the connection.
The example shows the command shape and the reply.
In this example, the key holds a 1MB (1048576 bytes) object of zero bytes.
The first command writes the object into one region.
The second command writes the object into two regions of 512KB each.

```
127.0.0.1:6379> BLOB.RDMA_GET mykey 4242 140237318455296 1048576
1) (integer) 1048576
2) (integer) 338267154
127.0.0.1:6379> BLOB.RDMA_GET mykey 4242 140237318455296 524288 4243 140237320552448 524288
1) (integer) 1048576
2) (integer) 338267154
127.0.0.1:6379> BLOB.RDMA_GET mykey 4242 140237318455296 4096
(error) ERR client memory address length 4096 smaller than object length 1048576
127.0.0.1:6379> BLOB.RDMA_GET nosuchkey 4242 140237318455296 1048576
(nil)
```

On a connection without an RDMA session, an existing key with regions that are large enough returns the session error.
The server checks the regions before the session:

```
127.0.0.1:6379> BLOB.RDMA_GET mykey 999 0 1048576
(error) ERR no RDMA session (call BLOB.RDMA_HELLO first)
```

Stores a large object at `key`.
The server reads the payload directly from client memory with RDMA.
The payload does not go through the Valkey connection.

The connection must have an RDMA session.
To start a session, use [`BLOB.RDMA_HELLO`](blob.rdma_hello.md).

`total-len` is the length of the object in bytes.
The object must contain at least 1 byte.
The object length must not be more than the `largeobj.max-object-size` configuration (default 512MB).

The optional `CRC` argument gives the CRC32C (Castagnoli) checksum of the payload, as an unsigned 32-bit decimal integer.
`CRC` must come directly after `total-len`.
When you give `CRC`, the server compares it with the checksum that it calculates after the transfer.
If the two values are different, the command returns an error and does not store the object.
The server always calculates the checksum and stores it with the object.

Each `region` is a triple that identifies a client memory region that the client registered with its libfabric endpoint:

* `rkey` - The remote key of the registered memory region.
* `addr` - The start address in the region.
  This is a virtual address, or an offset into the registered memory when the fabric provider does not use virtual addresses.
  `0` is a valid value.
* `len` - The number of bytes in the region.
  The value must be more than `0`.

All values are unsigned decimal integers.
You can give up to 256 regions.
The server reads `total-len` bytes from the regions in the order that you give them.
The total length of all the regions must be equal to or more than `total-len`.

The server replies `OK` only after it reads all the bytes and stores the object.
In the `Tiered` operating mode, the server replies only after the disk write is complete.

The overwrite, write-order, keyspace event, and eviction behavior is the same as for [`BLOB.TCP_SET`](blob.tcp_set.md).
If `key` holds a value of a different type, the command returns a `WRONGTYPE` error, and the server does not start a transfer.
The module does not replicate large objects or save their data to RDB or AOF.
This is a blocking command, so it cannot run in transactions, scripts, functions, or module calls.
For more information, see [Limitations](../topics/large-object.md#limitations).

To read the object with RDMA, use [`BLOB.RDMA_GET`](blob.rdma_get.md).
For more information, see [Valkey Large Object - RDMA Transfers](../topics/large-object-rdma.md) and [Valkey Large Object - Configuration and Monitoring](../topics/large-object-configuration.md).

## Reply

`OK` after the server reads all the bytes and stores the object.

An error occurs if an argument is not valid, if the connection has no RDMA session, if the RDMA read fails or the checksum is different from the `CRC` value, if there is not sufficient memory or disk space, or if the key holds a value of a different type. See [Errors](../topics/large-object-rdma.md#errors) for all errors.

## Examples

You cannot do the transfer from `valkey-cli`.
The command needs a client that has a libfabric endpoint and registered memory, and that has an RDMA session on the connection.
The example shows the command shape and the reply.
In this example, the client buffer holds 1MB (1048576 bytes) of zero bytes, with the CRC32C checksum `338267154`.

```
127.0.0.1:6379> BLOB.RDMA_SET mykey 1048576 4242 140237318455296 1048576
OK
127.0.0.1:6379> BLOB.RDMA_SET mykey 1048576 CRC 338267154 4242 140237318455296 524288 4243 140237320552448 524288
OK
127.0.0.1:6379> BLOB.INFO mykey
1) len
2) (integer) 1048576
3) crc
4) (integer) 338267154
5) tier
6) dram
127.0.0.1:6379> BLOB.RDMA_SET mykey 1048576 CRC 12345 4242 140237318455296 1048576
(error) ERR CRC mismatch after transfer
127.0.0.1:6379> BLOB.RDMA_SET mykey 1048576 4242 140237318455296 1048576 4243
(error) ERR memory address args must be rkey, addr, len triples
127.0.0.1:6379> BLOB.RDMA_SET mykey abc 4242 140237318455296 1048576
(error) ERR invalid len
127.0.0.1:6379> BLOB.RDMA_SET mykey 1048576 CRC 4294967296 4242 140237318455296 1048576
(error) ERR invalid CRC value
```

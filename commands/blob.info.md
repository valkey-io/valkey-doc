Returns metadata about the large object stored at `key`.
The command does not transfer the payload.

If you do not give a field, the command returns all the fields as a flat array of field names and values.
If you give one field, the command returns only the value of that field.
The field name is not case-sensitive.

The fields are:

* `LEN` - The length of the object, in bytes, as the client stored it.
  It does not include DRAM allocation overhead (`Dram` mode) or file system overhead (`Tiered` mode).
* `CRC` - The CRC32C (Castagnoli) checksum of the payload, as an unsigned 32-bit integer.
  The server calculates this value when it stores the object.
* `TIER` - The storage tier of the object: `dram` or `disk`.

In the `Dram` operating mode, `TIER` is always `dram`.
In the `Tiered` operating mode, `TIER` is `dram` only when a cached copy of the object is ready in DRAM.
Otherwise, `TIER` is `disk`.
For more information about the operating modes, see [Valkey Large Object - Overview](../topics/large-object.md).

If `key` does not exist, the command returns nil.
If `key` holds a value of a different type, the command returns a `WRONGTYPE` error.

Clients can compare `LEN` and `CRC` with the values that [`BLOB.RDMA_GET`](blob.rdma_get.md) returns, or with a checksum that they calculate after [`BLOB.TCP_GET`](blob.tcp_get.md).

## Reply

One of the following:

* Array: when no field is given, a flat array of field names and values: `len` and the object length as an integer, `crc` and the CRC32C checksum as an integer, and `tier` and the storage tier (`dram` or `disk`).
* Integer: the object length in bytes when `LEN` is given, or the CRC32C checksum when `CRC` is given.
* `dram` or `disk`: the storage tier when `TIER` is given.
* Null: if the key does not exist.

An error occurs if the field is not valid, if `largeobj.enabled` is `no`, or if the key holds a value of a different type.

## Examples

```
127.0.0.1:6379> BLOB.TCP_SET mykey "hello world"
OK
127.0.0.1:6379> BLOB.INFO mykey
1) len
2) (integer) 11
3) crc
4) (integer) 3381945770
5) tier
6) dram
127.0.0.1:6379> BLOB.INFO mykey LEN
(integer) 11
127.0.0.1:6379> BLOB.INFO mykey crc
(integer) 3381945770
127.0.0.1:6379> BLOB.INFO mykey TIER
dram
127.0.0.1:6379> BLOB.INFO mykey SIZE
(error) ERR invalid information field
127.0.0.1:6379> BLOB.INFO nosuchkey
(nil)
```

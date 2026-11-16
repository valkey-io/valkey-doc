Move `key` from the currently selected database (see [`SELECT`](select.md)) to the specified
destination database.
When `key` does not exist in the source database, it does nothing.
When `key` already exists in the destination database, it does nothing unless
the `REPLACE` option is given, in which case the existing key is overwritten.
Without `REPLACE`, it is possible to use `MOVE` as a locking primitive.

The caller must have access to the current and the destination databases. See
[database permissions](../topics/acl.md#database-permissions).

## Reply

One of the following:

* Integer: `1` if _key_ was moved.
* Integer: `0` if _key_ does not exist in the source database, or it already exists in the destination database and `REPLACE` was not given.

## Examples

```
127.0.0.1:6379> SET mykey "db0"
OK
127.0.0.1:6379> SELECT 1
OK
127.0.0.1:6379[1]> SET mykey "db1"
OK
127.0.0.1:6379[1]> SELECT 0
OK
127.0.0.1:6379> MOVE mykey 1
(integer) 0
127.0.0.1:6379> MOVE mykey 1 REPLACE
(integer) 1
127.0.0.1:6379> SELECT 1
OK
127.0.0.1:6379[1]> GET mykey
"db0"
```

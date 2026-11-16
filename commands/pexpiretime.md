`PEXPIRETIME` has the same semantic as [`EXPIRETIME`](expiretime.md), but returns the absolute Unix expiration timestamp in milliseconds instead of seconds.

## Reply

One of the following:

* Integer: Expiration Unix timestamp in milliseconds.
* Integer: `-1` if the key exists but has no associated expiration time.
* Integer: `-2` if the key does not exist.

## Examples

```
127.0.0.1:6379> SET mykey "Hello"
OK
127.0.0.1:6379> PEXPIREAT mykey 33177117420000
(integer) 1
127.0.0.1:6379> PEXPIRETIME mykey
(integer) 33177117420000
```

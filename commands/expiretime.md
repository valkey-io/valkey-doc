Returns the absolute Unix timestamp (since January 1, 1970) in seconds at which the given key will expire.

See also the [`PEXPIRETIME`](pexpiretime.md) command which returns the same information with milliseconds resolution.

## Reply

One of the following:

* Integer: the expiration Unix timestamp in seconds.
* Integer: `-1` if the key exists but has no associated expiration time.
* Integer: `-2` if the key does not exist.

## Examples

```
127.0.0.1:6379> SET mykey "Hello"
OK
127.0.0.1:6379> EXPIREAT mykey 33177117420
(integer) 1
127.0.0.1:6379> EXPIRETIME mykey
(integer) 33177117420
```

Returns the absolute Unix timestamp (since January 1, 1970) in seconds at which the given key will expire.

See also the `PEXPIRETIME` command which returns the same information with milliseconds resolution.

@examples

```valkey-cli
127.0.0.1:6379> SET mykey "Hello"
OK
127.0.0.1:6379> EXPIREAT mykey 33177117420
(integer) 1
127.0.0.1:6379> EXPIRETIME mykey
(integer) 33177117420
```

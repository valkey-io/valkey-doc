`PSETEX` works exactly like `SETEX` with the sole difference that the expire
time is specified in milliseconds instead of seconds.

## Examples

```valkey-cli
127.0.0.1:6379> PSETEX mykey 1000 "Hello"
OK
127.0.0.1:6379> PTTL mykey
(integer) 990
127.0.0.1:6379> GET mykey
"Hello"
```

Returns the string length of the value associated with `field` in the hash stored at `key`. If the `key` or the `field` do not exist, 0 is returned.

## Examples

```valkey-cli
127.0.0.1:6379> HSET myhash f1 HelloWorld f2 99 f3 -256
(integer) 3
127.0.0.1:6379> HSTRLEN myhash f1
(integer) 10
127.0.0.1:6379> HSTRLEN myhash f2
(integer) 2
127.0.0.1:6379> HSTRLEN myhash f3
(integer) 4
```

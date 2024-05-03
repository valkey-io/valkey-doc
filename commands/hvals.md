Returns all values in the hash stored at `key`.

## Examples

```valkey-cli
127.0.0.1:6379> HSET myhash field1 "Hello"
(integer) 1
127.0.0.1:6379> HSET myhash field2 "World"
(integer) 1
127.0.0.1:6379> HVALS myhash
1) "Hello"
2) "World"
```

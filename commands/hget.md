Returns the value associated with `field` in the hash stored at `key`.

## Examples

```valkey-cli
127.0.0.1:6379> HSET myhash field1 "foo"
(integer) 1
127.0.0.1:6379> HGET myhash field1
"foo"
127.0.0.1:6379> HGET myhash field2
(nil)
```

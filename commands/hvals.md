Returns all values in the hash stored at `key`.

## Reply

Array of values in the hash, or an empty array when the key does not exist.

## Examples

```
127.0.0.1:6379> HSET myhash field1 "Hello"
(integer) 1
127.0.0.1:6379> HSET myhash field2 "World"
(integer) 1
127.0.0.1:6379> HVALS myhash
1) "Hello"
2) "World"
```

Returns all field names in the hash stored at `key`.

## Reply

Array of fields in the hash, or an empty array when the key does not exist.

## Examples

```
127.0.0.1:6379> HSET myhash field1 "Hello"
(integer) 1
127.0.0.1:6379> HSET myhash field2 "World"
(integer) 1
127.0.0.1:6379> HKEYS myhash
1) "field1"
2) "field2"
```

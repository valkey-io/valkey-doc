Returns the value associated with `field` in the hash stored at `key`.

## Reply

One of the following:

* String: The value associated with the field.
* Null: If the field is not present in the hash or key does not exist.

## Examples

```
127.0.0.1:6379> HSET myhash field1 "foo"
(integer) 1
127.0.0.1:6379> HGET myhash field1
"foo"
127.0.0.1:6379> HGET myhash field2
(nil)
```

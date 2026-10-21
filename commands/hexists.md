Returns if `field` is an existing field in the hash stored at `key`.

## Reply

One of the following:

* Integer: `0` if the hash does not contain the field, or the key does not exist.
* Integer: `1` if the hash contains the field.

## Examples

```
127.0.0.1:6379> HSET myhash field1 "foo"
(integer) 1
127.0.0.1:6379> HEXISTS myhash field1
(integer) 1
127.0.0.1:6379> HEXISTS myhash field2
(integer) 0
```

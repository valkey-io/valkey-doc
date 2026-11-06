Sets `field` in the hash stored at `key` to `value`, only if `field` does not
yet exist.
If `key` does not exist, a new key holding a hash is created.
If `field` already exists, this operation has no effect.

## Reply

One of the following:

* Integer: `0` if the field already exists in the hash and no operation was performed.
* Integer: `1` if the field is a new field in the hash and the value was set.

## Examples

```
127.0.0.1:6379> HSETNX myhash field "Hello"
(integer) 1
127.0.0.1:6379> HSETNX myhash field "World"
(integer) 0
127.0.0.1:6379> HGET myhash field
"Hello"
```

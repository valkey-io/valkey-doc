Returns the string length of the value associated with `field` in the hash stored at `key`. If the `key` or the `field` do not exist, 0 is returned.

## Reply

Integer: the string length of the value associated with the _field_, or zero when the _field_ isn't present in the hash or the _key_ doesn't exist at all.

## Examples

```
127.0.0.1:6379> HSET myhash f1 HelloWorld f2 99 f3 -256
(integer) 3
127.0.0.1:6379> HSTRLEN myhash f1
(integer) 10
127.0.0.1:6379> HSTRLEN myhash f2
(integer) 2
127.0.0.1:6379> HSTRLEN myhash f3
(integer) 4
```

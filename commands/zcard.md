Returns the sorted set cardinality (number of elements) of the sorted set stored
at `key`.

## Reply

Integer: the cardinality (number of members) of the sorted set, or 0 if the key doesn't exist.

## Examples

```
127.0.0.1:6379> ZADD myzset 1 "one"
(integer) 1
127.0.0.1:6379> ZADD myzset 2 "two"
(integer) 1
127.0.0.1:6379> ZCARD myzset
(integer) 2
```

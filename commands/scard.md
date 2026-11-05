Returns the set cardinality (number of elements) of the set stored at `key`.

## Reply

Integer: the cardinality (number of elements) of the set, or `0` if the key does not exist.

## Examples

```
127.0.0.1:6379> SADD myset "Hello"
(integer) 1
127.0.0.1:6379> SADD myset "World"
(integer) 1
127.0.0.1:6379> SCARD myset
(integer) 2
```

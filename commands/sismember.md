Returns if `member` is a member of the set stored at `key`.

## Reply

One of the following:

* Integer: `0` if the element is not a member of the set, or when the key does not exist.
* Integer: `1` if the element is a member of the set.

## Examples

```
127.0.0.1:6379> SADD myset "one"
(integer) 1
127.0.0.1:6379> SISMEMBER myset "one"
(integer) 1
127.0.0.1:6379> SISMEMBER myset "two"
(integer) 0
```

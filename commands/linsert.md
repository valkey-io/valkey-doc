Inserts `element` in the list stored at `key` either before or after the reference
value `pivot`.

When `key` does not exist, it is considered an empty list and no operation is
performed.

An error is returned when `key` exists but does not hold a list value.

## Reply

One of the following:

* Integer: the list length after a successful insert operation.
* Integer: `0` when the key doesn't exist.
* Integer: `-1` when the pivot wasn't found.

## Examples

```
127.0.0.1:6379> RPUSH mylist "Hello"
(integer) 1
127.0.0.1:6379> RPUSH mylist "World"
(integer) 2
127.0.0.1:6379> LINSERT mylist BEFORE "World" "There"
(integer) 3
127.0.0.1:6379> LRANGE mylist 0 -1
1) "Hello"
2) "There"
3) "World"
```

Returns the specified elements of the list stored at `key`.
The offsets `start` and `stop` are zero-based indexes, with `0` being the first
element of the list (the head of the list), `1` being the next element and so
on.

These offsets can also be negative numbers indicating offsets starting at the
end of the list.
For example, `-1` is the last element of the list, `-2` the penultimate, and so
on.

## Consistency with range functions in various programming languages

Note that if you have a list of numbers from 0 to 100, `LRANGE list 0 10` will
return 11 elements, that is, the rightmost item is included.
This **may or may not** be consistent with behavior of range-related functions
in your programming language of choice (think Ruby's `Range.new`, `Array#slice`
or Python's `range()` function).

## Out-of-range indexes

Out of range indexes will not produce an error.
If `start` is larger than the end of the list, an empty list is returned.
If `stop` is larger than the actual end of the list, Valkey will treat it like
the last element of the list.

## Examples

```
127.0.0.1:6379> RPUSH mylist "one"
(integer) 1
127.0.0.1:6379> RPUSH mylist "two"
(integer) 2
127.0.0.1:6379> RPUSH mylist "three"
(integer) 3
127.0.0.1:6379> LRANGE mylist 0 0
1) "one"
127.0.0.1:6379> LRANGE mylist -3 2
1) "one"
2) "two"
3) "three"
127.0.0.1:6379> LRANGE mylist -100 100
1) "one"
2) "two"
3) "three"
127.0.0.1:6379> LRANGE mylist 5 10
(empty array)
```

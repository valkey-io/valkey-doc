Returns the score of `member` in the sorted set at `key`.

If `member` does not exist in the sorted set, or `key` does not exist, `nil` is
returned.

## Reply

One of the following:

* Double: the score of the member (a double-precision floating point number).
* Null: if _member_ does not exist in the sorted set, or the key does not exist.

## Examples

```
127.0.0.1:6379> ZADD myzset 1 "one"
(integer) 1
127.0.0.1:6379> ZSCORE myzset "one"
"1"
```

Search for the first occurrence of a scalar JSON value in the arrays at the path.


* Out of range errors are treated by rounding the index to the array's start and end.
* If start > end, return -1 (not found).

## Syntax

```bash
JSON.ARRINDEX <key> <path> <json-scalar> [start [end]]
```

* key - required, Redis key of document type.
* path - required, a JSON path.
* json-scalar - required, scalar value to search for. JSON scalar refers to values that are not objects or arrays.
  i.e., String, number, boolean and null are scalar values.
* start - optional, start index, inclusive. Defaults to 0 if not provided.
* end - optional, end index, exclusive. Defaults to 0 if not provided, which means the last element is included.
  0 or -1 means the last element is included.

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], ["a"], ["a", "b"], ["a", "b", "c"]]'
OK
127.0.0.1:6379> JSON.ARRINDEX k1 $[*] '"b"'
1) (integer) -1
2) (integer) -1
3) (integer) 1
4) (integer) 1
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"children": ["John", "Jack", "Tom", "Bob", "Mike"]}'
OK
127.0.0.1:6379> JSON.ARRINDEX k1 .children '"Tom"'
(integer) 2
```

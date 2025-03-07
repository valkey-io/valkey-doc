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

## Return

* If the path is enhanced syntax:
    * Array of integers. Each value is the index of the matching element in the array at the path. The value is -1 if not found.
    * If a value is not an array, its corresponding return value is null.

* If the path is restricted syntax:
    * Integer, the index of matching element, or -1 if not found.
    * WRONGTYPE error if the value at the path is not an array.

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

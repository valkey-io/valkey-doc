Insert one or more values into the array values at path before the index.


* Inserting at index 0 prepends to the array.
* A negative index values is interpreted as starting from the end.
* The index must be in the array's boundary.

## Syntax

```bash
JSON.ARRINSERT <key> <path> <index> <json> [json ...]
```

* key - required, Redis key of document type
* path - required, a JSON path
* index - required, array index before which values are inserted.
* json - required, JSON value to be appended to the array

## Return

* If the path is restricted syntax:
    * Array of integers, representing the new length of the array at each path.
    * If a value is an empty array, its corresponding return value is null.
    * If a value is not an array, its corresponding return value is null.
    * OUTOFBOUNDARIES error if the index argument is out of bounds.

* If the path is restricted syntax:
    * Integer, the new length of the array.
    * WRONGTYPE error if the value at the path is not an array.
    * OUTOFBOUNDARIES error if the index argument is out of bounds.

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], ["a"], ["a", "b"]]'
OK
127.0.0.1:6379> JSON.ARRINSERT k1 $[*] 0 '"c"'
1) (integer) 1
2) (integer) 2
3) (integer) 3
127.0.0.1:6379> JSON.GET k1
"[[\"c\"],[\"c\",\"a\"],[\"c\",\"a\",\"b\"]]"
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], ["a"], ["a", "b"]]'
OK
127.0.0.1:6379> JSON.ARRINSERT k1 . 0 '"c"'
(integer) 4
127.0.0.1:6379> JSON.GET k1
"[\"c\",[],[\"a\"],[\"a\",\"b\"]]"
```

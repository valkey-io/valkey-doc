Trim arrays at the path so that it becomes subarray [start, end], both inclusive.\n\n* If the array is empty, do nothing, return 0.\n* If start < 0, treat it as 0.\n* If end >= size (size of the array), treat it as size-1.\n* If start >= size or start > end, empty the array and return 0.

## Syntax

```bash
JSON.ARRTRIM <key> <path> <start> <end>
```

* key - required, Redis key of document type.
* path - required, a JSON path.
* start - required, start index, inclusive.
* end - required, end index, inclusive.

## Return

* If the path is restricted syntax:
    * Array of integers, representing the new length of the array at each path.
    * If a value is an empty array, its corresponding return value is null.
    * If a value is not an array, its corresponding return value is null.
    * OUTOFBOUNDARIES error if an index argument is out of bounds.

* If the path is restricted syntax:
    * Integer, the new length of the array.
    * Null if the array is empty.
    * WRONGTYPE error if the value at the path is not an array.
    * OUTOFBOUNDARIES error if an index argument is out of bounds.

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], ["a"], ["a", "b"], ["a", "b", "c"]]'
OK
127.0.0.1:6379> JSON.ARRTRIM k1 $[*] 0 1
1) (integer) 0
2) (integer) 1
3) (integer) 2
4) (integer) 2
   127.0.0.1:6379> JSON.GET k1
   "[[],[\"a\"],[\"a\",\"b\"],[\"a\",\"b\"]]"
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"children": ["John", "Jack", "Tom", "Bob", "Mike"]}'
OK
127.0.0.1:6379> JSON.ARRTRIM k1 .children 0 1
(integer) 2
127.0.0.1:6379> JSON.GET k1 .children
"[\"John\",\"Jack\"]"
```

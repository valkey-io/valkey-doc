## Syntax

```bash
JSON.ARRPOP <key> [path [index]]
```

* key - required, Redis key of document type
* path - optional, a JSON path. Defaults to the root path if not provided
* index - optional, position in the array to start popping from.
    * Defaults -1 if not provided, which means the last element.
    * Negative value means position from the last element.
    * Out of boundary indexes are rounded to their respective array boundaries.

## Return

* If the path is enhanced syntax:
    * Array of bulk strings, representing popped values at each path.
    * If a value is an empty array, its corresponding return value is null.
    * If a value is not an array, its corresponding return value is null.

* If the path is restricted syntax:
    * Bulk string, representing the popped JSON value
    * Null if the array is empty.
    * WRONGTYPE error if the value at the path is not an array.

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], ["a"], ["a", "b"]]'
OK
127.0.0.1:6379> JSON.ARRPOP k1 $[*]
1) (nil)
2) "\"a\""
3) "\"b\""
127.0.0.1:6379> JSON.GET k1
"[[],[],[\"a\"]]"
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], ["a"], ["a", "b"]]'
OK
127.0.0.1:6379> JSON.ARRPOP k1
"[\"a\",\"b\"]"
127.0.0.1:6379> JSON.GET k1
"[[],[\"a\"]]"

127.0.0.1:6379> JSON.SET k2 . '[[], ["a"], ["a", "b"]]'
OK
127.0.0.1:6379> JSON.ARRPOP k2 . 0
"[]"
127.0.0.1:6379> JSON.GET k2
"[[\"a\"],[\"a\",\"b\"]]"
```

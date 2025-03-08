## Syntax

```bash
JSON.CLEAR <key> <path>
```

* key - required, Redis key of document type.
* path - optional, a JSON path. Defaults to the root path if not provided

## Return

* Integer, the number of containers cleared.
* Clearing an empty array or object accounts for 0 container cleared.
* Clearing a non-container value returns 0.
* If no array or object value is located by the path, the command returns 0.

## Examples

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], [0], [0,1], [0,1,2], 1, true, null, "d"]'
OK
127.0.0.1:6379>  JSON.CLEAR k1  $[*]
(integer) 6
127.0.0.1:6379> JSON.CLEAR k1  $[*]
(integer) 0 
127.0.0.1:6379> JSON.SET k2 . '{"children": ["John", "Jack", "Tom", "Bob", "Mike"]}'
OK
127.0.0.1:6379> JSON.CLEAR k2 .children
(integer) 1
127.0.0.1:6379> JSON.GET k2 .children
"[]"
```

Append a string to the JSON strings at the path.

## Syntax

```bash
JSON.STRAPPEND <key> [path] <json_string>
```

* key - required, Redis key of document type
* path - optional, a JSON path. Defaults to the root path if not provided
* json_string - required, JSON representation of a string. Note that a JSON string must be quoted, i.e., '"foo"'.

## Return

* If the path is enhanced syntax:
    * Array of integers, representing the new length of the string at each path.
    * If a value at the path is not a string, its corresponding return value is null.
    * SYNTAXERR error if the input json argument is not a valid JSON string.
    * NONEXISTENT error if the path does not exist.

* If the path is restricted syntax:
    * Integer, the string's new length.
    * If multiple string values are selected, the command returns the new length of the last updated string.
    * WRONGTYPE error if the value at the path is not a string.
    * WRONGTYPE error if the input json argument is not a valid JSON string.
    * NONEXISTENT error if the path does not exist.

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 $ '{"a":{"a":"a"}, "b":{"a":"a", "b":1}, "c":{"a":"a", "b":"bb"}, "d":{"a":1, "b":"b", "c":3}}'
OK
127.0.0.1:6379> JSON.STRAPPEND k1 $.a.a '"a"'
1) (integer) 2
127.0.0.1:6379> JSON.STRAPPEND k1 $.a.* '"a"'
1) (integer) 3
127.0.0.1:6379> JSON.STRAPPEND k1 $.b.* '"a"'
1) (integer) 2
2) (nil)
127.0.0.1:6379> JSON.STRAPPEND k1 $.c.* '"a"'
1) (integer) 2
2) (integer) 3
127.0.0.1:6379> JSON.STRAPPEND k1 $.c.b '"a"'
1) (integer) 4
127.0.0.1:6379> JSON.STRAPPEND k1 $.d.* '"a"'
1) (nil)
2) (integer) 2
3) (nil)
````

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"a":{"a":"a"}, "b":{"a":"a", "b":1}, "c":{"a":"a", "b":"bb"}, "d":{"a":1, "b":"b", "c":3}}'
OK
127.0.0.1:6379> JSON.STRAPPEND k1 .a.a '"a"'
(integer) 2
127.0.0.1:6379> JSON.STRAPPEND k1 .a.* '"a"'
(integer) 3
127.0.0.1:6379> JSON.STRAPPEND k1 .b.* '"a"'
(integer) 2
127.0.0.1:6379> JSON.STRAPPEND k1 .c.* '"a"'
(integer) 3
127.0.0.1:6379> JSON.STRAPPEND k1 .c.b '"a"'
(integer) 4
127.0.0.1:6379> JSON.STRAPPEND k1 .d.* '"a"'
(integer) 2
```

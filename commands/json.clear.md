Clear the values at the path.
Arrays and objects become empty.
Strings become empty strings, numbers become 0 and booleans become `false`.
Null values are not changed.

## Reply

* Integer:
  * The number of values cleared.
  * A value is counted only if it changes: a non-empty array, object or string, a non-zero number, or `true`.
  * Returns 0 if the values are already empty, 0, `false` or `null`.
  * Returns 0 if no value is located by the path.
* Error:
  * if the document key does not exist.

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

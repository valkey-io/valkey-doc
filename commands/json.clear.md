Clear the arrays or objects at the path.

## Reply

* Integer:
  * The number of containers cleared.
  * Returns 0 if clearing an empty array or object.
  * Returns 0 if clearing a non-container value.
  * Returns 0 if no array or object value is located by the path.

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

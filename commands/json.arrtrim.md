Trim arrays at the path so that it becomes subarray [start, end], both inclusive.


* If the array is empty, do nothing, return 0.
* If start < 0, treat it as 0.
* If end >= size (size of the array), treat it as size-1.
* If start >= size or start > end, empty the array and return 0.

## Reply

* If the path is enhanced syntax:
  * Array of integers representing the new length of the array at each path.
  * Null: For each path where the value is an empty array or not an array.
* If the path is restricted syntax:
  * Integer: The new length of the array.
  * Null: If the array is empty.
* Error:
  * if the value at the path is not an array (only for restricted syntax).
  * if an index argument is out of bounds.

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

Insert one or more values into the array values at path before the index.


* Inserting at index 0 prepends to the array.
* A negative index values is interpreted as starting from the end.
* The index must be in the array's boundary.

## Reply

* If the path is enhanced syntax:
  * Array of integers representing the new length of the array at each path.
  * Null: For each path where the value is an empty array or not an array.
* If the path is restricted syntax:
  * Integer: The new length of the array.
* Error:
  * if the path does not exist.
  * if the value at the path is not an array (only for restricted syntax).
  * if the index argument is out of bounds.

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

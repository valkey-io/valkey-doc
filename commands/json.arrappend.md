Append one or more values to the array values at the path.

## Reply

* If the path is enhanced syntax:
  * Array of integers representing the new length of the array at each path.
  * Null: For each path where the value is not an array.
* If the path is restricted syntax:
  * Integer: The array's new length.
  * Integer: If multiple array values are selected, the command returns the new length of the last updated array.
* Error:
  * if the path does not exist.
  * if the value at the path is not an array (only for restricted syntax).

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], ["a"], ["a", "b"]]'
OK
127.0.0.1:6379> JSON.ARRAPPEND  k1 $[*] '"c"'
1) (integer) 1
2) (integer) 2
3) (integer) 3
127.0.0.1:6379> JSON.GET k1
"[[\"c\"],[\"a\",\"c\"],[\"a\",\"b\",\"c\"]]"
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[[], ["a"], ["a", "b"]]'
OK
127.0.0.1:6379> JSON.ARRAPPEND  k1 [-1] '"c"'
(integer) 3
127.0.0.1:6379> JSON.GET k1
"[[],[\"a\"],[\"a\",\"b\",\"c\"]]"
```

Get key names in the object values at the path.

## Reply

* If the path is enhanced syntax:
  * Array of arrays, each containing bulk strings representing keys in a matching object.
  * Array: Empty array for each path where the value is not an object.
  * Null: If the document key does not exist.
* If the path is restricted syntax:
  * Array of bulk strings, each representing a key name in the object.
  * Array: If multiple objects are selected, returns the keys of the first object.
  * Null: If the document key does not exist.
* Error:
  * if the value at the path is not an object (only for restricted syntax).
  * if the path does not exist (only for restricted syntax).

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 $ '{"a":{}, "b":{"a":"a"}, "c":{"a":"a", "b":"bb"}, "d":{"a":1, "b":"b", "c":{"a":3,"b":4}}, "e":1}'
OK
127.0.0.1:6379> JSON.OBJKEYS k1 $.*
1) (empty array)
2) 1) "a"
3) 1) "a"
   2) "b"
4) 1) "a"
   2) "b"
   3) "c"
5) (empty array)
127.0.0.1:6379> JSON.OBJKEYS k1 $.d
1) 1) "a"
   2) "b"
   3) "c"
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 $ '{"a":{}, "b":{"a":"a"}, "c":{"a":"a", "b":"bb"}, "d":{"a":1, "b":"b", "c":{"a":3,"b":4}}, "e":1}'
OK
127.0.0.1:6379> JSON.OBJKEYS k1 .*
1) "a"
127.0.0.1:6379> JSON.OBJKEYS k1 .d
1) "a"
2) "b"
3) "c"
```

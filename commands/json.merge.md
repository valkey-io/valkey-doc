Merge a JSON value into the value at the path using [RFC 7386](https://www.rfc-editor.org/rfc/rfc7386) JSON Merge Patch semantics.

* If the key does not exist:
    * A new key is created when the path is the document root (`.` or `$`).
    * Otherwise, the command returns a `SYNTAXERR` error.
* If the key exists:
    * If the value at the path is an object and the patch value is an object, members are merged recursively:
        * Members present only in the patch are added.
        * Members present in both are replaced by the merged result.
        * Members set to `null` in the patch are deleted from the target.
    * If the patch value is not an object (for example a string, number, boolean, array, or `null`), the value at the path is replaced entirely.
    * If the path exists except for the final child, and the parent is an object, the final child is created and set to the patch value.
    * Arrays are replaced, not merged element-by-element.
* Document nesting is subject to the configured maximum depth (`json.max-path-limit`).
  Once the recursion depth reaches that limit, merging stops and the new value is used as-is for the remainder of the path.

## Examples

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.MERGE k1 . '{"a":1,"b":2}'
OK
127.0.0.1:6379> JSON.GET k1
"{\"a\":1,\"b\":2}"
127.0.0.1:6379> JSON.MERGE k1 . '{"b":3,"c":4}'
OK
127.0.0.1:6379> JSON.GET k1
"{\"a\":1,\"b\":3,\"c\":4}"

127.0.0.1:6379> JSON.SET k2 . '{"a":{"x":1,"y":2},"b":10}'
OK
127.0.0.1:6379> JSON.MERGE k2 .a '{"y":3,"z":4}'
OK
127.0.0.1:6379> JSON.GET k2 .a
"{\"x\":1,\"y\":3,\"z\":4}"

127.0.0.1:6379> JSON.SET k3 . '{"a":1,"b":2,"c":3}'
OK
127.0.0.1:6379> JSON.MERGE k3 . '{"b":null}'
OK
127.0.0.1:6379> JSON.GET k3
"{\"a\":1,\"c\":3}"

127.0.0.1:6379> JSON.SET k4 . '{"str":"hello","arr":[1,2,3],"obj":{"x":1}}'
OK
127.0.0.1:6379> JSON.MERGE k4 . '{"str":"world","arr":[4,5],"obj":{"y":2}}'
OK
127.0.0.1:6379> JSON.GET k4
"{\"str\":\"world\",\"arr\":[4,5],\"obj\":{\"x\":1,\"y\":2}}"
```

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"users":[{"name":"Alice","meta":{"active":false}},{"name":"Bob","meta":{"active":false}}]}'
OK
127.0.0.1:6379> JSON.MERGE k1 '$..meta' '{"active":true,"updated":true}'
OK
127.0.0.1:6379> JSON.GET k1 .users[0].meta
"{\"active\":true,\"updated\":true}"
127.0.0.1:6379> JSON.GET k1 .users[1].meta
"{\"active\":true,\"updated\":true}"
```

Get the value of `key`.
If the key does not exist the special value `nil` is returned.
An error is returned if the value stored at `key` is not a string, because `GET`
only handles string values.

## Reply

One of the following:

* String: the value of the key.
* Null: if the key does not exist.

## Examples

```
127.0.0.1:6379> GET nonexisting
(nil)
127.0.0.1:6379> SET mykey "Hello"
OK
127.0.0.1:6379> GET mykey
"Hello"
```

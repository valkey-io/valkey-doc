Get the value of `key` and delete the key.
This command is similar to `GET`, except for the fact that it also deletes the key on success (if and only if the key's value type is a string).

## Reply

One of the following:

* String: the value of the key.
* Null: if the key does not exist or if the key's value type is not a string.

## Examples

```
127.0.0.1:6379> SET mykey "Hello"
OK
127.0.0.1:6379> GETDEL mykey
"Hello"
127.0.0.1:6379> GET mykey
(nil)
```

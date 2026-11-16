Returns the length of the string value stored at `key`.
An error is returned when `key` holds a non-string value.

## Reply

Integer: the length of the string stored at key, or 0 when the key does not exist.

## Examples

```
127.0.0.1:6379> SET mykey "Hello world"
OK
127.0.0.1:6379> STRLEN mykey
(integer) 11
127.0.0.1:6379> STRLEN nonexisting
(integer) 0
```

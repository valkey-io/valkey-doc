Returns the substring of the string value stored at `key`, determined by the
offsets `start` and `end` (both are inclusive).
Negative offsets can be used in order to provide an offset starting from the end
of the string.
So -1 means the last character, -2 the penultimate and so forth.

The function handles out of range requests by limiting the resulting range to
the actual length of the string.

## Examples

```
127.0.0.1:6379> SET mykey "This is a string"
OK
127.0.0.1:6379> GETRANGE mykey 0 3
"This"
127.0.0.1:6379> GETRANGE mykey -3 -1
"ing"
127.0.0.1:6379> GETRANGE mykey 0 -1
"This is a string"
127.0.0.1:6379> GETRANGE mykey 10 100
"string"
```

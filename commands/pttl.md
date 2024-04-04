Like `TTL` this command returns the remaining time to live of a key that has an
expire set, with the sole difference that `TTL` returns the amount of remaining
time in seconds while `PTTL` returns it in milliseconds.

The command returns the following values in case of errors:

* The command returns `-2` if the key does not exist.
* The command returns `-1` if the key exists but has no associated expire.

@examples

```cli
SET mykey "Hello"
EXPIRE mykey 1
PTTL mykey
```

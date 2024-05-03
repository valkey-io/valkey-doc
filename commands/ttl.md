Returns the remaining time to live of a key that has a timeout.
This introspection capability allows a Valkey client to check how many seconds a
given key will continue to be part of the dataset.

The command returns the following valueis in case of errors:

* The command returns `-2` if the key does not exist.
* The command returns `-1` if the key exists but has no associated expire.

See also the `PTTL` command that returns the same information with milliseconds resolution.

## Examples

```valkey-cli
127.0.0.1:6379> SET mykey "Hello"
OK
127.0.0.1:6379> EXPIRE mykey 10
(integer) 1
127.0.0.1:6379> TTL mykey
(integer) 10
```

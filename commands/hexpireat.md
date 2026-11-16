`HEXPIREAT` has the same effect and semantic as [`HEXPIRE`](hexpire.md), but instead of
specifying the number of seconds representing the TTL (time to live), it takes
an absolute Unix timestamp (seconds since January 1, 1970). A
timestamp in the past will delete the key immediately.

For the specific semantics of the command refer to the documentation of
[`HEXPIRE`](hexpire.md).

## Options

The `HEXPIREAT` command supports a set of options that modify its behavior:

* NX — For each specified field, set expiration only when the field has no expiration.
* XX — For each specified field, set expiration only when the field has an existing expiration.
* GT — For each specified field, set expiration only when the new expiration is greater than current one.
* LT — For each specified field, set expiration only when the new expiration is less than current one.

## Reply

Array of integer codes indicating the result of setting expiry on each specified field, in the same order as the fields are requested.

* -2: Field does not exist in the HASH, or key does not exist.
* 0: The specified NX | XX | GT | LT condition has not been met.
* 1: The expiration time was applied.
* 2: When called with 0 seconds.

## Examples

```
127.0.0.1:6379> HSET myhash f1 v1 f2 v2 f3 v3
(integer) 3
27.0.0.1:6379> HEXPIREAT myhash 1754846600 FIELDS 2 f2 f3
1) (integer) 1
2) (integer) 1
127.0.0.1:6379> HEXPIRETIME myhash FIELDS 3 f1 f2 f3
1) (integer) -1
2) (integer) 1754846600
3) (integer) 1754846600
```

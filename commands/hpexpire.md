This command works exactly like [`HEXPIRE`](hexpire.md) but the time to live of the field(s) is
specified in milliseconds instead of seconds.
Note, that providing a millisecond time of '0' will cause immediate expiration and reclamation of the field(s).

## Options

The `HPEXPIRE` command supports a set of options that modify its behavior:

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
127.0.0.1:6379> HPEXPIRE myhash 10000 FIELDS 2 f2 f3
1) (integer) 1
2) (integer) 1
127.0.0.1:6379> HPTTL myhash FIELDS 3 f1 f2 f3
1) (integer) -1
2) (integer) 9597
3) (integer) 9597
```

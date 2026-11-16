Like [`HTTL`](httl.md) this command returns the remaining time to live of hash field(s) that has an associated expiration time,
with the sole difference that `HTTL` returns the amount of remaining
time in seconds while `HPTTL` returns it in milliseconds.

See also the [`HTTL`](httl.md) command that returns the same information with seconds resolution.

## Reply

Array of values associated with the result of getting the remaining time-to-live of the specific fields, in the same order as they are requested.

* -2: Field does not exist in the provided hash key, or the hash key is empty.
* -1: Field exists in the provided hash key, but has no expiration associated with it.
* Integer: The expiration time associated with the hash key field, in milliseconds.

## Examples

```
127.0.0.1:6379> HSET myhash f1 v1 f2 v2 f3 v3
(integer) 3
27.0.0.1:6379> HPEXPIRE myhash 10000 FIELDS 2 f2 f3
1) (integer) 1
2) (integer) 1
127.0.0.1:6379> HPTTL myhash FIELDS 3 f1 f2 f3
1) (integer) -1
2) (integer) 9597
3) (integer) 9597
```

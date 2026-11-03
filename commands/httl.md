The `HTTL` command returns the remaining time to live of hash field(s) with associated expiration time(s).
This introspection capability allows a Valkey client to check how many seconds a
given hash field will continue to be part of the hash object.

See also the [`HPTTL`](hpttl.md) command that returns the same information with milliseconds resolution.

## Reply

Array of values associated with the result of getting the remaining time-to-live of the specific fields, in the same order as they are requested.

* -2: Field does not exist in the provided hash key, or the hash key is empty.
* -1: Field exists in the provided hash key, but has no expiration associated with it.
* Integer: The expiration time associated with the hash key field, in seconds.

## Examples

```
127.0.0.1:6379> HSET myhash f1 v1 f2 v2 f3 v3
(integer) 3
27.0.0.1:6379> HEXPIRE myhash 10 FIELDS 2 f2 f3
1) (integer) 1
2) (integer) 1
127.0.0.1:6379> HTTL myhash FIELDS 4 f1 f2 f3 non-exist
1) (integer) -1
2) (integer) 8
3) (integer) 8
4) (integer) -2
```

The `HTTL` command returns the remaining time to live of a hash field that has an associated expiration time.
This introspection capability allows a Valkey client to check how many seconds a
given hash field will continue to be part of the hash object.

## Synopsis

```
HTTL key FIELDS numfields field [field ...]
```

The command can also return the following values:

* The command returns `-2` if the specified field does not exist in the hash.
* The command returns `-1` if the specified field exists in the hash but has no associated expiration time.

See also the [`HPTTL`](hpttl.md) command that returns the same information with milliseconds resolution.

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

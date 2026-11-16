The `HPEXPIRETIME` command returns the absolute Unix timestamp (since January 1, 1970) in milliseconds at which the given hash field(s) will expire.

See also the [`HEXPIRETIME`](hexpiretime.md) command which returns the same information with seconds resolution.

## Reply

Array of values associated with the result of getting the absolute expiry timestamp of the specific fields, in the same order as they are requested.

* -2: Field does not exist in the provided hash key, or the hash key is empty.
* -1: Field exists in the provided hash key, but has no expiration associated with it.
* Integer: The expiration time associated with the hash key field, in milliseconds.

## Examples

```
127.0.0.1:6379> HSET myhash f1 v1 f2 v2 f3 v3
(integer) 3
27.0.0.1:6379> HPEXPIREAT myhash 1754847944000 FIELDS 2 f2 f3
1) (integer) 1
2) (integer) 1
127.0.0.1:6379> HPEXPIRETIME myhash FIELDS 4 f1 f2 f3 non-exist
1) (integer) -1
2) (integer) 1754847944000
3) (integer) 1754847944000
4) (integer) -2
```

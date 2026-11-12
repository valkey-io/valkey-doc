Returns the values of the requested fields at the exact `path` in a [Path Hash](../topics/path-hashes.md).
For multiple paths, use [`PHMGET`](phmget.md).
To retrieve every field at one path, use [`PHGETALL`](phgetall.md).

## Reply

Array in RESP2 and RESP3, with one entry per requested field in the same order.
Each entry is a string, or null if the field, path, or key does not exist.
The reply is an array even when only one field is requested.

## Examples

```
> PHSET tree app FIELDS 1 host local
OK
> PHGET tree app host port
1) "local"
2) (nil)
```

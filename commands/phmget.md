Returns field values from one or more exact paths in a [Path Hash](../topics/path-hashes.md).
Each group consists of a path followed by `FIELDS`, a positive field count, and that many field names.

## Reply

Flat array in RESP2 and RESP3, in the order of the path groups and then of the fields within each group.
Each entry is a string, or null if the corresponding field, path, or key does not exist.

## Examples

```
> PHMSET tree app FIELDS 1 host local app/api FIELDS 1 host api
OK
> PHMGET tree app FIELDS 2 host port app/api FIELDS 1 host
1) "local"
2) (nil)
3) "api"
```

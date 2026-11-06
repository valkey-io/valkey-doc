Atomically sets fields at one or more exact paths in a [Path Hash](../topics/path-hashes.md).
Each group consists of a path followed by `FIELDS`, a positive pair count, and that many field-value pairs.
The entire argument list is validated before any writes are applied.
The command creates missing keys and paths as needed.
If a field at the same path appears more than once, the last assignment wins.

For a conditional write at one path, see [`PHSET`](phset.md).

## Reply

`OK` in RESP2 and RESP3.

## Examples

```
> PHMSET tree app FIELDS 2 host local port 8080 app/api FIELDS 1 host api
OK
> PHMGET tree app FIELDS 2 host port app/api FIELDS 1 host
1) "local"
2) "8080"
3) "api"
```

Checks whether the exact `path` has a field map in a [Path Hash](../topics/path-hashes.md).
A path that is only a prefix of a stored path does not count as a match.
Use [`PHPATHCOUNT`](phpathcount.md) with `PREFIX` to count paths below a prefix.

## Reply

Integer in RESP2 and RESP3: `1` if the exact path exists, or `0` if the key or path does not exist.

## Examples

```
> PHSET tree app/api FIELDS 1 host api
OK
> PHPATHEXISTS tree app
(integer) 0
> PHPATHEXISTS tree app/api
(integer) 1
```

Deletes the exact `path` and its fields in a [Path Hash](../topics/path-hashes.md).
With `WITHSUBPATHS`, it also deletes every stored path that starts with the given bytes, even if the exact path is absent.
An empty path with `WITHSUBPATHS` matches the entire Path Hash.
Deleting the last stored path removes the key.

Use [`PHDEL`](phdel.md) to remove individual fields.

## Reply

Integer in RESP2 and RESP3: the number of paths removed, or `0` if the key does not exist or no paths match.

## Examples

```
> PHMSET tree app FIELDS 1 host local app/api FIELDS 1 host api
OK
> PHPATHDEL tree app
(integer) 1
> PHPATHEXISTS tree app/api
(integer) 1
> PHPATHDEL tree app WITHSUBPATHS
(integer) 1
> EXISTS tree
(integer) 0
```

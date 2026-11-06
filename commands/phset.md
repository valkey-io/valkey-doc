Sets one or more field-value pairs at the exact `path` in a [Path Hash](../topics/path-hashes.md).
The `FIELDS` count must be positive and match the number of pairs supplied.
A successful write creates the key or path if needed and overwrites existing values.
If a field is supplied more than once, the last value wins.

The optional conditions are mutually exclusive:

* `FNX`: write only if none of the specified fields exist at the path.
* `FXX`: write only if all of the specified fields exist at the path.

The condition is evaluated for the entire group before any field is written.
If it fails, no fields are changed and no key or path is created.

## Reply

One of the following in RESP2 and RESP3:

* `OK`: the fields were written.
* Null: the condition was not met.

## Examples

```
> PHSET tree app FNX FIELDS 2 host local port 8080
OK
> PHSET tree app FNX FIELDS 2 host remote region eu
(nil)
> PHSET tree app FXX FIELDS 1 port 9090
OK
> PHGET tree app host port region
1) "local"
2) "9090"
3) (nil)
```

Returns all field-value pairs at the exact `path` in a [Path Hash](../topics/path-hashes.md).
Field order is unspecified.

## Reply

* RESP2: flat array of alternating field names and values, or an empty array if the key or path does not exist.
* RESP3: map of field names to values, or an empty map if the key or path does not exist.

## Examples

```
> PHSET tree app FIELDS 1 host local
OK
> PHGETALL tree app
1) "host"
2) "local"
```

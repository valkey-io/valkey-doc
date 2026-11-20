Returns all field-value pairs at the exact `path`.
Field order is unspecified.

## Reply

Map of field names to values, or an empty map if the key or path does not exist.

## Examples

```
> PHSET tree app FIELDS 1 host local
OK
> PHGETALL tree app
1) "host"
2) "local"
```

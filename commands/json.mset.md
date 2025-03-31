Set JSON values for multiple keys. The operation is atomic. Either all values are set or none is set.


## Syntax

```bash
JSON.MSET <key> <path> <value> [key <path> <value> ...]
```

* key - required, one or more Redis keys of document type
* path - required, a JSON path to set the value at
* value - required, a JSON value to set at the specified path

## Return

* Simple String 'OK' if the operation was successful
* Error on failure

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.MSET k1 .address.street '{"street": "21 2nd Street"}' k2 .address.city '{"city": "New York"}'
OK
127.0.0.1:6379> JSON.GET k1 .address.street
"{\"street\":\"21 2nd Street\"}"
127.0.0.1:6379> JSON.GET k2 .address.city
"{\"city\":\"New York\"}"
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.MSET k1 .address.street '\"21 2nd Street\"' k2 .address.city '\"New York\"'
OK
127.0.0.1:6379> JSON.GET k1 .address.street
"\"21 2nd Street\""
127.0.0.1:6379> JSON.GET k2 .address.city
"\"New York\""
```

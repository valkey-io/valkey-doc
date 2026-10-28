Delete `key` based on condition.

## Options

* `IFEQ` *comparison-value* -- Delete the key only if the comparison value matches key's existing value. Error is returned if provided key or value is not string.
* `IFNE` *comparison-value* -- Delete the key only if the comparison value does not matches key's existing value. Error is returned if provided key or value is not string.

## Example

Delete the `key` if given value is equal to existing value.

```
127.0.0.1:6379> SET x 1
OK
127.0.0.1:6379> DELEX x IFEQ 1
(integer) 1
```

Delete the `key` if given value is not equal to existing value.

```
127.0.0.1:6379> SET x 1
OK
127.0.0.1:6379> DELEX x IFNE 2
(integer) 1
```


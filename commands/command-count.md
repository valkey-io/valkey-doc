Returns the total number of commands in this Valkey server.

## Reply

Integer: the number of commands returned by `COMMAND`.

## Examples

```
127.0.0.1:6379> COMMAND COUNT
(integer) 241
```

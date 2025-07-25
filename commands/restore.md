Create a key associated with a value that is obtained by deserializing the
provided serialized value (obtained via [`DUMP`](dump.md)).

If `ttl` is 0 the key is created without any expire, otherwise the specified
expire time (in milliseconds) is set.

If the `ABSTTL` modifier was used, `ttl` should represent an absolute
[Unix timestamp][hewowu] (in milliseconds) in which the key will expire.

[hewowu]: http://en.wikipedia.org/wiki/Unix_time

For eviction purposes, you may use the `IDLETIME` or `FREQ` modifiers. See
[`OBJECT`](object.md) for more information.

`RESTORE` will return a "Target key name is busy" error when `key` already
exists unless you use the `REPLACE` modifier.

`RESTORE` checks the RDB version and data checksum.
If they don't match an error is returned.

## Examples

```
127.0.0.1:6379> DEL mykey
(integer) 0
127.0.0.1:6379> RESTORE mykey 0 "\n\x17\x17\x00\x00\x00\x12\x00\x00\x00\x03\x00\
                        x00\xc0\x01\x00\x04\xc0\x02\x00\x04\xc0\x03\x00\
                        xff\x04\x00u#<\xc0;.\xe9\xdd"
OK
127.0.0.1:6379> TYPE mykey
list
127.0.0.1:6379> LRANGE mykey 0 -1
1) "1"
2) "2"
3) "3"
```

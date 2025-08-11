The `HGETEX` command get the value of one or more fields of a given hash key, and optionally manipulates their expiration time.
The command will return an array in the size of the number of requested fields.
Without providing any optional flags, this command behaves exactly like a normal [`HMGET`](hmget.md) command.

## Options

The `HGETEX` command supports a set of options that modify its behavior:

* EX seconds — Set the specified expiration time, in seconds.
* PX milliseconds — Set the specified expiration time, in milliseconds.
* EXAT `unix-time-seconds` — Set the specified Unix time at which the fields will expire, in seconds.
* PXAT `unix-time-milliseconds` — Set the specified Unix time at which the fields will expire, in milliseconds.
* PERSIST — Remove the expiration time associated with the fields.

Note for the following:

1. The EX, PX, EXAT, PXAT, and PERSIST options are mutually exclusive.
2. Providing '0' expiration TTL via `EX` or `PX` optional arguments will result in the specified fields to immediately expire and removed from the hash.
3. Providing past expiration time via `EXAT` or `PXAT` optional arguments will result in the specified fields to immediately expire and removed from the hash.

## Notifications

`hexpire` keyspace event will be issued once in case in case at least 1 field has been set with an expiration time which is in the future.
`hexpired` keyspace event will be issued once in case at least 1 field has been set with an expiration time which is zero or in the past.
`hpersist` keyspace event will be issued once in case the `PERSIST` option was specified and at least 1 field's expiration time was removed.
`del` keyspace event will be issued once in case all the specified fields have been set with an expiration time which is zero or in the past, 
  and there are no more fields in the hash object.

## Examples

```
127.0.0.1:6379> HSET myhash f1 v1 f2 v2 f3 v3
(integer) 3
27.0.0.1:6379> HGETEX myhash EX 10 FIELDS 2 f2 f3
1) "v2"
2) "v3"
127.0.0.1:6379> HTTL myhash FIELDS 3 f1 f2 f3
1) (integer) -1
2) (integer) 8
3) (integer) 8
127.0.0.1:6379> HGETEX myhash EX 0 FIELDS 3 f1 f2 f3 
1) "v1"
2) "v2"
3) "v3"
127.0.0.1:6379> HGETEX myhash FIELDS 3 f1 f2 f3 
1) "nil"
2) "nil"
3) "nil"
```

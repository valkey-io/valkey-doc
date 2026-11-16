Remove the existing timeout on `key`, turning the key from _volatile_ (a key
with an expire set) to _persistent_ (a key that will never expire as no timeout
is associated).

## Reply

One of the following:

* Integer: `0` if _key_ does not exist or does not have an associated timeout.
* Integer: `1` if the timeout has been removed.

## Examples

```
127.0.0.1:6379> SET mykey "Hello"
OK
127.0.0.1:6379> EXPIRE mykey 10
(integer) 1
127.0.0.1:6379> TTL mykey
(integer) 10
127.0.0.1:6379> PERSIST mykey
(integer) 1
127.0.0.1:6379> TTL mykey
(integer) -1
```

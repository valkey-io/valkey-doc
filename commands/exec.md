Executes all previously queued commands in a [transaction][tt] and restores the
connection state to normal.

[tt]: ../topics/transactions.md

When using `WATCH`, `EXEC` will execute commands only if the watched keys were
not modified, allowing for a [check-and-set mechanism][ttc].

[ttc]: ../topics/transactions.md#cas

## Options

`EXEC` accepts conditions that are checked before the queued commands run, providing [optimistic locking][ttcond] without `WATCH`:

[ttcond]: ../topics/transactions.md#exec-conditions

* `IFEQ` *key* *value* -- Execute only if *key* holds a string equal to *value*.
* `IFNE` *key* *value* -- Execute only if *key* does not exist, or holds a string different from *value*.
* `NX` *key* -- Execute only if *key* does not exist.
* `XX` *key* -- Execute only if *key* exists.

When multiple conditions are given, all of them must match.
If any condition does not match, the transaction is discarded and `EXEC` returns a Null reply.

The transaction is discarded and `EXEC` returns an `EXECABORT` error if `IFEQ` or `IFNE` is used on a key that does not hold a string, if the conditions are malformed, or if the user has no read permission on a condition key.
In cluster mode, condition keys must be in the same hash slot as the keys of the queued commands.

If a `WATCH`ed key was modified, `EXEC` returns a Null reply without evaluating the conditions.

## Reply

One of the following:

* Array: each element being the reply to each of the commands in the atomic transaction.
* Null: the transaction was aborted because a `WATCH`ed key was touched or a condition did not match.

## Examples

```
127.0.0.1:6379> SET version 1
OK
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379(TX)> SET version 2
QUEUED
127.0.0.1:6379(TX)> SET data "new data"
QUEUED
127.0.0.1:6379(TX)> EXEC IFEQ version 1
1) OK
2) OK
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379(TX)> SET version 2
QUEUED
127.0.0.1:6379(TX)> EXEC IFEQ version 1
(nil)
```

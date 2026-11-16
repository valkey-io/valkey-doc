Executes all previously queued commands in a [transaction][tt] and restores the
connection state to normal.

[tt]: ../topics/transactions.md

When using `WATCH`, `EXEC` will execute commands only if the watched keys were
not modified, allowing for a [check-and-set mechanism][ttc].

[ttc]: ../topics/transactions.md#cas

## Reply

One of the following:

* Array: each element being the reply to each of the commands in the atomic transaction.
* Null: the transaction was aborted because a `WATCH`ed key was touched.

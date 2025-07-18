`BLMOVE` is the blocking variant of [`LMOVE`](lmove.md).
When `source` contains elements, this command behaves exactly like `LMOVE`.
When used inside a [`MULTI`](multi.md)/[`EXEC`](exec.md) block, this command behaves exactly like `LMOVE`.
When `source` is empty, Valkey will block the connection until another client
pushes to it or until `timeout` (a double value specifying the maximum number of seconds to block) is reached.
A `timeout` of zero can be used to block indefinitely.

This command comes in place of the now deprecated [`BRPOPLPUSH`](brpoplpush.md). Doing
`BLMOVE RIGHT LEFT` is equivalent.

See [`LMOVE`](lmove.md) for more information.

## Pattern: Reliable queue

Please see the pattern description in the `LMOVE` documentation.

## Pattern: Circular list

Please see the pattern description in the `LMOVE` documentation.

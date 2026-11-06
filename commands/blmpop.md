`BLMPOP` is the blocking variant of [`LMPOP`](lmpop.md).

When any of the lists contains elements, this command behaves exactly like `LMPOP`.
When used inside a [`MULTI`](multi.md)/[`EXEC`](exec.md) block, this command behaves exactly like `LMPOP`.
When all lists are empty, Valkey will block the connection until another client pushes to it or until the `timeout` (a double value specifying the maximum number of seconds to block) elapses.
A `timeout` of zero can be used to block indefinitely.

See [`LMPOP`](lmpop.md) for more information.

## Reply

One of the following:

* Null: when no element could be popped and the _timeout_ is reached.
* Two-element array with the first element being the name of the key from which elements were popped, and the second element being an array of the popped elements.

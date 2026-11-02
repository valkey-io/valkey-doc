See [`SCAN`](scan.md)  for `ZSCAN` documentation.

## Reply

Two-element array.

* The first element is a string that represents an unsigned 64-bit number, the cursor.
* The second element is an array of member/score pairs that were scanned. When `NOSCORES` option is on, a list of members from the sorted set.

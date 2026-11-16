See [`SCAN`](scan.md) for `HSCAN` documentation.

## Reply

Two-element array.

* The first element is a string that represents an unsigned 64-bit number, the cursor.
* The second element is an array of field/value pairs that were scanned. When `NOVALUES` option is on, a list of keys from the hash.

Incrementally scans field-value pairs at the exact `path` in a [Path Hash](../topics/path-hashes.md).
`MATCH` filters field names using a glob pattern.
`COUNT` is a positive work hint and defaults to 10.
A call may return more or fewer pairs than requested, or an empty page with a nonzero cursor.
Field order is unspecified.

Start with cursor `0` and continue with the returned cursor using the same key and path until the cursor is `0` again.
The cursor and iteration behavior follow [`HSCAN`](hscan.md).
Use [`PHPATHSCAN`](phpathscan.md) to iterate over path names.

## Reply

Two-element array in RESP2 and RESP3:

* String: the next cursor as an unsigned 64-bit number, or `"0"` when the scan is complete.
* Array of strings: alternating field names and values.

A missing key or path returns cursor `"0"` and an empty array.

## Examples

```
> PHSET tree app FIELDS 2 host local port 8080
OK
> PHSCAN tree app 0 MATCH h*
1) "0"
2) 1) "host"
   2) "local"
```

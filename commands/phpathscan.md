Incrementally lists stored paths in a [Path Hash](../topics/path-hashes.md) in byte lexicographic order.
Use `PREFIX` to restrict results to paths starting with the given bytes.
An empty prefix matches all paths.
`COUNT` is a positive maximum number of paths to return per call and defaults to 10.

Start with cursor `0` and pass the returned cursor unchanged to the next call, using the same key and prefix.
A returned cursor of `0` means the scan is complete.
Each page resumes strictly after the last path returned, even if that path has been deleted.
The scan is not a snapshot.
For example, paths inserted at or before the current position are not visited during that scan.

Use [`PHSCAN`](phscan.md) to iterate over the fields at one exact path.

## Reply

Two-element array in RESP2 and RESP3:

* String: the next opaque cursor, or `"0"` when the scan is complete.
* Array of strings: the paths returned on this page.

A missing key or no matching paths on the page returns cursor `"0"` and an empty array.

## Examples

```
> PHMSET tree app FIELDS 1 host local app/api FIELDS 1 host api
OK
> PHPATHSCAN tree 0 PREFIX app COUNT 1
1) "1:617070"
2) 1) "app"
> PHPATHSCAN tree 1:617070 PREFIX app COUNT 1
1) "0"
2) 1) "app/api"
```

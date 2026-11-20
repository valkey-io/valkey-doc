Incrementally lists stored paths in byte lexicographic order.
This order is independent of `hash-seed`.
Use `PREFIX` to restrict results to paths starting with the given bytes.
An empty prefix matches all paths.
`COUNT` is a positive maximum number of paths to return per call and defaults to 10.
The [`SCAN` family](scan.md#number-of-elements-returned-at-every-scan-call) uses `COUNT` as a work hint.

Start with cursor `0` and pass the returned cursor unchanged to the next call, using the same key and prefix.
A returned cursor of `0` means the scan is complete.
The scan is not a snapshot, and its guarantees differ from the [`SCAN` guarantees](scan.md#scan-guarantees):

* Each page resumes strictly after the last path returned, even if that path has been deleted.
  A full iteration returns a given path name at most once.
* Paths inserted at or before the current position are skipped.
  Matching paths inserted after the current position can be returned by a later call.

Use [`PHSCAN`](phscan.md) to iterate over the fields at one exact path.

## Reply

Two-element array with the following elements:

* String: the next opaque cursor, or `"0"` when the scan is complete.
* Array of strings: the paths returned on this page.

A missing key or no matching paths on the page returns cursor `"0"` and an empty array.

## Examples

The second page resumes after `app/api` even though that path was deleted.
It includes the new path `app/db` and skips `app`, which sorts before the cursor.

```
> PHMSET tree app/api FIELDS 1 host api app/web FIELDS 1 host web
OK
> PHPATHSCAN tree 0 PREFIX app COUNT 1
1) "1:6170702f617069"
2) 1) "app/api"
> PHPATHDEL tree app/api
(integer) 1
> PHMSET tree app FIELDS 1 host local app/db FIELDS 1 host db
OK
> PHPATHSCAN tree 1:6170702f617069 PREFIX app COUNT 2
1) "0"
2) 1) "app/db"
   2) "app/web"
```

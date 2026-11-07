Finds stored paths in a [Path Hash](../topics/path-hashes.md) that are byte prefixes of `query`, ordered from longest to shortest.
An exact match is included by default.
If stored, the empty path matches every query.

* `LENGTHS` returns the length in bytes of each match instead of the path bytes.
* `WITHVALUES` includes all field-value pairs for each match.
* `FIELDS numfields field [field ...]` includes the values of the selected fields for each match.
  The count must be positive and match the number of field names.
  This option is mutually exclusive with `WITHVALUES`.
* `COUNT count` returns at most that many of the longest matches.
  The count must be positive.
* `MAXPATHLEN max-path-bytes` excludes paths longer than the given byte length before applying `COUNT`.
  The length must be zero or greater.
* `EXCLUDESELF` excludes a stored path equal to the query.
  Pass the shortest match from one page as the query on the next call with `EXCLUDESELF` to continue toward shorter ancestors.

Use [`PHPATHSCAN`](phpathscan.md) with `PREFIX` to enumerate stored paths that start with a given prefix.

## Reply

Array in RESP2 and RESP3, empty if the key does not exist or no paths match.
By default each entry is a path string, or an integer byte length when `LENGTHS` is used.
With `WITHVALUES` or `FIELDS`, each entry is a two-element array containing the path (or length) followed by:

* With `WITHVALUES`: a map of field-value pairs in RESP3, or a flat array of alternating field names and values in RESP2.
  Field order is unspecified.
* With `FIELDS`: an array of values in the requested field order in both protocols, with null for each missing field.

## Examples

```
> PHMSET tree app FIELDS 1 host local app/api FIELDS 1 host api
OK
> PHPREFIXES tree app/api/v1
1) "app/api"
2) "app"
> PHPREFIXES tree app/api EXCLUDESELF LENGTHS FIELDS 2 host port
1) 1) (integer) 3
   2) 1) "local"
      2) (nil)
> PHPREFIXES tree app/api/v1 COUNT 1
1) "app/api"
```

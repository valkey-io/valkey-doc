Counts the stored paths in a [Path Hash](../topics/path-hashes.md).
With `PREFIX`, it counts all paths that start with the specified bytes, including the exact path if it exists.
An omitted or empty prefix counts the whole Path Hash in constant time.
A nonempty prefix requires traversing the matching paths.

## Reply

Integer in RESP2 and RESP3: the number of matching paths, or `0` if the key does not exist or no paths match.

## Examples

```
> PHMSET tree app FIELDS 1 host local app/api FIELDS 1 host api docs FIELDS 1 host static
OK
> PHPATHCOUNT tree
(integer) 3
> PHPATHCOUNT tree PREFIX app
(integer) 2
```

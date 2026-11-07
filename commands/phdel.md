Deletes the specified fields at the exact `path` in a [Path Hash](../topics/path-hashes.md).
Missing fields are ignored.
If no fields are specified, the command deletes the whole path and its field map.
Deleting the last field removes the path.
In either form, deleting the last path also removes the key.

To delete an exact path or a whole subtree, see [`PHPATHDEL`](phpathdel.md).

## Reply

Integer in RESP2 and RESP3.
With field arguments, the reply is the number of fields removed.
Without field arguments, it is `1` if the path was removed or `0` otherwise.
A missing key or path returns `0` in both forms.

## Examples

```
> PHSET tree app FIELDS 2 host local port 8080
OK
> PHDEL tree app host missing
(integer) 1
> PHDEL tree app
(integer) 1
> EXISTS tree
(integer) 0
```

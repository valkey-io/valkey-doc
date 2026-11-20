Returns field values from one or more exact paths.
Each group consists of a path followed by `FIELDS`, a positive field count, and that many field names.

## Reply

Flat array with one element per requested field, in the order of the path groups and then of the fields within each group.
Each element is the field's value as a string, or null if the field or its path does not exist.
If the key does not exist, all elements are null and the array length still equals the total number of requested fields.

## Examples

```
> PHMSET tree app FIELDS 1 host local app/api FIELDS 1 host api
OK
> PHMGET tree app FIELDS 2 host port app/api FIELDS 1 host
1) "local"
2) (nil)
3) "api"
> PHMGET missing app FIELDS 2 host port app/api FIELDS 1 host
1) (nil)
2) (nil)
3) (nil)
```

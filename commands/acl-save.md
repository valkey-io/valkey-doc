When Valkey is configured to use an ACL file (with the `aclfile` configuration
option), this command will save the currently defined ACLs from the server memory to the ACL file.

## Examples

```
> ACL SAVE
+OK

> ACL SAVE
-ERR There was an error trying to save the ACLs. Please check the server logs for more information
```

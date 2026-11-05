When Valkey is configured to use an ACL file (with the `aclfile` configuration
option), this command will save the currently defined ACLs from the server memory to the ACL file.

## Reply

`OK`.

The command may fail with an error for several reasons: if the file cannot be written or if the server is not configured to use an external ACL file.

## Examples

```
127.0.0.1:6379> ACL SAVE
OK
127.0.0.1:6379> ACL SAVE
(error) ERR There was an error trying to save the ACLs. Please check the server logs for more information
```

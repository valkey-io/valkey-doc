Delete all the specified ACL roles.
A role cannot be deleted while it is assigned to a user: if any of the specified roles is still held by a user, the command returns an error and no role is deleted.
Use the `resetroles` or `role=` rules of [`ACL SETUSER`](acl-setuser.md) to remove the role from its users first.
The users holding a role are listed by [`ACL GETROLE`](acl-getrole.md).

The list of roles may include role names that do not exist, in such case no operation is performed for the non existing roles.

## Examples

```
127.0.0.1:6379> ACL DELROLE reader
(error) ERR Role 'reader' is assigned to one or more users. Remove it from them first.
127.0.0.1:6379> ACL SETUSER alice resetroles
OK
127.0.0.1:6379> ACL DELROLE reader nosuchrole
(integer) 1
```

This command deletes one or more ACL roles.

`ACL DELROLE` fails if any of the given roles is still assigned to a user. In that case, no roles are deleted, including other valid names in the same call. Remove the role from all users first.

It returns the number of roles deleted. Deleting an unknown role name counts as zero.

## Examples

In this example, a role is deleted:

```
127.0.0.1:6379> ACL DELROLE sample
(integer) 1
```

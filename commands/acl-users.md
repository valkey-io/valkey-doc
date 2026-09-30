The command shows a list of all the usernames of the currently configured
users in the Valkey ACL system. Roles are not included, use
[`ACL ROLES`](acl-roles.md) to list them.

## Examples

```
127.0.0.1:6379> ACL USERS
1) "anna"
2) "antirez"
3) "default"
```

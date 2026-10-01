This command creates and modifies an ACL role and its rules.

If the role does not exist, `ACL SETROLE` creates it. If the role exists, the rules you provide are added to its current rules. The whole set of rules is applied atomically: if any rule is invalid, none of them are applied.

Roles get `alldbs` by default, the same as new users.

Roles do not support user-only rules such as `on`, `off`, `nopass`, `resetpass`, `reset`, `>password`, or `role=`. Use these only with [`ACL SETUSER`](acl-setuser.md).

## Examples

In this example, the role can run only `GET` and `SET ~key2`:

```
127.0.0.1:6379> ACL SETROLE sample +GET allkeys &* (+SET ~key2)
OK
```

Rules added in a later call build on the existing rules:

```
127.0.0.1:6379> ACL SETROLE sample +DEL
OK
127.0.0.1:6379> ACL GETROLE sample
 1) "commands"
 2) "-@all +get +set +del"
 ...
```

See [`ACL GETROLE`](acl-getrole.md) to inspect a role's current rules, and [`ACL SETUSER`](acl-setuser.md) for assigning roles to users with `role=`.

Create an ACL role with the specified rules or modify the rules of an existing role.

A role is a named, reusable set of permissions that can be assigned to any number of users with the `role=` rule of [`ACL SETUSER`](acl-setuser.md), so a policy is written once instead of being repeated in every user.
See [roles](../topics/acl.md#roles) for more information.

If the role does not exist, the command creates it without any privilege.
It then reads from left to right all the rules provided as successive arguments, setting the role ACL rules as specified.
If the role already exists, the provided ACL rules are applied *in addition* to the rules already set, exactly as `ACL SETUSER` does for users.
The rules are applied atomically: if any rule is invalid, the role is left unchanged.

A role accepts the [command rules](acl-setuser.md#command-rules) of `ACL SETUSER`, as well as selectors (`(<rule list>)`) and `clearselectors`.
The rules that only make sense for a user are rejected with an error: `on`, `off`, `reset`, the password rules (`>`, `<`, `#`, `!`, `nopass`, `resetpass`), `role=` and `resetroles`.
Roles cannot be nested.

Changes to a role take effect immediately for every user holding it.
If the change removes access to Pub/Sub channels, the clients of those users that are subscribed to channels they can no longer access are disconnected.

Role names are case sensitive and may contain any printable ASCII character except for spaces, commas, quotes (`"` and `'`) and backslashes.
Roles live in a namespace of their own, so a role may have the same name as a user, a command, or a category.

Note: a new role starts with access to all databases (`alldbs`), and to all Pub/Sub channels if `acl-pubsub-default` is set to `allchannels`, just like a new user.
Since a user's own permissions and those of its roles are combined with OR logic, such a role grants those databases and channels to its users even if the user itself is restricted with `resetdbs`, `db=<id>` or `resetchannels`.
Use `db=<id>` (or `resetdbs`) and `resetchannels` in the role rules to restrict the role itself.
See [database permissions](../topics/acl.md#database-permissions).

## Examples

```
127.0.0.1:6379> ACL SETROLE reader ~app:* +@read
OK
127.0.0.1:6379> ACL SETROLE ops ~* +info (+config|get)
OK
127.0.0.1:6379> ACL SETROLE reader on
(error) ERR Error in ACL SETROLE modifier 'on': Syntax error
```

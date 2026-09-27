The command returns all the rules defined for an existing ACL user.

Specifically, it lists the user's ACL flags, password hashes, commands, key patterns, channel patterns (Added in version 6.2), selectors (Added in version 7.0) and databases (Added in version 9.1).
Additional information may be returned in the future if more metadata is added to the user.

Command rules are always returned in the same format as the one used in the [`ACL SETUSER`](acl-setuser.md) command.
Before version 7.0, keys and channels were returned as an array of patterns, however in version 7.0 later they are now also returned in same format as the one used in the `ACL SETUSER` command.
Note: This description of command rules reflects the user's effective permissions, so while it may not be identical to the set of rules used to configure the user, it is still functionally identical.

Selectors are listed in the order they were applied to the user, and include information about commands, key patterns, channel patterns, and database permissions.

## Examples

Here's an example configuration for a user

```
127.0.0.1:6379> ACL SETUSER sample on nopass +GET allkeys &* (+SET ~key2)
"OK"
127.0.0.1:6379> ACL GETUSER sample
1) "flags"
2) 1) "on"
   2) "nopass"
3) "passwords"
4) (empty array)
5) "commands"
6) "-@all +get"
7) "keys"
8) "~*"
9) "channels"
10) "&*"
11) "databases"
12) "alldbs"
13) "selectors"
14) 1) 1) "commands"
       2) "-@all +set"
       3) "keys"
       4) "~key2"
       5) "channels"
       6) ""
       7) "databases"
       8) "alldbs"
```

This command returns the ACL rules of an ACL role.

The reply contains the commands, key patterns, channel patterns, databases, and selectors of the role. It also lists the users that have the role assigned. The selectors are listed in the order they are applied.

The command returns a null reply if the role does not exist.

Command rules are always returned in the same format as the one used in the [`ACL SETROLE`](acl-setrole.md) command.

## Examples

In this example, the role can `GET` all keys, but it can `SET` only `key2`:

```
127.0.0.1:6379> ACL SETROLE sample +GET allkeys &* (+SET ~key2)
OK
127.0.0.1:6379> ACL SETUSER alice on nopass role=sample
OK
127.0.0.1:6379> ACL GETROLE sample
1) "commands"
2) "-@all +get"
3) "keys"
4) "~*"
5) "channels"
6) "&*"
7) "databases"
8) "alldbs"
9) "selectors"
10) 1) 1) "commands"
    2) "-@all +set"
    3) "keys"
    4) "~key2"
    5) "channels"
    6) ""
    7) "databases"
    8) "alldbs"
11) "users"
12) 1) "alice"
```

See [`ACL SETROLE`](acl-setrole.md) and [`ACL SETUSER`](acl-setuser.md) for the rule syntax.

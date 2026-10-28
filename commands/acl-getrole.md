The command returns all the rules defined for an existing ACL role, and the users that hold it.
The command returns a null reply if the role does not exist.

Specifically, it lists the role's commands, key patterns, channel patterns, databases and selectors, with rules returned in the same format as the one used in the [`ACL SETROLE`](acl-setrole.md) command, followed by the names of the users the role is assigned to.

## Examples

```
127.0.0.1:6379> ACL SETROLE reader ~app:* +@read (+info)
OK
127.0.0.1:6379> ACL SETUSER alice on >alicepass role=reader
OK
127.0.0.1:6379> ACL GETROLE reader
 1) "commands"
 2) "-@all +@read"
 3) "keys"
 4) "~app:*"
 5) "channels"
 6) ""
 7) "databases"
 8) "alldbs"
 9) "selectors"
10) 1)  1) "commands"
        2) "-@all +info"
        3) "keys"
        4) ""
        5) "channels"
        6) ""
        7) "databases"
        8) "alldbs"
11) "users"
12) 1) "alice"
127.0.0.1:6379> ACL GETROLE nosuchrole
(nil)
```

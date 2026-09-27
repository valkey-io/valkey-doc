Return a fingerprint of the ACL rules currently in effect, as a hexadecimal string.
The digest depends only on the rules in effect and not on the order the users were
created in, so two servers configured alike report the same digest.

The digest covers everything [`ACL LIST`](acl-list.md) reports: the user names, their
flags, their password hashes, and their command, key and channel rules.
Any change to any user changes the digest.
The reply is the same size however many users are configured.

This is meant for confirming which revision of an ACL a server is running.
A client that manages users through an ACL file can read the digest before and after an
[`ACL LOAD`](acl-load.md) to tell whether the file it wrote is the one now in effect.
Comparing the rules themselves is impractical, because the server reports them in its
own normalized form rather than the form they were written in, so a client would need its
own copy of the rule parser to compare them.

## Examples

```
127.0.0.1:6379> ACL DIGEST
"24ece0a4daea0bcb936b438ae6c9f36db76f57dfc70e00def7b2c26041c49822"
127.0.0.1:6379> ACL SETUSER alice on >alice ~key:* +get
OK
127.0.0.1:6379> ACL DIGEST
"d06ec40dd1a8e30a4babea1011d4b0daf02dbdf5de95ea18768e15f346a7d385"
127.0.0.1:6379> ACL DELUSER alice
(integer) 1
127.0.0.1:6379> ACL DIGEST
"24ece0a4daea0bcb936b438ae6c9f36db76f57dfc70e00def7b2c26041c49822"
```

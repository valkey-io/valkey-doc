Return a fingerprint of the ACL rules currently in effect, as a hexadecimal string.
The digest depends only on the rules in effect and not on the order the users and roles
were created in, so two servers configured alike report the same digest.

The digest covers everything [`ACL LIST`](acl-list.md) reports: the user names, their
flags, their password hashes, and their command, key and channel rules, and the
[roles](../topics/acl.md#roles) with their rules.
Any change to any user or role changes the digest.
Changing a role's rules with [`ACL SETROLE`](acl-setrole.md) changes it too, even though
the lines of the users that hold the role stay the same.
The reply is the same size however many users and roles are configured.

This is meant for confirming which revision of an ACL a server is running.
A client that manages users through an ACL file can read the digest before and after an
[`ACL LOAD`](acl-load.md) to tell whether the file it wrote is the one now in effect.
Comparing the rules themselves is impractical, because the server reports them in its
own normalized form rather than the form they were written in, so a client would need its
own copy of the rule parser to compare them.

## Reply

String: the digest of the ACL rules currently in effect, as a hexadecimal string.

## Examples

```
127.0.0.1:6379> ACL DIGEST
"19566a9119379147926cb177af97ea4c8cc6cd5ef252ae6e6a0c587ae174e731"
127.0.0.1:6379> ACL SETUSER alice on >alice ~key:* +get
OK
127.0.0.1:6379> ACL DIGEST
"b7fe19e1064127c9739f0a9cb0efaac7a2e7e7e788ef2f9ff55bf68806ebd43b"
127.0.0.1:6379> ACL DELUSER alice
(integer) 1
127.0.0.1:6379> ACL DIGEST
"19566a9119379147926cb177af97ea4c8cc6cd5ef252ae6e6a0c587ae174e731"
```

Editing a role changes the digest, although the line of the user that holds it does not change:

```
127.0.0.1:6379> ACL SETROLE reader ~data:* +get
OK
127.0.0.1:6379> ACL SETUSER bob on >bob role=reader
OK
127.0.0.1:6379> ACL DIGEST
"fae16b1655b7c98804f3c98b6e7521bd425bc42dd7fedd8d2490d593609ece3f"
127.0.0.1:6379> ACL SETROLE reader +set
OK
127.0.0.1:6379> ACL DIGEST
"6ea056a39eb57b0bc9a85f0c640913946216f6b44563dba043ab489f81c9d47f"
```

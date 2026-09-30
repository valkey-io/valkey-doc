The command shows the currently active ACL rules in the Valkey server. Each
line in the returned array defines a different role or user. Lines starting
with `role` describe [roles](../topics/acl.md#roles) and are listed first,
followed by the lines starting with `user`. The format is the
same used in the valkey.conf file or the external ACL file, so you can
cut and paste what is returned by the ACL LIST command directly inside a
configuration file if you wish (but make sure to check [`ACL SAVE`](acl-save.md)).
Implicit defaults may be omitted: for example, access to all databases (`alldbs`)
is not shown, while explicit `db=<dbid>` and `resetdbs` rules are shown.

## Examples

```
127.0.0.1:6379> ACL LIST
1) "role reader ~app:* resetchannels -@all +@read"
2) "user alice on #13dc8554575637802eec3c0117f41591a990e1a2d37160018c48c9125063838a resetchannels -@all role=reader"
3) "user antirez on #9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 ~objects:* &* +@all -@admin -@dangerous"
4) "user default on nopass ~* &* +@all"
```

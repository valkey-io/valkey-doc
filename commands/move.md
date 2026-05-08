Move `key` from the currently selected database (see [`SELECT`](select.md)) to the specified
destination database.
When `key` already exists in the destination database, or it does not exist in
the source database, it does nothing.
It is possible to use `MOVE` as a locking primitive because of this.

The caller must have ACL permission to access the destination database. The
source database is the currently selected one, so the user already had to be
allowed to [`SELECT`](select.md) it. See
[database permissions](../topics/acl.md#database-permissions).

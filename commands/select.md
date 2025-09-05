Select the Valkey logical database having the specified zero-based numeric index.
New connections always use the database 0.

By default, Valkey provides 16 logical databases, indexed from `0` to `15`.
You can increase this number by setting the `databases` parameter in the configuration file.
This change must be made at startup and cannot be modified at runtime.

Selectable Valkey databases are a form of namespacing: all databases are still persisted in the same RDB / AOF file. However different databases can have keys with the same name, and commands like [`FLUSHDB`](flushdb.md), [`SWAPDB`](swapdb.md) or [`RANDOMKEY`](randomkey.md) work on specific databases.

In practical terms, Valkey databases should be used to separate different keys belonging to the same application (if needed), and not to use a single Valkey instance for multiple unrelated applications.

Valkey 9.0 and later supports multiple databases in cluster mode. You can use `SELECT <dbid>`  to switch between them.

Since the currently selected database is a property of the connection, clients should track the currently selected database and re-select it on reconnection.

While there is no dedicated command to query the currently selected database for a connection, you can infer it from the output of [`CLIENT LIST`](client-list.md) or [`CLIENT INFO`](client-info.md), where each client entry includes the `db=N` field indicating the selected database.

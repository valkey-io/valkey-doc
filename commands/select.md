Select the Valkey logical database having the specified zero-based numeric index.
New connections always use the database 0.

Selectable Valkey databases are a form of namespacing: all databases are still persisted in the same RDB / AOF file. However different databases can have keys with the same name, and commands like `FLUSHDB`, `SWAPDB` or `RANDOMKEY` work on specific databases.

In practical terms, Valkey databases should be used to separate different keys belonging to the same application (if needed), and not to use a single Valkey instance for multiple unrelated applications.

When using Valkey Cluster, the `SELECT` command cannot be used, since Valkey Cluster only supports database zero. In the case of a Valkey Cluster, having multiple databases would be useless and an unnecessary source of complexity. Commands operating atomically on a single database would not be possible with the Valkey Cluster design and goals.

Since the currently selected database is a property of the connection, clients should track the currently selected database and re-select it on reconnection. While there is no command in order to query the selected database in the current connection, the `CLIENT LIST` output shows, for each client, the currently selected database.

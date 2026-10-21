Initiates a replication stream from the primary.

The `PSYNC` command is called by Valkey replicas for initiating a replication
stream from the primary.

For more information about replication in Valkey please check the
[replication page][tr].

[tr]: ../topics/replication.md

## Reply

**Non-standard return value**, a bulk transfer of the data followed by `PING` and write requests from the primary.

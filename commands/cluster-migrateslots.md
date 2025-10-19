`CLUSTER MIGRATESLOTS` initiates an asynchronous migration of the designated
slot range(s) to the specified target node using
[atomic slot migration](../topics/atomic-slot-migration.md).

Multiple slot migrations may be specified through repeated `SLOTSRANGE` and
`NODE` pairs. `OK` is returned if all slot migrations are successfully
initiated, otherwise an error message is returned and no slot migrations are
initiated.

To check on the progress of the slot migration, use the
[`CLUSTER GETSLOTMIGRATIONS`](cluster-getslotmigrations.md) command.

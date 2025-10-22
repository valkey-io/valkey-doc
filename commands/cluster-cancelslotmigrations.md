`CLUSTER CANCELSLOTMIGRATIONS` cancels all in progress
[atomic slot migrations](../topics/atomic-slot-migration.md) initiated through
[`CLUSTER MIGRATESLOTS`](cluster-migrateslots.md).

Only slot migrations initiated on this node are cancelled. If this node is the
target of a slot migration, the cancellation must be performed on the source
node.

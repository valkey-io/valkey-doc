`CLUSTER MIGRATESLOTS` initiates an asynchronous migration of the designated
slot range(s) to the specified target node using
[atomic slot migration](../topics/atomic-slot-migration.md).

This command allows for many slot ranges in a single migration through repeated
start and end slot pairs within the `SLOTSRANGE` block. It also supports
multiple migrations in one command, through repeated `SLOTSRANGE` and `NODE`
blocks. For example:

```
CLUSTER MIGRATESLOTS SLOTSRANGE 0 9 20 29 NODE <target A> SLOTSRANGE 10 19 NODE <target B>
```

Initiates two slot migration jobs, one to `<target A>` with 20 slots (0-9
inclusive, 20-29 inclusive) and another to `<target B>` with 10 slots (10-19
inclusive).

`OK` is returned if all slot migrations are successfully initiated, otherwise an
error message is returned and no slot migrations are initiated.

To check on the progress of the slot migration, use the
[`CLUSTER GETSLOTMIGRATIONS`](cluster-getslotmigrations.md) command.

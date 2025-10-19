---
title: Atomic Slot Migration
description: Overview of atomic slot migration
---

To perform live resharding, Valkey uses a process known as slot migration.
During slot migration, one or more of the 16384 hash slots are moved from a
source node to a target node. Valkey 9.0 introduces a new option for migrating
hash slots known as Atomic Slot Migration.

## Background: The Existing Migration Process

Prior to Valkey 9.0, a slot migration from a source node to a target node was
performed through the following steps:

1. Send `<target>` `CLUSTER SETSLOT <slot> IMPORTING <source>`
2. Send `<source>` `CLUSTER SETSLOT <slot> MIGRATING <target>`
3. Send `<source>` `CLUSTER GETKEYSINSLOT <slot> <count>`
4. Send `<source>` `MIGRATE ...` for each key in the result of step 3
5. Repeat 3 & 4 until no keys are left in the slot on `<source>`
6. Send `<target>` `CLUSTER SETSLOT <slot> NODE <target>`
7. Send `<source>` `CLUSTER SETSLOT <slot> NODE <target>`

This was subject to the following problems:

- **Higher latency for client operations**: All client writes and reads to keys
  in the migrating hash slot were subject to `ASK` redirections, requiring
  re-execution of the command on the target node, effectively doubling client
  observed latency during the migration.
- **Multi-key operation unavailability**: Since there was no guarantee all keys
  in a multi-key operation were present on a single node, multi-key operations
  like [`MSET`](../commands/mset.md) or [`MGET`](../commands/mget.md) were
  subject to `TRYAGAIN` errors.
- **Problems with large keys/collections**: Since the migration was performed
  one key at a time, large keys (like a hash with many keys or a list with many
  elements) needed to be sent as a single command. Serialization of a large key
  required a large contiguous memory chunk on the source node and import of that
  payload required a large CPU burst on the target node. In some cases, the
  memory consumption is enough to trigger out-of-memory conditions on the source
  node, and the CPU burst is large enough to cause a failover on the target
  shard due to health probes not being served.
- **Slot migration latency**: The overall latency of the slot migration was
  bounded by how quickly the operator could send the `CLUSTER GETKEYSINSLOT` and
  `MIGRATE` commands. Each batch of keys required a full round-trip-time between
  the operator's machine and the cluster, leaving a lot of waiting time that
  could be used to do data migration.
- **Lack of resilience to failure**: If a failure condition was encountered, for
  example, the hash slot will not fit on the target node, undoing the slot
  migration is not well supported and requires replaying the listed steps in
  reverse. In some cases, the hash slot may have grown while the migration was
  underway, and may not fit on either the source or target node.

## Performing an Atomic Slot Migration using `CLUSTER MIGRATESLOTS`

Valkey 9.0 does not get rid of the existing slot migration option, but it does
introduce Atomic Slot Migration as a second option. To perform an Atomic Slot
Migration, an operator performs the following steps:

1. Send `<source>`
   `CLUSTER MIGRATESLOTS SLOTSRANGE <start-slot> <end-slot> NODE <target>`
2. Poll `<source>` for progress using `CLUSTER GETSLOTMIGRATIONS`

`CLUSTER MIGRATESLOTS` initiates a migration of the designated slot range to the
specified target node. The slot migration process is then performed
asynchronously.

The command also accepts many slot ranges, through repeated start and end slot
pairs, and even supports multiple migrations in one command, through repeated
`SLOTSRANGE` and `NODE` blocks. For example:

```
CLUSTER MIGRATESLOTS SLOTSRANGE 0 9 20 29 NODE <target A> SLOTSRANGE 10 19 NODE <target B>
```

Initiates two slot migration jobs, one to `<target A>` with 20 slots (0-9
inclusive, 20-29 inclusive) and another to `<target B>` with 10 slots (10-19
inclusive).

For more details on `CLUSTER MIGRATESLOTS` see the
[command documentation](../commands/cluster-migrateslots.md).

## Polling Atomic Slot Migrations

The `CLUSTER GETSLOTMIGRATIONS` command allows operators to poll the status of
their migration. `CLUSTER GETSLOTMIGRATIONS` can be executed on either the
source node or the target node. In progress migrations will always be shown, and
recently completed migrations will be visible up to a configurable threshold. In
the case of a failure, the slot migration will also include a short description
of the failure to allow for retry decisions.

For more details on `CLUSTER GETSLOTMIGRATIONS` see the
[command documentation](../commands/cluster-getslotmigrations.md).

## Canceling Atomic Slot Migrations

In the case a slot migration needs to be cancelled after the process is started,
Atomic Slot Migration provides the `CLUSTER CANCELSLOTMIGRATIONS` command to
cancel all active Atomic Slot Migrations for which that node is the source node.
This command can be sent to the whole cluster to cancel all slot migrations
everywhere.

For more details on `CLUSTER CANCELSLOTMIGRATIONS` see the
[command documentation](../commands/cluster-cancelslotmigrations.md).

## Behind the scenes of Atomic Slot Migration

Atomic Slot Migration utilizes a completely different process than
`CLUSTER SETSLOT`-based migrations:

1. Immediately after `CLUSTER MIGRATESLOTS` is received by the source node, it
   initiates a connection to the target node and performs authentication,
   similar to how a replication link is initialized.
2. Once established, the source node uses a new internal command -
   `CLUSTER SYNCSLOTS` - to inform the target of the migration.
3. The source node then forks a child process to do a one-time snapshot of the
   slot contents. The fork iterates all hash slots and serializes their contents
   over the slot migration link. The contents are subsequently replicated to any
   replicas of the target node.
4. While the child process is doing the snapshot, the parent process tracks all
   mutations performed on the migrating hash slots.
5. Once the child process snapshot finishes, the parent process sends all
   accumulated mutations. Any new mutations received during this step are also
   sent.
6. Once the amount of in-flight mutations goes below a configured threshold, the
   parent process freezes mutations temporarily to allow final synchronization
   of the hash slots.
7. Once the target node is completely caught up, it takes over the hash slots
   and broadcasts ownership to the cluster
8. When the source node finds out about the migration, it deletes the keys in
   the hash slot and unfreezes mutations. Clients will now get `MOVED`
   redirections to the target node, which now owns the hash slots. The slot
   migration is completed.

### Isolation of importing hash slots from clients

Since slot ownership is not moved until the very end of the migration, commands
targeting migrating hash slots on the target node will receive `MOVED`
redirections per the cluster specification. But there are some commands that
operate on the entire database:

1. `KEYS`/`SCAN`: These commands allow a client to list out all keys on a shard.
2. `DBSIZE`/`INFO`: These commands provide statistical information about how
   many keys are on a shard.
3. `FLUSHDB`/`FLUSHALL`: These commands allow a client to drop all data in a
   database, or on all databases, on a node.

To handle this, all importing hash slots are marked specially and hidden from
read operations on both the target primary and the target replica.

`FLUSHDB` and `FLUSHALL` present a special case where we fail the slot migration
when being executed on **both the source and target node**. It is expected that
operators would retry the migration after flushing, which should now succeed
almost instantly due to an empty database.

### Deep Dive on `CLUSTER SYNCSLOTS`

The `CLUSTER SYNCSLOTS` command is introduced as a new command for internal
communication between nodes. It implements various subcommands to allow the
navigation of the Atomic Slot Migration state machine:

- `CLUSTER SYNCSLOTS ESTABLISH SOURCE <source-node-id> NAME <unique-migration-name> SLOTSRANGE <start> <end> ...`:
  Inform a target node of an in progress slot migration and begin tracking the
  current connection as a slot migration link.
- `CLUSTER SYNCSLOTS SNAPSHOT-EOF`: Used as a marker to inform the target the
  full snapshot of the hash slot contents have been sent.
- `CLUSTER SYNCSLOTS REQUEST-PAUSE`: Inform a source node that the target has
  received all of the snapshot and is ready to proceed.
- `CLUSTER SYNCSLOTS PAUSED`: Used as a marker to inform the target no more
  mutations should occur as the source has paused mutations.
- `CLUSTER SYNCSLOTS REQUEST-FAILOVER`: Inform a source node that the target is
  fully caught up and ready to takeover the hash slots.
- `CLUSTER SYNCSLOTS FAILOVER-GRANTED`: Inform a target node that the source
  node is still paused and takeover can be safely performed.
- `CLUSTER SYNCSLOTS FINISH`: Inform a replica of the target node that a
  migration is completed (or failed).
- `CLUSTER SYNCSLOTS CAPA`: Reserved command allowing capability negotiation
  (for forwards and backwards compatibility).

```
     User                        Source                                          Target                         Target Replica
       |----CLUSTER MIGRATESLOTS--->|                                                |                                 |
       |                            |------------ SYNCSLOTS ESTABLISH -------------->|                                 |
       |            ...             |                                                |----- SYNCSLOTS ESTABLISH ------>|
       |                            |<-------------------- +OK ----------------------|                                 |
       |-CLUSTER GETSLOTMIGRATIONS->|                                                |                                 |
       |<-----{"state": "..."}------|~~~~~~~~~~~~~~~~~~ snapshot ~~~~~~~~~~~~~~~~~~~>|                                 |
       |            ...             |                                                |~~~~~~ forward snapshot ~~~~~~~~>|
       |                            |----------- SYNCSLOTS SNAPSHOT-EOF ------------>|                                 |
       |-CLUSTER GETSLOTMIGRATIONS->|                                                |                                 |
       |<-----{"state": "..."}------|<----------- SYNCSLOTS REQUEST-PAUSE -----------|                                 |
       |            ...             |                                                |                                 |
       |                            |~~~~~~~~~~~~ incremental changes ~~~~~~~~~~~~~~>|                                 |
       |-CLUSTER GETSLOTMIGRATIONS->|                                                |~~~~~~ forward changes ~~~~~~~~~>|
       |                            |--------------- SYNCSLOTS PAUSED -------------->|                                 |
       |            ...             |                                                |                                 |
       |                            |<---------- SYNCSLOTS REQUEST-FAILOVER ---------|                                 |
       |-CLUSTER GETSLOTMIGRATIONS->|                                                |                                 |
       |<-----{"state": "..."}------|---------- SYNCSLOTS FAILOVER-GRANTED --------->|                                 |
       |            ...             |                                                |                                 |
       |                            |                                            (performs takeover &                  |
       |-CLUSTER GETSLOTMIGRATIONS->|                                             propagates topology)                 |
       |<-----{"state": "..."}------|                                                |                                 |
       |            ...             |                                                |------- SYNCSLOTS FINISH ------->|
       |                      (finds out about topology                              |                                 |
       |                       change & marks migration done)                        |                                 |
       |                            |                                                |                                 |
       |-CLUSTER GETSLOTMIGRATIONS->|                                                |                                 |
       |<---{"state": "success"}----|                                                |                                 |
```

Since the `CLUSTER SYNCSLOTS` command is considered an internal command, the
subcommands and semantics are subject to change in future versions.

## Benefits of Atomic Slot Migration

By replicating the slot contents and atomically transferring ownership, Atomic
Slot Migration provides many desirable properties over the previous mechanism:

1. **Clients are unaware**: Since the entire hash slot is replicated before any
   cleanup is done on the source node, clients are completely unaware of the
   slot migration, and no longer need to follow `ASK` redirections and handle
   `TRYAGAIN` errors for multi-key operations.
2. **Keys no longer need to be atomically moved**: Collections are moved in
   chunks, preventing the reliability problems previously encountered when
   dumping and restoring a large collection.
3. **A migration can easily be rolled back on cancellation or failure**: Since
   the hash slots are placed in a staging area, we can easily wipe them
   independently of the rest of the database. Since this state is not
   broadcasted to the cluster, ending the migration is as simple as cleaning up
   the staging area and marking the migration as cancelled. Many failures, like
   out-of-memory, failover, or network partition can be handled completely by
   the engine, and only require the operator to check the result through
   `CLUSTER GETSLOTMIGRATIONS`.
4. **Greatly improved slot migration latency**: Valkey is already
   highly-optimized for replication. By batching the slot migrations and
   replicating their contents, the end-to-end migration latency can improve by
   as much as 31x when compared to using `CLUSTER SETSLOT` through the
   valkey-cli.

## Configuring Atomic Slot Migration

Some configurations may be worth tuning based on your workload:

- `client-output-buffer-limit`: Since the new atomic slot migration uses the
  replication process to migrate the slots, the amount of accumulated mutations
  while snapshotting could exceed that of the configured replication output
  buffer limit. Both the hard and soft limits of the `replica` client output
  buffer should be configured large enough to accumulate the accumulated
  mutations.
- `slot-migration-max-failover-repl-bytes`: By default, Atomic Slot Migration
  will only proceed to pausing mutations on the source node once all in-flight
  mutations have been sent to the target node. However, for workloads with
  persistently high write throughput, Atomic Slot Migration can be configured to
  do the pause so long as all in-flight mutations are under a given threshold.
- `cluster-slot-migration-log-max-len`: Atomic Slot Migration keeps track of all
  in progress migrations and recently completed or failed migrations. These can
  be viewed with `CLUSTER GETSLOTMIGRATIONS`. The number of recently completed
  migrations stored can be increased using this configuration.

---
title: Forkless operations
description: Overview of forkless operations
---

Valkey uses the `fork()` system call for several background operations, including saving the dataset to disk and fully synchronizing replicas.
Fork-based operations have been part of Valkey since its earliest days and are a simple, proven approach.
They also come with tradeoffs that can matter for some workloads.
One of them is memory usage: the forked child process shares memory with Valkey through copy-on-write, so memory usage can grow while the child is running.
In extreme cases, where writes are spread across much of the dataset during that time, memory usage can grow by up to 2x.

Valkey 9.2 introduces **forkless save** and **forkless full sync**, which perform these two operations without calling `fork()`.
Valkey takes the snapshot inside the running process, which keeps memory usage steadier and more predictable while the operation runs.
In this case, the tradeoff is that writes can briefly wait and latency can be slightly higher during the operation, as discussed later in [Impact on clients](#impact-on-clients).

It is important to note that forkless is not yet a full replacement for `fork()`.
In some situations, Valkey falls back to a fork-based save or full sync even when it is configured to prefer forkless operations.
When using forkless, it is highly encouraged to plan the configuration in a way that avoids these fallbacks, and to take into account that other operations, such as AOF rewrite and atomic slot migration, still use `fork()`.
This page describes how to plan for forkless operations.

## Enabling forkless operations

Forkless operations are disabled by default.
Two configuration parameters control them:

- `forkless-infrastructure-enabled`: enables support for forkless operations.
  It is `no` by default and can only be set at startup.
  When enabled, Valkey stores an additional 4 bytes with each key.
  This setting does not change how saves or full syncs are performed on its own.
- `forkless-policy`: selects how background saves and full syncs are performed.
  The default, `require-fork`, always uses `fork()`.
  `prefer-forkless` uses forkless operations when possible and falls back to `fork()` otherwise, as described in [When Valkey uses fork instead](#when-valkey-uses-fork-instead).
  It can be changed at runtime with `CONFIG SET`, and can only be set to `prefer-forkless` when `forkless-infrastructure-enabled` is `yes`.

### When Valkey uses fork instead

As the name suggests, `prefer-forkless` does not guarantee that every save and full sync is forkless.
Before each operation, Valkey checks whether a forkless operation is possible, and uses `fork()` when it is not.
Each fallback is logged to the server log, and counted in the `debug` section of `INFO`.

Valkey uses `fork()` for saves when:

- **A loaded module does not support forkless operations.**
  Every loaded module must declare support, as described in [For module developers](#for-module-developers).
  Counted in `forkless_fallbacks_module`.
- **The node is receiving slots through atomic slot migration.**
  This applies to the target node of a [`CLUSTER MIGRATESLOTS`](atomic-slot-migration.md) operation, for example while resharding.
  Saves and full syncs on that node use `fork()` until the migration finishes.
  `CLUSTER GETSLOTMIGRATIONS` shows which migrations are in progress.
  Counted in `forkless_fallbacks_slot_import`.

For full syncs, the conditions above apply, and Valkey additionally uses `fork()` when:

- **The replica runs a Valkey version older than 9.2.**
  Counted in `forkless_fallbacks_missing_inband_repl` or `forkless_fallbacks_old_rdb_version`.
- **The replica uses `repl-diskless-load swapdb`.**
  This only applies when the primary uses diskless sync (`repl-diskless-sync yes`, the default).
  Counted in `forkless_fallbacks_missing_inband_repl`.
- **The replica loads a module that does not support forkless operations.**
  This only applies when the primary uses diskless sync (`repl-diskless-sync yes`, the default).
  Counted in `forkless_fallbacks_missing_inband_repl`.
- **Replication compression is enabled.**
  When `repl-compression` is enabled on both the primary and the replica, the full sync uses `fork()`.
  Counted in `forkless_fallbacks_compression`.
- **A client requests an RDB file that contains only functions**, for example with `valkey-cli --functions-rdb`.
  Counted in `forkless_fallbacks_exclude_data`.

### Events that cancel forkless operations

Some events that do not affect a fork-based save or full sync cancel a forkless one:

- **`FLUSHDB`** cancels a forkless save to disk, including the save performed for a disk-based full sync (`repl-diskless-sync no`).
  During a diskless full sync, `FLUSHDB` cancels the sync only when the flushed database holds more than half of all keys.
  Otherwise, the flush is sent to the replica as part of the sync.
- **The start of a slot import** cancels a forkless full sync on the target node of an atomic slot migration.
  The replica's next full sync uses `fork()`, as described above.

When a full sync is cancelled, the replica reconnects and starts a new full sync.
When a save is cancelled, automatic saves configured with `save` are retried later, and a save started with `BGSAVE` must be started again.

## Monitoring forkless operations

The `persistence` section of `INFO` shows which method Valkey uses:

- `rdb_current_bgsave_type`: the method of the save or full sync in progress, `fork` or `forkless`, or `none` when no save is running.
- `rdb_last_bgsave_type`: the method of the last completed save to disk.
- `forkless_estimated_seconds_remaining`: an estimate of the time left in the forkless save or full sync in progress, or `-1` when none is running.

The server log records the method of each full sync, and the reason for each fallback.
For debugging, the `debug` section of `INFO` also includes the `forkless_fallbacks_*` counters described in [When Valkey uses fork instead](#when-valkey-uses-fork-instead).

## Impact on clients

A forkless operation runs while Valkey keeps serving clients, so it can affect commands that write to the dataset:

- **Writes can briefly wait.**
  A write to a key during a forkless operation has a small risk of waiting briefly.
  The larger the key, the higher the risk and the longer the wait.
  String values of up to 512 bytes are generally not affected.
  Read commands do not wait, except for the few that modify data internally, such as `PFCOUNT`.
- **Latency can be slightly higher.**
  Command latency can be slightly higher while a forkless operation runs, compared to a comparable fork-based operation.

Workloads with very large keys that receive frequent writes are the most affected.
Splitting very large collections into smaller keys reduces both the chance that a write waits and how long it waits.

## For module developers

A module declares that it supports forkless operations by setting the `VALKEYMODULE_OPTIONS_HANDLE_FORKLESS` option with `ValkeyModule_SetModuleOptions`.
Forkless operations are used only when every loaded module sets this option.
A module that does not set it keeps working as before, and Valkey uses `fork()` for saves and full syncs while that module is loaded, even when `forkless-policy` is set to `prefer-forkless`.

By setting the option, a module agrees to the following:

- **RDB save callbacks must be thread-safe.**
  A module that registers a data type declares that its RDB save callbacks can run on a background thread, at the same time as commands run on the main thread.
  The value being saved does not change during the callback, but any other module state that the callback reads must be protected with synchronization.
- **Auxiliary save callbacks must be small.**
  An `aux_save` or `aux_save2` callback must run only in the `VALKEYMODULE_AUX_BEFORE_RDB` section and save only a limited amount of data, because it runs on the main thread and blocks it during a forkless operation.
- **Opening a key for write can return `NULL`.**
  While a forkless operation is running, `ValkeyModule_OpenKey` with `VALKEYMODULE_WRITE` can return `NULL` for keys that the module command did not declare.
  For the keys that a module command declares, the risk is the same as for other writes, as described in [Impact on clients](#impact-on-clients): the command can briefly wait.
  For undeclared keys, including keys opened outside of a command, such as from a timer, there is a chance that `NULL` is returned.
  From the module's point of view, when `NULL` is returned can seem random, because it depends on internal server state that changes rapidly and cannot generally be monitored.
  Therefore, modules should be designed so that every such write can handle a `NULL` return.

A module cannot be loaded while a forkless save or full sync is running.
`MODULE LOAD` returns an error, and the module can be loaded after the operation finishes.

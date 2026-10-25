---
title: "Hot key detection"
description: >
    Finding the most frequently accessed keys on a Valkey server
---

A small number of keys often receives a disproportionate share of the traffic. On
a cluster those keys limit how evenly load can be spread, since a single hot key
cannot be split across shards; on a single server they are the keys worth caching
client-side, sharding across several keys, or rate-limiting. Hot key detection
finds them, on the server, from the traffic the server actually serves.

## How it works

Counting every access to every key exactly would cost memory proportional to the
keyspace and add work to every lookup. Detection approximates instead: it records
a random `hotkeys-sampling-percentage` of accesses, and tracks at most
`hotkeys-top-k` keys at a time. So a reported rate is an estimate, and a key
quieter than the top-K may not appear at all.

Counts accumulate in a *live* window. When `hotkeys-window-seconds` has elapsed
the live window is *frozen* and a fresh one starts.
[`HOTKEYS GET`](../commands/hotkeys-get.md) always reports the frozen window —
the last one to complete — and never the partial window still accumulating. A
report therefore describes a recent, completed interval rather than an average
since the server started, and the figures in one reply are all measured over the
same interval. A window can run slightly past its nominal length; rates divide by
the span actually measured, so that does not inflate them.

State is per node. Each server tracks only the accesses it serves, so on a
cluster query each node and read each reply on its own; there is no aggregated,
cluster-wide view.

## Configuration

Detection is disabled by default. Enable it by setting `hotkeys-top-k` to a
positive value, then read the result with
[`HOTKEYS GET`](../commands/hotkeys-get.md).

| Parameter | Default | Range | Meaning |
| --- | --- | --- | --- |
| `hotkeys-top-k` | `0` (disabled) | 0-1000 | Number of keys tracked, and the on/off switch: `0` disables detection entirely, any positive value enables it |
| `hotkeys-sampling-percentage` | `1` | 1-100 | Percentage of client key accesses that are sampled; `100` samples every access |
| `hotkeys-window-seconds` | `1` | 1-300 | Length of the reporting window |

All three can be changed at runtime with
[`CONFIG SET`](../commands/config-set.md). Any change discards the in-progress
window, whose counts were gathered under the old settings. What happens to the
last completed window depends on which parameter changed:

* `hotkeys-sampling-percentage`, `hotkeys-window-seconds`, or raising
  `hotkeys-top-k`: it is kept, so an in-flight
  [`HOTKEYS GET`](../commands/hotkeys-get.md) still sees it. The estimate uses
  the sampling percentage that was in effect when that window was recorded, not
  the new one.
* Lowering `hotkeys-top-k`: it is trimmed to the new top-K, so the coldest
  entries disappear from the next report.
* Setting `hotkeys-top-k` to `0`: detection is disabled and both windows are
  released.

Use [`HOTKEYS RESET`](../commands/hotkeys-reset.md) to discard everything
without changing the configuration.

While detection is disabled no memory is allocated for it and no work is added to
the access path.

## Choosing the sampling percentage and window

Both `hotkeys-sampling-percentage` and `hotkeys-window-seconds` improve accuracy,
because both increase how many samples a key contributes to a window. Each has a
cost: a higher sampling percentage adds per-access overhead, while a longer
window makes the report slower to react to a change in traffic. The defaults
(1%, 1 second) keep overhead low and the report quick to react, so raise either
when the rates you care about are too low to resolve.

The ranking is more robust than the individual numbers. Two keys with similar
rates may appear in either order, but a key with an order of magnitude more
traffic than another will reliably rank above it.

## What counts as an access

Each key a command touches is counted separately, so one command can record
several accesses: `MGET a b c` counts one access each for `a`, `b` and `c`.

Counted:

* Reads and writes alike, by any client executing a command.
* Accesses to keys that do not exist. This is deliberate — it surfaces load
  against a missing key, for example a bad key template, or a stampede on a key
  an eviction just removed.
* [`DEL`](../commands/del.md) and [`UNLINK`](../commands/unlink.md), which are
  activity on the key like any other access.
* Traffic served while importing, which is user-driven load.

Not counted:

* Replication and AOF traffic, so a replica reports the load its own clients
  generate rather than its primary's.
* Keys touched while loading an RDB or AOF file.
* Introspection lookups, such as those made by
  [`OBJECT`](../commands/object.md) and [`DEBUG`](../commands/debug.md).
* Key expiry, whether removed by the active expiry cycle or lazily on access,
  and eviction. The removal itself is not client access. Note that the client
  lookup which *triggers* a lazy expiry is still counted, as an access to a key
  that is now missing.
* Administrative bulk slot deletion.
* Background maintenance such as active defragmentation, which relocates keys
  in memory without going through the lookup path at all.

## Discarded windows

If the server is stalled long enough that the open window ends up covering more
than twice `hotkeys-window-seconds`, its counts no longer describe a single
window and are discarded.
[`HOTKEYS GET`](../commands/hotkeys-get.md) then returns an empty array until the
next window completes, rather than presenting a long-run average as if it were a
single window. This bounds how stale a report can be, at the cost of discarding
the accesses seen during the stall.

## Monitoring

[`INFO`](../commands/info.md) `hotkeys` reports two fields describing the last
completed window. The section is not part of the default `INFO` output, so
request it by name or use `INFO all`.

* `hotkeys_last_window_samples`: how many accesses were sampled. A window with
  few samples supports only a coarse estimate, so this indicates how much to
  trust a given report.
* `hotkeys_last_window_duration_ms`: the real span the window covered, which is
  also the denominator of every reported rate. `0` means there is no completed
  window to describe: detection is disabled, it was just enabled or reset, or the
  last window was discarded for spanning more than twice the configured length.

```
127.0.0.1:6379> INFO hotkeys
# Hotkeys
hotkeys_last_window_samples:19
hotkeys_last_window_duration_ms:1002
```

## State and resets

Hot key state, both the live window and the last completed one, is cleared by
[`HOTKEYS RESET`](../commands/hotkeys-reset.md) and automatically by anything
that discards an entire database or slot range:
[`FLUSHDB`](../commands/flushdb.md), [`FLUSHALL`](../commands/flushall.md), a
full sync or RDB reload that empties the dataset, a cluster reset, and dropping a
slot. The qualifier matters: a reload that keeps the existing data, such as
`DEBUG RELOAD NOFLUSH`, or one that is rejected by the RDB compatibility check,
never empties the dataset and so leaves hot key state in place. A
`repl-diskless-load swapdb` full sync is a further exception: it swaps the loaded
dataset in place instead of emptying the old one, and also leaves hot key state
untouched.

Ordinary key access and removal is activity rather than a reset, so
[`DEL`](../commands/del.md) and [`UNLINK`](../commands/unlink.md) count as
accesses, and expiry and eviction do not clear state.

Renaming or moving a key does not carry its statistics to the new name or
database. An entry is tracked by (key name, database), so after
[`RENAME`](../commands/rename.md), [`MOVE`](../commands/move.md) or
[`SWAPDB`](../commands/swapdb.md) the accumulated counts stay under the key's
previous identity. The entry stops accruing new hits immediately and then ages
out: it leaves the live window at the next rotation and the frozen window one
rotation after that, so a report can show the previous name or database for up to
roughly twice `hotkeys-window-seconds`.

## Commands

* [`HOTKEYS GET`](../commands/hotkeys-get.md): the hottest keys of the last
  completed window.
* [`HOTKEYS RESET`](../commands/hotkeys-reset.md): clear all collected
  statistics.
* [`HOTKEYS HELP`](../commands/hotkeys-help.md): help text for the subcommands.

## Comparison with `valkey-cli --hotkeys`

[`valkey-cli`](cli.md) has a `--hotkeys` option, which is a different mechanism
with different requirements. It scans the whole keyspace from the client and
reads each key's [`OBJECT FREQ`](../commands/object-freq.md), so it requires
`maxmemory-policy` to be set to an LFU policy, and its cost grows with the size
of the keyspace. What it reports is the LFU counter: a logarithmic, decaying
approximation of access frequency, shaped by `lfu-log-factor` and
`lfu-decay-time`, rather than a count of accesses over a known interval.

Server-side detection needs no particular eviction policy, costs nothing
proportional to the keyspace, and reports a rate over a recent window — which is
what identifies a key that is hot *now*.

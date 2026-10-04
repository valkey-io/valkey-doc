---
title: "Hot key detection"
description: >
    Finding the most frequently accessed keys on a Valkey server
---

A small number of keys often receives a disproportionate share of the traffic. On
a cluster those keys limit how evenly load can be spread, since a single hot key
cannot be split across shards; on a single server they are the keys worth caching
client-side, splitting, or rate-limiting. Hot key detection finds them, on the
server, from the traffic the server actually serves.

Detection is disabled by default. Enable it by setting `hotkeys-top-k` to a
positive value, then read the result with [`HOTKEYS GET`](../commands/hotkeys-get.md).

## How it works

Measuring every access to every key exactly would cost memory proportional to the
keyspace and add work to every lookup. Detection instead approximates, in two
ways:

* **Sampling.** Only `hotkeys-sampling-percentage` percent of accesses are
  recorded, chosen independently at random.
* **Bounded tracking.** Sampled accesses feed the Space-Saving algorithm, which
  tracks at most `hotkeys-top-k` keys in a fixed amount of memory. Rather than
  discard a new key when full, it replaces the coldest tracked key and inherits
  its count, which can over-estimate. Space-Saving keeps that possible
  over-estimate alongside each count, and the reported rate is derived from the
  middle of the resulting range.

Counts accumulate in a *live* window. When `hotkeys-window-seconds` has elapsed
the live window is *frozen* and a fresh one starts. `HOTKEYS GET` always reports
the frozen window — the last one to complete — and never the partial window still
accumulating. So a report describes a recent, completed interval rather than an
average since the server started, and the figures in one reply are all measured
over the same interval.

State is per node. Each server tracks only the accesses it serves, so on a
cluster query each node and read each reply on its own; there is no aggregated,
cluster-wide view.

## Configuration

| Parameter | Default | Range | Meaning |
| --- | --- | --- | --- |
| `hotkeys-top-k` | `0` (disabled) | 0-1000 | Number of keys tracked, and the on/off switch: `0` disables detection entirely, any positive value enables it |
| `hotkeys-sampling-percentage` | `1` | 1-100 | Percentage of client key accesses that are sampled; `100` samples every access |
| `hotkeys-window-seconds` | `1` | 1-300 | Length of the reporting window |

All three can be changed at runtime with
[`CONFIG SET`](../commands/config-set.md). Changing any of them discards the
in-progress window, whose counts were gathered under the old settings, but keeps
the last completed window so an in-flight `HOTKEYS GET` still sees it. Use
[`HOTKEYS RESET`](../commands/hotkeys-reset.md) to discard everything.

While detection is disabled no memory is allocated for it and no work is added to
the access path.

## Choosing the sampling percentage and window

A reported rate is a statistical estimate, and its precision depends on how many
samples the key contributed to the window:

```
samples ≈ qps × hotkeys-sampling-percentage / 100 × hotkeys-window-seconds
```

Sampling is independent per access, so the relative sampling error of an estimate
falls as roughly `1 / sqrt(samples)`. A key that contributes few samples therefore
has a correspondingly coarse estimate, and `hotkeys-sampling-percentage` and
`hotkeys-window-seconds` both scale the sample count in proportion: both improve
accuracy. A higher sampling percentage adds per-access overhead. A longer window
delays how quickly the report reacts to a change in traffic.

The ranking is more robust than the individual numbers. Two keys whose estimates
are within each other's error may appear in either order, but a key with an order
of magnitude more traffic than another will reliably rank above it.

Space-Saving guarantees that a key is tracked if it accounts for more than
`1 / hotkeys-top-k` of the sampled accesses in the window. `INFO hotkeys` reports
the window's sample total, so that threshold can be read off a live server (see
[Monitoring](#monitoring)).

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
* Passive expiry and eviction, which are not client access.
* Administrative bulk slot deletion.

## Windows

Windows are closed by the server's periodic task rather than by a dedicated
timer, so a window is frozen at or shortly after its nominal boundary and spans
`hotkeys-window-seconds` plus a small lag. Reported rates divide by the span
actually measured rather than by the configured length, so the lag does not
inflate them.

If the server is stalled long enough that the open window ends up covering more
than twice `hotkeys-window-seconds`, its counts describe too coarse an interval
to publish as "the last window" and are dropped instead. `HOTKEYS GET` then
returns an empty array until the next window completes, rather than presenting a
long-run average as if it were a single window. This bounds how stale a report
can be, at the cost of discarding the accesses seen during the stall.

## Monitoring

`INFO hotkeys` reports two fields describing the last completed window. The
section is not part of the default [`INFO`](../commands/info.md) output, so
request it by name or use `INFO all`.

* `hotkeys_last_window_samples`: how many accesses were sampled. Combined with
  `hotkeys-top-k` this gives the detection floor described above, and it
  indicates how much to trust a given entry.
* `hotkeys_last_window_duration_ms`: the real span the window covered, which is
  also the denominator of every reported rate. `0` means there is no completed
  window: detection was just enabled or reset, or the last window was dropped for
  spanning more than twice the configured length.

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
full sync or RDB reload, a cluster reset, and dropping a slot. A
`repl-diskless-load swapdb` full sync is the exception: it swaps the loaded
dataset in place instead of emptying the old one, and leaves hot key state
untouched.

Ordinary key access and removal is activity rather than a reset, so `DEL` and
`UNLINK` count as accesses, and expiry and eviction do not clear state.

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
reads each key's access counter, so it requires `maxmemory-policy` to be set to
an LFU policy, its cost grows with the size of the keyspace, and it reports
counters accumulated over the key's lifetime.

Server-side detection needs no particular eviction policy, costs nothing
proportional to the keyspace, and reports a rate over a recent window — which is
what identifies a key that is hot *now*.

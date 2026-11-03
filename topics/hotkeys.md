---
title: "Hot key tracking"
description: >
    Finding the most frequently accessed keys on a Valkey server
---

A small number of keys often receives a disproportionate share of the traffic. On
a cluster those keys limit how evenly load can be spread, since a single hot key
cannot be split across shards; on a single server they are the keys worth caching
client-side, sharding across several keys, or rate-limiting. Hot key tracking
finds them, on the server, from the traffic the server actually serves.

## How it works

Counting every access to every key exactly would cost memory proportional to the
keyspace and add work to every lookup. Tracking approximates instead: it records
a random `hotkeys-sampling-percentage` of accesses, and tracks at most
`hotkeys-top-k` keys at a time. The result is an approximate set of candidates:
neither exact top-K membership nor the relative order of the entries is
guaranteed, and a key quieter than the top-K may not appear at all.

Counts accumulate in a *live* window. When `hotkeys-window-seconds` has elapsed
the live window is *frozen* and a fresh one starts.
[`HOTKEYS GET`](../commands/hotkeys-get.md) always reports the frozen window —
the last one to complete — and never the partial window still accumulating. A
report therefore describes a recent, completed interval rather than an average
since the server started, and the figures in one reply are all measured over the
same interval.

If the server stalls long enough that the live window has spanned at least twice
`hotkeys-window-seconds` by the time it rotates, its counts no longer describe a
single window. Both the live and the frozen state are then discarded, and
`HOTKEYS GET` returns an empty result until the next valid window completes.

Keys are tracked over the whole keyspace, not per logical database. There is one
top-K list, and every key competes for a place in it whichever database it
belongs to; each entry records the database it was accessed in so the keys can be
told apart.

State is per node. Each server tracks only the accesses it serves, so on a
cluster query each node and read each reply on its own; there is no aggregated,
cluster-wide view.

## Configuration

Tracking is disabled by default. Enable it by setting `hotkeys-top-k` to a
positive value.

| Parameter | Default | Range | Meaning |
| --- | --- | --- | --- |
| `hotkeys-top-k` | `0` (disabled) | 0-1000 | Number of keys tracked: `0` disables tracking entirely, any positive value enables it |
| `hotkeys-sampling-percentage` | `1` | 1-100 | Percentage of client key accesses that are sampled; `100` samples every access |
| `hotkeys-window-seconds` | `1` | 1-300 | Length of the reporting window |

All three can be changed at runtime with
[`CONFIG SET`](../commands/config-set.md). A change takes at least one full
window to take effect, since a report always describes a window that has already
completed.

## Choosing the sampling percentage and window

Both `hotkeys-sampling-percentage` and `hotkeys-window-seconds` can improve
accuracy by increasing the number of samples a key contributes to each
measurement window. Each comes with a different trade-off: a higher sampling
percentage increases per-access overhead, while a longer window provides more
samples but makes the report slower to reflect changes in access patterns, since
samples from earlier in the window are still included. The defaults (1% sampling
and a 1-second window) keep overhead low while allowing the report to react
quickly to changing traffic. Increase either setting when the hot key rates you
care about are too low to resolve reliably.

## What counts as an access

Accesses are sampled at individual key lookups and at successful key removals,
not once per command and key pair. So a command that touches several keys
contributes one access for each of them, and a command that both reads and
removes the same key contributes two: `MGET a b c` records one access against
each of `a`, `b` and `c`, while `GETDEL` on an existing key records two against
that one key.

A lookup counts whether or not the key exists, which helps reveal load caused by
missing keys or repeated requests for keys that have been evicted. A removal only
counts when it removes something, so [`DEL`](../commands/del.md) and
[`UNLINK`](../commands/unlink.md) on an existing key count as accesses while the
same commands on a missing key record nothing. Client-driven traffic during data
imports is counted as well.

Internal activity is not counted. This includes the write stream a replica
applies from its primary and the commands a server loads from an RDB or AOF file,
introspection lookups such as those made by [`OBJECT`](../commands/object.md),
administrative bulk slot deletion, and background maintenance such as active
defragmentation. Key expiration and eviction are also not counted, because the
removal itself is internal activity — but a client lookup that triggers a lazy
expiration is still counted, since the lookup was initiated by the client.

## State and resets

Hot key tracking keeps statistics for both the current (live) window and the last
completed window. You can clear this state explicitly with
[`HOTKEYS RESET`](../commands/hotkeys-reset.md), or it is cleared automatically
when an operation discards an entire database or slot range.

The following operations clear hot key state:

* [`FLUSHDB`](../commands/flushdb.md) and [`FLUSHALL`](../commands/flushall.md)
* A full sync or RDB reload that empties the dataset
* A cluster reset
* Dropping a slot

Normal key activity does not clear hot key state: `DEL` and `UNLINK` are treated
as accesses, and neither expiration nor eviction clears the tracking state.

### Renaming and moving keys

Hot key statistics are associated with a key's name and database, rather than
with the underlying key itself. As a result, renaming or moving a key does not
transfer its statistics to its new name or database.

After [`RENAME`](../commands/rename.md), [`MOVE`](../commands/move.md), or
[`SWAPDB`](../commands/swapdb.md), the existing statistics remain associated with
the key's previous identity, and clients still accessing that old name or
database keep adding to them — a lookup of a key that is no longer there is
counted like any other. Once no further accesses are recorded against it, the
entry ages out of the tracking windows: it leaves the live window at the next
window rotation, and the last-completed (frozen) window one rotation later. So a
report can continue to show the old key name or database for up to roughly twice
`hotkeys-window-seconds` after the last access to it.

## Monitoring

`INFO hotkeys` describes the last completed window: how many accesses were
sampled, and the length of the window those samples were measured over. See
[`INFO`](../commands/info.md) for the fields.

## Commands

* [`HOTKEYS GET`](../commands/hotkeys-get.md): the hottest keys of the last
  completed window.
* [`HOTKEYS RESET`](../commands/hotkeys-reset.md): clear all collected
  statistics.
* [`HOTKEYS HELP`](../commands/hotkeys-help.md): help text for the subcommands.

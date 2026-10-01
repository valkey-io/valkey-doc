This is a container command for hot key detection commands. To see the list of
available subcommands, run [`HOTKEYS HELP`](hotkeys-help.md).

Hot key detection samples client key accesses and maintains an approximate
top-K of the most frequently accessed keys using the Space-Saving algorithm.
Accesses accumulate in a *live* window; when the window elapses it is *frozen*,
and [`HOTKEYS GET`](hotkeys-get.md) reports that last completed window, never
the partial one still accumulating.

Detection is disabled by default and consumes no resources while off. State is
per node: each server tracks only the accesses it serves, so in a cluster you
query each node separately.

## Configuration

| Parameter | Default | Range | Meaning |
| --- | --- | --- | --- |
| `hotkeys-top-k` | `0` (disabled) | 0-1000 | Number of keys tracked, and the on/off switch: `0` disables detection entirely, any positive value enables it |
| `hotkeys-sampling-percentage` | `1` | 1-100 | Percentage of client key accesses that are sampled; `100` samples every access |
| `hotkeys-window-seconds` | `1` | 1-300 | Length of the reporting window |

All three can be changed at runtime with [`CONFIG SET`](config-set.md).
Changing any of them discards the in-progress window, whose counts were gathered
under the old settings, but keeps the last completed window so an in-flight
`HOTKEYS GET` still sees it. Use [`HOTKEYS RESET`](hotkeys-reset.md) to discard
everything.

Because only a fraction of accesses is sampled, a reported value is a statistical
estimate whose precision follows the number of samples a key contributed to the
window, which is about
`qps * hotkeys-sampling-percentage / 100 * hotkeys-window-seconds`. With the
defaults (1%, 1 second) the resolution is roughly 100 QPS, and a key at 10,000
QPS contributes around 100 samples, giving its estimate a relative error of
roughly ±10%; at 1,000 QPS it contributes around 10 samples and the error is
closer to ±30%. Raising `hotkeys-sampling-percentage` and raising
`hotkeys-window-seconds` both increase the sample count in proportion, so either
buys the same accuracy — sampling at the cost of per-access overhead, the window
at the cost of how quickly a report reacts.

## What counts as an access

Any key lookup or client-issued deletion performed by a client executing a
command counts, reads and writes alike, and whether or not the key exists.
Accesses to a key that does not exist are tracked like any other, which surfaces
load against a missing key — a bad key template, or a stampede on a key that an
eviction just removed. [`DEL`](del.md) and [`UNLINK`](unlink.md) count as
accesses.

The following are not counted: replication and AOF traffic, keys touched while
loading an RDB or AOF file, introspection lookups such as those made by
[`OBJECT`](object.md) and [`DEBUG`](debug.md), passive expiry, eviction, and
administrative bulk slot deletion. Traffic served during an import is
user-driven load and is counted.

## Windows

Windows are closed by the server's periodic task, so a window is frozen at or
shortly after its nominal boundary and therefore spans `hotkeys-window-seconds`
plus a small lag. Reported QPS is divided by the span actually measured rather
than by the configured length, so the lag does not inflate the numbers.

If the server is stalled long enough that the open window ends up covering more
than twice `hotkeys-window-seconds`, its counts describe too coarse an interval
to report as "the last window" and are dropped instead. `HOTKEYS GET` then
returns an empty array until the next window completes, rather than presenting a
long-run average as if it were a single window. This bounds how stale a report
can be, at the cost of discarding the accesses seen during the stall.

## Monitoring

`INFO hotkeys` reports two fields describing the last completed window. The
section is not part of the default `INFO` output, so request it by name or use
`INFO all`.

* `hotkeys_last_window_samples`: the number of sampled observations, *N*. The
  Space-Saving guarantee is stated relative to *N*: only keys accessed more than
  *N* / `hotkeys-top-k` times are guaranteed to be tracked, so this gives the
  detection floor of a report and an indication of how much to trust a given
  entry.
* `hotkeys_last_window_duration_ms`: the real span the window covered, which is
  also the QPS denominator. `0` means there is no completed window: detection
  was just enabled or reset, or the last window was dropped for spanning more
  than twice the configured length.

## State and resets

Hot key state, both the live window and the last completed one, is cleared by
[`HOTKEYS RESET`](hotkeys-reset.md) and automatically by anything that discards
an entire database or slot range: [`FLUSHDB`](flushdb.md),
[`FLUSHALL`](flushall.md), a full sync or RDB reload (except a
`repl-diskless-load swapdb` sync, which swaps the loaded dataset in place and
leaves hot key state untouched), a cluster reset, and dropping a slot. Ordinary
key access and removal is treated as activity rather than a reset, so `DEL` and
`UNLINK` count as accesses, and expiry and eviction do not clear state.

Renaming or moving a key does not carry its statistics to the new name or
database. An entry is tracked by (key name, database), so after
[`RENAME`](rename.md), [`MOVE`](move.md) or [`SWAPDB`](swapdb.md) the
accumulated counts stay under the key's previous identity. The entry stops
accruing new hits immediately and then ages out: it leaves the live window at the
next rotation and the frozen window one rotation after that, so `HOTKEYS GET` may
report the previous name or database for up to roughly twice
`hotkeys-window-seconds`.

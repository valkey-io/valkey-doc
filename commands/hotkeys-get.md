The `HOTKEYS GET` command returns the hottest keys observed during the last
completed tracking window, ordered by estimated queries per second (QPS), from
highest to lowest. It takes no arguments and returns at most `hotkeys-top-k`
entries.

See [`HOTKEYS`](hotkeys.md) and [Hot key tracking](../topics/hotkeys.md) for how
tracking is enabled and configured, what an empty reply can mean, and how state
is reset.

Each entry contains:

* `key`: the key name.
* `db`: the database in which the key was accessed.
* `qps`: the estimated accesses per second over the completed window.

`qps` is an estimate rather than an exact value, because accesses are sampled
when `hotkeys-sampling-percentage` is below `100` (its default is `1`), and
because only `hotkeys-top-k` keys are tracked at a time. It is a rate over the
span the window actually covered, which [`INFO`](info.md) reports as
`hotkeys_last_window_duration_ms` in its `hotkeys` section. See
[Choosing the sampling percentage and window](../topics/hotkeys.md#choosing-the-sampling-percentage-and-window)
for how accuracy depends on those two settings.

A key that is accessed but does not exist is tracked like any other. This
surfaces load against a missing key, for example from a bad key template or a
stampede against a key an eviction just removed.

The command returns an empty array when there is nothing to report: either hot
key tracking is disabled, or no hot keys were tracked in the last completed
window.

## Examples

Enable tracking, then read the hottest keys:

```
127.0.0.1:6379> CONFIG SET hotkeys-top-k 16
OK
127.0.0.1:6379> HOTKEYS GET
1) 1) "key"
   2) "product:8fd21a"
   3) "db"
   4) (integer) 0
   5) "qps"
   6) (integer) 48200
2) 1) "key"
   2) "session:2c1f09"
   3) "db"
   4) (integer) 0
   5) "qps"
   6) (integer) 12700
```

The `HOTKEYS GET` command returns the hottest keys observed during the last
completed detection window, ordered by estimated queries per second (QPS), from
highest to lowest. It takes no arguments and returns at most `hotkeys-top-k`
entries.

See [`HOTKEYS`](hotkeys.md) and [Hot key detection](../topics/hotkeys.md) for how
detection is enabled and configured, what an empty reply can mean, and how state
is reset.

Each entry contains:

* `key`: the key name.
* `db`: the database in which the key was accessed.
* `qps`: the estimated accesses per second over the completed window. Each key a
  command touches counts separately, so `MGET a b c` contributes one access to
  each of the three keys.

`qps` is an estimate rather than an exact value, because accesses are sampled and
counts are tracked approximately. It is measured over the span the window
actually covered, which [`INFO`](info.md) reports as
`hotkeys_last_window_duration_ms` in its `hotkeys` section. See
[Choosing the sampling percentage and window](../topics/hotkeys.md#choosing-the-sampling-percentage-and-window)
for how accurate a given entry is.

A key that is accessed but does not exist is tracked like any other. This
surfaces load against a missing key, for example from a bad key template or a
stampede against a key an eviction just removed.

The command returns an empty array rather than an error whenever there is nothing
to report, so a polling client has a single reply shape to parse and does not
have to match on an error string to tell "disabled" from "nothing is hot". That
is the case when:

* Detection is disabled (`hotkeys-top-k` is `0`, the default).
* No window has completed yet, because detection was just enabled or
  [`HOTKEYS RESET`](hotkeys-reset.md) was just called.
* The last window was dropped for spanning more than twice
  `hotkeys-window-seconds`.
* No accesses were sampled during the last completed window.

## Examples

Enable detection, then read the hottest keys:

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

Before the first window has completed, or while detection is disabled:

```
127.0.0.1:6379> HOTKEYS GET
(empty array)
```

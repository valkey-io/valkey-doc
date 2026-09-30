Returns the hottest keys observed during the last completed detection window,
ordered by estimated accesses per second (QPS), from highest to lowest. At most
`hotkeys-top-k` entries are returned.

Each entry contains:

* `key`: the key name.
* `db`: the database in which the key was accessed.
* `qps`: the estimated accesses per second over the completed window.

`qps` is an estimate rather than an exact value. Accesses are sampled, and counts
are tracked approximately by the Space-Saving algorithm, which keeps each count
together with the maximum amount by which it may over-estimate. The reported
value is derived from the midpoint of that band, scaled back up by the sampling
percentage that was in effect when the window was recorded, and divided by the
span the window actually covered — the same span `INFO hotkeys` reports as
`hotkeys_last_window_duration_ms`.

The command returns an empty array rather than an error whenever there is nothing
to report, so a polling client has a single reply shape to parse and does not
have to match on an error string to tell "disabled" from "nothing is hot". That
is the case when:

* Detection is disabled (`hotkeys-top-k` is `0`, the default).
* No window has completed yet, because detection was just enabled, the
  configuration just changed, or [`HOTKEYS RESET`](hotkeys-reset.md) was just
  called.
* The last window was dropped for spanning more than twice
  `hotkeys-window-seconds`.
* No accesses were sampled during the last completed window.

See [`HOTKEYS`](hotkeys.md) for how detection is enabled and configured, what
counts as an access, and how state is cleared.

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

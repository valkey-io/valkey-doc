Clears all accumulated hot key statistics on this node, discarding both the
in-progress (live) window and the last completed (frozen) window. Afterwards,
[`HOTKEYS GET`](hotkeys-get.md) returns an empty array until the next window
completes.

Use it to start monitoring from a clean baseline. Note that changing
`hotkeys-top-k`, `hotkeys-sampling-percentage` or `hotkeys-window-seconds`
already discards the in-progress window on its own, but deliberately keeps the
last completed one; `HOTKEYS RESET` is what discards that too.

Hot key state is also cleared automatically by anything that discards an entire
database or slot range: [`FLUSHDB`](flushdb.md), [`FLUSHALL`](flushall.md), a
full sync or RDB reload that empties the dataset, a cluster reset, and dropping a
slot. `HOTKEYS RESET` is for clearing it on demand outside of those events.
Ordinary key access and removal is treated as activity rather than a reset, so
[`DEL`](del.md) and [`UNLINK`](unlink.md) count as accesses, and expiry and
eviction do not clear state.

Hot key detection is enabled by setting `hotkeys-top-k` to a positive value
(`0`, the default, disables it). While it is disabled there is nothing to clear
and the command succeeds as a no-op.

## Examples

```
127.0.0.1:6379> HOTKEYS RESET
OK
```

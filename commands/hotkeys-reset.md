The `HOTKEYS RESET` command clears all accumulated hot key statistics on this
node, discarding both the in-progress window and the last completed one. It takes
no arguments. Afterwards, [`HOTKEYS GET`](hotkeys-get.md) returns an empty array
until the next window completes.

Use it to start monitoring from a clean baseline. Changing
`hotkeys-top-k`, `hotkeys-sampling-percentage` or `hotkeys-window-seconds`
already discards the in-progress window on its own, but deliberately keeps the
last completed one; `HOTKEYS RESET` is what discards that too.

While detection is disabled (`hotkeys-top-k` is `0`, the default) there is
nothing to clear and the command succeeds as a no-op.

Hot key state is also cleared automatically by several server events. See
[State and resets](../topics/hotkeys.md#state-and-resets) for the full list.

## Examples

```
127.0.0.1:6379> HOTKEYS RESET
OK
127.0.0.1:6379> HOTKEYS GET
(empty array)
```

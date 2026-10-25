The `HOTKEYS RESET` command clears all accumulated hot key statistics on this
node, discarding both the in-progress window and the last completed one. It takes
no arguments. Afterwards, [`HOTKEYS GET`](hotkeys-get.md) returns an empty array
until the next window completes.

Use it to start monitoring from a clean baseline, without changing the
configuration.

While detection is disabled (`hotkeys-top-k` is `0`, the default) there is
nothing to clear and the command succeeds as a no-op.

Hot key state is also cleared automatically by several server events, and a
configuration change clears part of it. See
[Hot key detection](../topics/hotkeys.md) for both.

## Examples

```
127.0.0.1:6379> HOTKEYS RESET
OK
127.0.0.1:6379> HOTKEYS GET
(empty array)
```

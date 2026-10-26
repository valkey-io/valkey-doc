The `HOTKEYS RESET` command clears all accumulated hot key statistics on this
node, discarding both the in-progress window and the last completed one. It takes
no arguments. It always replies `OK`, including when hot key tracking is
disabled, in which case there is nothing to clear.

Use it to start monitoring from a clean baseline, without changing the
configuration.

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

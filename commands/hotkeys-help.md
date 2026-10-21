The `HOTKEYS HELP` command returns helpful text about the
[`HOTKEYS`](hotkeys.md) subcommands. For the feature itself, see
[Hot key detection](../topics/hotkeys.md).

## Examples

```
127.0.0.1:6379> HOTKEYS HELP
1) HOTKEYS <subcommand> [<arg> [value] [opt] ...]. Subcommands are:
2) GET
3)     Return the hottest keys of the last completed window, ordered by
4)     estimated accesses per second (descending). Each entry reports the
5)     key name, the database it was accessed in, and the estimated QPS.
6) RESET
7)     Clear all collected hot key statistics.
8) HELP
9)     Print this help.
```

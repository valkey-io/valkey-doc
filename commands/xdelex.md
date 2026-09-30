The `XDELEX` command is an extension of the [XDEL](xdel.md) command that allows you to delete one or more stream messages with more control over how those message entries are deleted concerning consumer groups.

The command supports three deletion modes:

- KEEPREF (default): deletes the stream entry but leaves pending entries list (PEL) references intact in all consumer groups,
- DELREF: deletes the stream entry and forcibly removes it from all consumer group PELs,
- ACKED: deletes a message only once no consumer group still needs it, meaning none has it pending (each has either acknowledged it or never picked it up), and no group can still deliver it later.

The command returns a per-ID integer array: `1` for deleted, `2` for exists-but-not-yet-deletable (ACKED mode only), and `-1` when the message wasn't found.

## Examples

```
127.0.0.1:6899> XADD s4 * a 1
"1788346731590-0"
127.0.0.1:6899> XGROUP CREATE s4 grp 0
OK
127.0.0.1:6899> XREADGROUP GROUP grp cons1 COUNT 10 STREAMS s4 >
1) 1) "s4"
    2) 1) 1) "1788346731590-0"
            2) 1) "a"
               2) "1"
127.0.0.1:6899> XDELEX s4 ACKED IDS 1 1788346731590-0
1) (integer) 2
127.0.0.1:6899> XLEN s4
(integer) 1
127.0.0.1:6899> XACK s4 grp 1788346731590-0
(integer) 1
127.0.0.1:6899> XDELEX s4 ACKED IDS 1 1788346731590-0
1) (integer) 1
127.0.0.1:6899> XLEN s4
(integer) 0
```

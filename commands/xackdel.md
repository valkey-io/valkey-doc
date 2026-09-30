The `XACKDEL` command is an extension of the [XACK](xack.md) stream command that acknowledges the specified message IDs in `group`'s pending entries list (PEL) and, depending on `mode`, deletes the underlying stream entries.

This is particularly useful when multiple consumer groups independently process the same stream and you need to reclaim entries without deleting messages that another group still needs.

The command supports three deletion modes:

- KEEPREF (default, implicit): acknowledges and deletes messages immediately, leaving PEL references in other groups,
- DELREF: acknowledges, deletes, and forcibly removes PEL entries from all other groups,
- ACKED: deletes a message only once no consumer group still needs it, meaning none has it pending (each has either acknowledged it or never picked it up), and no group can still deliver it later.

The command returns a per-ID integer array: `1` when the message was acknowledged (and, depending on mode, deleted), `2` when it was acknowledged but not yet deletable because another group still needs it (ACKED mode only), and `-1` when the key isn't a stream, the message doesn't exist, the group doesn't exist, or the message wasn't in group's PEL.

## Examples

```
127.0.0.1:6899> XADD s5 * a 1
"1788350000000-0"
127.0.0.1:6899> XGROUP CREATE s5 g1 0
OK
127.0.0.1:6899> XGROUP CREATE s5 g2 0
OK
127.0.0.1:6899> XREADGROUP GROUP g1 cons1 COUNT 10 STREAMS s5 >
1) 1) "s5"
   2) 1) 1) "1788350000000-0"
         2) 1) "a"
            2) "1"
127.0.0.1:6899> XACKDEL s5 g1 ACKED IDS 1 1788350000000-0
1) (integer) 2
127.0.0.1:6899> XLEN s5
(integer) 1
127.0.0.1:6899> XREADGROUP GROUP g2 cons1 COUNT 10 STREAMS s5 >
1) 1) "s5"
   2) 1) 1) "1788350000000-0"
         2) 1) "a"
            2) "1"
127.0.0.1:6899> XACKDEL s5 g2 ACKED IDS 1 1788350000000-0
1) (integer) 1
127.0.0.1:6899> XLEN s5
(integer) 0
```

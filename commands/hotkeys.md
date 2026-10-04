This is a container command for hot key detection commands. To see the list of
available subcommands, run [`HOTKEYS HELP`](hotkeys-help.md).

Hot key detection samples client key accesses and reports the most frequently
accessed keys over a recent, completed time window. It is disabled by default;
enable it by setting `hotkeys-top-k` to a positive value, and read the result
with [`HOTKEYS GET`](hotkeys-get.md).

For how detection works, how to configure and tune it, what counts as an access,
and when state is cleared, see
[Hot key detection](../topics/hotkeys.md).

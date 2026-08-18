This is a container command for hot key detection commands.

Hot key detection samples client key accesses and maintains an approximate
top-K of the most frequently accessed keys using the Space-Saving algorithm
over a fixed reporting window. It is disabled by default; enable it by setting
the `hotkey-top-k` configuration parameter to a positive value, which is both
the number of keys tracked and the on/off switch — `0` (the default) disables
detection entirely (see also `hotkey-sampling-percentage` and
`hotkey-window-seconds`).

To see the list of available subcommands, refer to
[`HOTKEYS GET`](hotkeys-get.md) and [`HOTKEYS RESET`](hotkeys-reset.md).

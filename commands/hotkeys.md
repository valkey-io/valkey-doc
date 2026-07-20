This is a container command for hot key detection commands.

Hot key detection samples client key accesses and maintains an approximate
top-K of the most frequently accessed keys using the Space-Saving algorithm
over a fixed reporting window. It is disabled by default; enable it by setting
the `hotkey-sampling-percentage` configuration parameter above `0` (see also
`hotkey-top-k` and `hotkey-window-seconds`).

To see the list of available subcommands, refer to
[`HOTKEYS GET`](hotkeys-get.md) and [`HOTKEYS RESET`](hotkeys-reset.md).

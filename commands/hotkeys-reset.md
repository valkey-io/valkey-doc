Clears all accumulated hot key statistics, discarding both the in-progress
(live) window and the last completed (frozen) window.

Hot key detection must be enabled by setting `hotkey-sampling-percentage` above
`0`; otherwise the command returns an error.

After `HOTKEYS RESET`, [`HOTKEYS GET`](hotkeys-get.md) returns an empty result
until the next window completes.

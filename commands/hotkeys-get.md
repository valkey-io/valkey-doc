Returns the hottest keys observed during the last completed detection window,
ordered by estimated accesses per second (QPS), from highest to lowest.

Hot key detection must be enabled by setting `hotkey-top-k` to a positive value
(`0`, the default, disables it); otherwise the command returns an error.

Client key accesses are sampled into a *live* window whose length is
`hotkey-window-seconds`. When a window completes it is *frozen*, and
`HOTKEYS GET` always reports that last completed window — never the partial,
in-progress one. Consequently, immediately after detection is enabled (or after
[`HOTKEYS RESET`](hotkeys-reset.md)) the command returns an empty result until
the first window completes.

Each returned entry contains:

* `key`: the key name.
* `db`: the database in which the key was accessed.
* `qps`: the estimated accesses per second over the completed window. Because
  counts are sampled and tracked approximately (Space-Saving), `qps` is an
  estimate rather than an exact value. It is reconstructed by scaling the
  sampled count by `100 / hotkey-sampling-percentage` and dividing by
  `hotkey-window-seconds`.

At most `hotkey-top-k` keys are returned.

Note that `RENAME`, `MOVE`, and `SWAPDB` are not re-attributed: a tracked entry
is keyed by (key name, database), so after one of these commands the
accumulated counts remain under the key's previous identity until they age out.
As these commands are not typically high-frequency, the stale entry is harmless
— it stops accruing new hits immediately and disappears once the reporting
window rotates (at most one `hotkey-window-seconds` later).

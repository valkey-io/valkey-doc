Load a script into the scripts cache, without executing it.
After the specified command is loaded into the script cache it will be callable
using [`EVALSHA`](evalsha.md) with the correct SHA1 digest of the script, exactly like after
the first successful invocation of [`EVAL`](eval.md).

The script is guaranteed to stay in the script cache forever (unless [`SCRIPT
FLUSH`](script-flush.md) is called).

The command works in the same way even if the script was already present in the
script cache.

Scripts loaded with this command are not evicted when the number of cached `EVAL` scripts
or the `maxmemory-scripts` limit is reached.
Starting from Valkey 9.2, `SCRIPT LOAD` is flagged as [`DENYOOM`](command.md#flags): when the server is over
the `maxmemory` limit and can't free memory by eviction, the command is rejected with an out of memory error.

For more information about `EVAL` scripts please refer to [Introduction to Eval Scripts](../topics/eval-intro.md).

## Reply

String: the SHA1 digest of the script added into the script cache.

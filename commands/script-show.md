Returns the original source code of a script in the script cache.

This command accepts a SHA1 digest and returns the original script's source code if the script is present in the script cache.
This command is intended primarily for debugging, to introspect into the contents of a script when the user does not have access to script anymore.
One example is when an admin only has access to a script SHA1 from monitor or slowlog, and is unable to determine the contents of the script.

For more information about `EVAL` scripts please refer to [Introduction to Eval Scripts](../topics/eval-intro.md).

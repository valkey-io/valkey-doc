Return the serialized payload of loaded libraries.
You can restore the serialized payload later with the `FUNCTION RESTORE` command.

For more information please refer to [Introduction to Valkey Functions](../topics/functions-intro.md).

## Examples

The following example shows how to dump loaded libraries using `FUNCTION DUMP` and then it calls `FUNCTION FLUSH` deletes all the libraries.
Then, it restores the original libraries from the serialized payload with `FUNCTION RESTORE`.

```
valkey> FUNCTION LOAD "#!lua name=mylib \n server.register_function('myfunc', function(keys, args) return args[1] end)"
"mylib"
valkey> FUNCTION DUMP
"\xf5\xc3@X@]\x1f#!lua name=mylib \n server.registe\rr_function('my@\x0b\x02', @\x06`\x12\nkeys, args) 6\x03turn`\x0c\a[1] end)\x0c\x00\xba\x98\xc2\xa2\x13\x0e$\a"
valkey> FUNCTION FLUSH
OK
valkey> FUNCTION RESTORE "\xf5\xc3@X@]\x1f#!lua name=mylib \n server.registe\rr_function('my@\x0b\x02', @\x06`\x12\nkeys, args) 6\x03turn`\x0c\a[1] end)\x0c\x00\xba\x98\xc2\xa2\x13\x0e$\a"
OK
valkey> FUNCTION LIST
1) 1) "library_name"
   2) "mylib"
   3) "engine"
   4) "LUA"
   5) "functions"
   6) 1) 1) "name"
         2) "myfunc"
         3) "description"
         4) (nil)
         5) "flags"
         6) (empty array)
```

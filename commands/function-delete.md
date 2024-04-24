Delete a library and all its functions.

This command deletes the library called _library-name_ and all functions in it.
If the library doesn't exist, the server returns an error.

For more information please refer to [Introduction to Valkey Functions](../topics/functions-intro.md).

@examples

```
valkey> FUNCTION LOAD "#!lua name=mylib \n server.register_function('myfunc', function(keys, args) return 'hello' end)"
"mylib"
valkey> FCALL myfunc 0
"hello"
valkey> FUNCTION DELETE mylib
OK
valkey> FCALL myfunc 0
(error) ERR Function not found
```

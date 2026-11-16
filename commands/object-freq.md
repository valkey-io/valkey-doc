This command returns the logarithmic access frequency counter of a Valkey object stored at `<key>`.

The command is only available when the `maxmemory-policy` configuration directive is set to one of the LFU policies.

## Reply

One of the following:

Integer: the counter's value.

Null: if _key_ doesn't exist.

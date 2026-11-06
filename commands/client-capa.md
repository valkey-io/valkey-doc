Clients can declare their capabilities to Valkey using the `CLIENT CAPA` command, and Valkey
will adjust the corresponding features for the current connection based on the declared client capabilities.

Multiple capabilities can be declared in the command. If any capabilities are unrecognized,
Valkey will ignore them instead of returning an error.

The capabilities currently supported are:

* `redirect` - This indicates that the client is capable of handling redirect messages.
  When accessing a replica node in standalone mode, if a data operation is performed (read or write commands),
  Valkey will return `-REDIRECT primary-ip:port` to this connection.
  Since Valkey 9.2, the same applies in cluster mode to read or write commands with no key arguments, such as `SCAN` or `FLUSHDB`.
  Note that the `primary-ip` can be an IPv6 which itself contains colons, so to properly parse ip and port, a client needs to locate the *last* colon.
  Using the [`READONLY`](readonly.md) command can enable this connection to execute read commands on the replica node.

## Reply

`OK`.

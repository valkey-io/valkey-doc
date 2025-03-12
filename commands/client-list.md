The `CLIENT LIST` command returns information and statistics about the client
connections server in a mostly human readable format.

You can use one or more optional arguments to filter the list:

- **`TYPE type`**: Filters the list by clients' type, where *type* is one of `normal`, `master`, `replica`, and `pubsub`.
  > Note: Clients blocked by the `MONITOR` command belong to the `normal` class.

- **`ID client-id [client-id ...]`**: Returns entries for clients with IDs matching one or more `client-id` arguments.

- **`USER user`**: Filters the list to include only clients authenticated as the specified user.

- **`ADDR ip:port`**: Filters the list to include only clients connected from the specified address and port.

- **`LADDR ip:port`**: Filters the list to include only clients connected to the specified local address and port.

- **`SKIPME yes|no`**: Filters whether the list should skip the client making the request.
    - `yes`: Skips the client making the request.
    - `no`: Includes the client making the request.

- **`MAXAGE milliseconds`**: Filters the list to include only clients whose connection age (time since the client was created) is greater than or equal to the specified number of milliseconds.
  > Note: This is actually a minimum age, not a maximum age. This filter was first added to CLIENT KILL, where the intention was to keep clients of a maximum age and kill the ones newer than the max age.

Filters can be combined to perform more precise searches. The command will handle multiple filters via logical AND.

Here is the meaning of the fields:

* `id`: a unique 64-bit client ID
* `addr`: address/port of the client
* `laddr`: address/port of local address client connected to (bind address)
* `fd`: file descriptor corresponding to the socket
* `name`: the name set by the client with `CLIENT SETNAME`
* `age`: total duration of the connection in seconds
* `idle`: idle time of the connection in seconds
* `flags`: client flags (see below)
* `capa`: client capabilities (see below). Added in Valkey 8.1
* `db`: current database ID
* `sub`: number of channel subscriptions
* `psub`: number of pattern matching subscriptions
* `ssub`: number of shard channel subscriptions.
* `multi`: number of commands in a MULTI/EXEC context
* `watch`: number of keys this client is currently watching. Added in Valkey 8.0
* `qbuf`: query buffer length (0 means no query pending)
* `qbuf-free`: free space of the query buffer (0 means the buffer is full)
* `argv-mem`: incomplete arguments for the next command (already extracted from query buffer)
* `multi-mem`: memory is used up by buffered multi commands.
* `obl`: output buffer length
* `oll`: output list length (replies are queued in this list when the buffer is full)
* `omem`: output buffer memory usage
* `tot-mem`: total memory consumed by this client in its various buffers
* `events`: file descriptor events (see below)
* `cmd`: last command played
* `user`: the authenticated username of the client
* `redir`: client id of current client tracking redirection
* `resp`: client RESP protocol version.
* `lib-name`: The client library name as set by `CLIENT SETINFO`
* `lib-version`: The client library version as set by `CLIENT SETINFO`
* `tot-net-in`: Total network input bytes read from this client. Added in Valkey 8.0
* `tot-net-out`: Total network output bytes sent to this client. Added in Valkey 8.0
* `tot-cmds`: Total count of commands this client executed. Added in Valkey 8.0

The client flags can be a combination of:

```
A: connection to be closed ASAP
b: the client is waiting in a blocking operation
c: connection to be closed after writing entire reply
d: a watched keys has been modified - EXEC will fail
e: the client is excluded from the client eviction mechanism
i: the client is waiting for a VM I/O (deprecated)
M: the client is a primary
N: no specific flag set
O: the client is a client in MONITOR mode
P: the client is a Pub/Sub subscriber
r: the client is in readonly mode against a cluster node
S: the client is a replica node connection to this instance
u: the client is unblocked
U: the client is connected via a Unix domain socket
x: the client is in a MULTI/EXEC context
t: the client enabled keys tracking in order to perform client side caching
T: the client will not touch the LRU/LFU of the keys it accesses
R: the client tracking target client is invalid
B: the client enabled broadcast tracking mode
I: the client is an import source
```

Client's capabilities can be:

```
r: the client can handle redirect messages
```

The file descriptor events can be:

```
r: the client socket is readable (event loop)
w: the client socket is writable (event loop)
```

## Examples

```bash
CLIENT LIST TYPE normal USER admin MAXAGE 5000 ID 1234 5678
```

## Notes

New fields are regularly added for debugging purpose. Some could be removed
in the future. A version safe Valkey client using this command should parse
the output accordingly (i.e. handling gracefully missing fields, skipping
unknown fields).

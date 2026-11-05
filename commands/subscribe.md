Subscribes the client to the specified channels.

Once the client enters the subscribed state it is not supposed to issue any
other commands, except for additional `SUBSCRIBE`, [`SSUBSCRIBE`](ssubscribe.md), [`PSUBSCRIBE`](psubscribe.md), [`UNSUBSCRIBE`](unsubscribe.md), [`SUNSUBSCRIBE`](sunsubscribe.md), 
[`PUNSUBSCRIBE`](punsubscribe.md), [`PING`](ping.md), [`RESET`](reset.md) and [`QUIT`](quit.md) commands.
However, if RESP3 is used (see [`HELLO`](hello.md)) it is possible for a client to issue any commands while in subscribed state.

Note that [`RESET`](reset.md) can be called to exit subscribed state.

For more information, see [Pub/sub](../topics/pubsub.md).

## Reply

When successful, this command doesn't return anything. Instead, for each channel, one message with the first element being the string `subscribe` is pushed as a confirmation that the command succeeded.

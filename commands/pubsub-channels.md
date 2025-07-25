Lists the currently *active channels*.

An active channel is a Pub/Sub channel with one or more subscribers (excluding clients subscribed to patterns).

If no `pattern` is specified, all the channels are listed, otherwise if pattern is specified only channels matching the specified glob-style pattern are listed.

Cluster note: in a Valkey Cluster clients can subscribe to every node, and can also publish to every other node. The cluster will make sure that published messages are forwarded as needed. That said, the replies from [`PUBSUB`](pubsub.md) in a cluster only report information from the node's Pub/Sub context, rather than the entire cluster.

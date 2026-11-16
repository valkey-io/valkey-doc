Returns the number of subscribers for the specified shard channels.

Note that it is valid to call this command without channels, in this case it will just return an empty list.

Cluster note: in a Valkey Cluster, the replies from [`PUBSUB`](pubsub.md) in a cluster only report information from the node's Pub/Sub context, rather than the entire cluster.

## Reply

Array: the number of subscribers per shard channel, each even element (including the 0th) is channel name, each odd element is the number of subscribers.

## Examples

```
> PUBSUB SHARDNUMSUB orders
1) "orders"
2) (integer) 1
```

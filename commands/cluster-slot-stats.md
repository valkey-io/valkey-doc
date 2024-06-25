`CLUSTER SLOT-STATS` returns an array of slot usage statistics for slots assigned to the current shard.
The command is suitable for Valkey Cluster users aiming to assess general slot usage trends, identify hot / cold slots, migrate slots for a balanced cluster workload, and / or re-write application logic to better utilize slots.

As of now, the following metrics are supported:
* key-count

## Supported arguments
There exist two mutually exclusive arguments, namely;

### SLOTSRANGE
Returns slot statistics based on the slots range provided.
The `SLOTSRANGE` argument allows for request pagination.

```
> CLUSTER SLOT-STATS SLOTSRANGE 0 2
> 1) (integer) 0
> 2) 1) "key-count"
>    2) (integer) 0
> 3) (integer) 1
> 4) 1) "key-count"
>    2) (integer) 0
> 5) (integer) 2
> 6) 1) "key-count"
>    2) (integer) 0
```

### ORDERBY
Orders slot statistics based on the provided metric. Right now, only `key-count` is available.
The `ORDERBY` argument allows for the user to identify hot / cold slots across the cluster.

```
> CLUSTER SLOT-STATS ORDERBY KEY-COUNT LIMIT 3 DESC
> 1) (integer) 12426
> 2) 1) "key-count"
>    2) (integer) 45
> 3) (integer) 13902
> 4) 1) "key-count"
>    2) (integer) 20
> 5) (integer) 2704
> 6) 1) "key-count"
>    2) (integer) 11
```

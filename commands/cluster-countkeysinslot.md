Returns the number of keys in the specified Valkey Cluster hash slot in the
currently selected database. The command only queries the local data set, 
so contacting a node that is not serving the specified hash slot will always 
result in a count of zero being returned.


```
> CLUSTER COUNTKEYSINSLOT 7000
(integer) 50341
```

## Reply

Integer: The number of keys in the specified hash slot, or an error if the hash slot is invalid.

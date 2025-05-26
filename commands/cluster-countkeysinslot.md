Returns the number of keys in the specified Valkey Cluster hash slot in the
currently selected database. For example, if the selected database is 1, the
command returns the total number of keys in the specified slot only in database 1.
The command only queries the local data set, so contacting a node that is not
serving the specified hash slot will always result in a count of zero being returned.

```
> CLUSTER COUNTKEYSINSLOT 7000
(integer) 50341
```

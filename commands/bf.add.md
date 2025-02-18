Adds an item to a bloom filter, if the specified filter does not exist creates a default bloom filter with that name.
## Arguments
* key (required) - A Valkey key of Bloom data type
* item (required) - Item to add

## Examples
```
127.0.0.1:6379> BF.ADD key val
1 
127.0.0.1:6379> BF.ADD key val
0
```

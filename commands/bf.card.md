Gets the cardinality of a Bloom filter - number of items that have been successfully added to a Bloom filter. 
## Arguments
* key (required) - A Valkey key of Bloom data type

## Examples
```
127.0.0.1:6379> BF.ADD key val
1
127.0.0.1:6379> BF.CARD key
1
127.0.0.1:6379> BF.CARD missing
0
```
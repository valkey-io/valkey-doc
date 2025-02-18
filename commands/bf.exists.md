Determines if a specified item has been added to the specified bloom filter.
Syntax

## Arguments
* key (required) -  A Valkey key of Bloom data type
* item (required) -  The item that we are checking if it exists in the bloom object

## Examples
```
127.0.0.1:6379> BF.ADD key val
1
127.0.0.1:6379> BF.EXISTS key val
1
127.0.0.1:6379> BF.EXISTS key missing
0
```

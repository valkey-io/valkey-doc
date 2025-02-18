Determines if one or more items has been added to the specified bloom filter
## Arguments
* key (required) - A Valkey key of Bloom data type
* item (requires at least 1 item but can add as many as desired) -  The item/s that we are checking if it exists in the bloom object
## Examples
```
127.0.0.1:6379> BF.MADD key item1 item2
1) (integer) 1
2) (integer) 1
127.0.0.1:6379> BF.MEXISTS key item1 item2 item3
1) (integer) 1
2) (integer) 1
3) (integer) 0
127.0.0.1:6379> BF.MEXISTS key item1
1) (integer) 1
```
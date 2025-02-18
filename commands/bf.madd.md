Adds one or more items to a Bloom Filter, if the specified filter does not exist creates a default bloom filter with that name.
## Arguments
* key (required) - Is the key name for a Bloom filter to add the item to
* item (requires at least 1 item but can add as many as wanted ) - Is the item/s to add
## Examples
```
127.0.0.1:6379> BF.MADD key item1 item2
1) (integer) 1
2) (integer) 1
127.0.0.1:6379> BF.MADD key item2 item3
1) (integer) 0
2) (integer) 1
127.0.0.1:6379> BF.MADD key_new item1
1) (integer) 1
```
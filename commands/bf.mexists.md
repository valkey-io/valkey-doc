Determines if one or more items has been added to a bloom filter. 

A Bloom filter has two possible responses when you check if an item exists:

* "No" (Definite) - If the filter says an item is NOT present, this is 100% certain. The item is definitely not in the set.

* "Maybe" (Probabilistic) - If the filter says an item IS present, this is uncertain. There's a chance it's a false positive. The item might be in the set, but may not be

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
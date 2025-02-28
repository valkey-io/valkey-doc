Determines if an item has been added to the bloom filter. 

A Bloom filter has two possible responses when you check if an item exists:

* "No" (Definite) - If the filter says an item is NOT present, this is 100% certain. The item is definitely not in the set.

* "Maybe" (Probabilistic) - If the filter says an item IS present, this is uncertain. There's a chance it's a false positive. The item might be in the set, but may not be


## Examples

```
127.0.0.1:6379> BF.ADD key val
1
127.0.0.1:6379> BF.EXISTS key val
1
127.0.0.1:6379> BF.EXISTS key missing
0
```

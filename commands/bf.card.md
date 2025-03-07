Returns the cardinality of a Bloom filter which is the number of items that have been successfully added to it. 

## Examples

```
127.0.0.1:6379> BF.ADD key val
1
127.0.0.1:6379> BF.CARD key
1
127.0.0.1:6379> BF.CARD nonexistentkey
0
```
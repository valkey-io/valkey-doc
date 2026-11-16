Returns the cardinality of a bloom filter which is the number of items that have been successfully added to it. 

## Reply

Integer: The number of items successfully added to the bloom filter, or 0 if the key does not exist

## Examples

```
127.0.0.1:6379> BF.ADD key val
(integer) 1
127.0.0.1:6379> BF.CARD key
(integer) 1
127.0.0.1:6379> BF.CARD nonexistentkey
(integer) 0
```

Determines if an item has been added to the bloom filter previously. 

A bloom filter has two possible responses when you check if an item exists:

* 0 - The item definitely does not exist since with bloom filters, false negatives are not possible.

* 1 - The item exists with a given false positive (`fp`) percentage. There is an `fp` rate % chance that the item does not exist. You can create bloom filters with a more strict false positive rate as needed.

## Reply

One of the following:

* Integer: `1` if the item exists in the bloom filter
* Integer: `0` if the bloom filter does not exist or the item has not been added to the bloom filter

## Examples

```
127.0.0.1:6379> BF.ADD key val
(integer) 1
127.0.0.1:6379> BF.EXISTS key val
(integer) 1
127.0.0.1:6379> BF.EXISTS key nonexistent
(integer) 0
```

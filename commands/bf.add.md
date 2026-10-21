Adds a single item to a bloom filter. If the specified bloom filter does not exist, a bloom filter is created with the provided name with default properties.

To add multiple items to a bloom filter, you can use the [`BF.MADD`](bf.madd.md) or [`BF.INSERT`](bf.insert.md) commands.

To create a bloom filter with non-default properties, use the [`BF.INSERT`](bf.insert.md) or [`BF.RESERVE`](bf.reserve.md) command.

## Reply

One of the following:

* Integer: `1` if the item was successfully added
* Integer: `0` if the item already existed in the bloom filter

An error will occur if input is invalid, if a non bloom filter key with the same name already exists, if the bloom filter creation / scale out exceeds limits, or if an item is being added to a full non scaling filter.

## Examples

```
127.0.0.1:6379> BF.ADD key val
(integer) 1
127.0.0.1:6379> BF.ADD key val
(integer) 0
```

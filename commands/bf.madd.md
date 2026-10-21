Adds one or more items to a bloom filter. If the specified bloom filter does not exist, a bloom filter is created with the provided name with default properties.

If you want to create a bloom filter with non-default properties, use the [`BF.INSERT`](bf.insert.md) or [`BF.RESERVE`](bf.reserve.md) command.

## Reply

Array of integers (`1` or `0`)

An error will occur if input is invalid, if a non bloom filter key with the same name already exists, if the bloom filter creation / scale out exceeds limits, or if an item is being added to a full non scaling filter.

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

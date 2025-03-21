Adds a single item to a bloom filter. If the specified bloom filter does not exist, a bloom filter is created with the provided name with default properties.

To add multiple items to a bloom filter, you can use the BF.MADD or BF.INSERT commands.

If you want to create a bloom filter with non-default properties, use the `BF.INSERT` or `BF.RESERVE` command.

## Examples

```
127.0.0.1:6379> BF.ADD key val
1 
127.0.0.1:6379> BF.ADD key val
0
```

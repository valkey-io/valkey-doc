Adds an item to a bloom filter, if the specified bloom filter does not exist creates a bloom filter with default configurations with that name.

If you want to create a bloom filter with non-standard options, use the `BF.INSERT` or `BF.RESERVE` command.

## Examples

```
127.0.0.1:6379> BF.ADD key val
1 
127.0.0.1:6379> BF.ADD key val
0
```

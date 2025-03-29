<<<<<<< HEAD
<<<<<<< HEAD
Adds one or more items to a bloom filter. If the specified bloom filter does not exist, a bloom filter is created with the provided name with default properties.
=======
Adds one or more items to a bloom filter. If the specified bloom filter does not exist, a bloom filter is created with the provided name with default properties
>>>>>>> f062a8a0 (Changes based on feedback for bloom commands and documentation)
=======
Adds one or more items to a bloom filter. If the specified bloom filter does not exist, a bloom filter is created with the provided name with default properties.
>>>>>>> 8e1f3649 (Apply suggestions from code review)

If you want to create a bloom filter with non-default properties, use the `BF.INSERT` or `BF.RESERVE` command.

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
Creates an empty bloom object with the capacity and false positive rate specified

## Reserve fields

* error_rate - The false positive rate the bloom filter will be created with
* capacity -  The starting capacity the bloom filter will be created with
* EXPANSION expansion - The rate in which filters will increase by
* NONSCALING - Setting this will make it so the bloom object can’t expand past its initial capacity

## Examples

```
127.0.0.1:6379> BF.RESERVE key 0.01 1000
OK
127.0.0.1:6379> BF.RESERVE key 0.1 1000000
(error) ERR item exists
```
```
127.0.0.1:6379> BF.RESERVE bf_expansion 0.0001 5000 EXPANSION 3
OK
```
```
127.0.0.1:6379> BF.RESERVE bf_nonscaling 0.0001 5000 NONSCALING
OK
```

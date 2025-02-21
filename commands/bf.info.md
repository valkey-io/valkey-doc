Returns information about a bloom filter

## Info Fields

* CAPACITY - Returns the number of unique items that would need to be added before scaling would happen
* SIZE - Returns the number of bytes allocated
* FILTERS - Returns the number of filters in the specified key
* ITEMS - Returns the number of unique items that have been added the the bloom filter
* ERROR - Returns the false positive rate for the bloom filter
* EXPANSION - Returns the expansion rate
* MAXSCALEDCAPACITY - Returns the maximum capacity that can be reached before an error occurs

If none of the optional fields are specified, all the fields will be returned. MAXSCALEDCAPACITY will be an unrecognized argument on non scaling filters
 
## Examples

```
127.0.0.1:6379> BF.ADD key val
1
127.0.0.1:6379> BF.INFO key
 1) Capacity
 2) (integer) 100
 3) Size
 4) (integer) 384
 5) Number of filters
 6) (integer) 1
 7) Number of items inserted
 8) (integer) 2
 9) Error rate
10) "0.01"
11) Expansion rate
12) (integer) 2
13) Max scaled capacity
14) (integer) 26214300
127.0.0.1:6379> BF.INFO key CAPACITY
100
```
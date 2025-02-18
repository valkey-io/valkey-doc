Creates a bloom object with the specified parameters. If a parameter is not specified then the default value will be used. If ITEMS is specified then it will also attempt to add all items specified after

## Arguments
Due to the nature of  NONSCALING and VALIDATESCALETO arguments, specifying NONSCALING and VALIDATESCALETO isn't allowed
* key (required) - Is the key name for a Bloom filter to add the item to
* CAPACITY capacity (optional) -  capacity for the inital bloom filter
* ERROR fp_error (optional)- The false positive rate for the bloom filter
* EXPANSION expansion(optional) - The expansion rate for a scaling filter
* NOCREATE (optional) - Will not create the bloom filter and add items if the filter does not exist already
* TIGHTENING (optional) - The tightening ratio for the bloom filter
* SEED (optional) - The seed the hash functions will use
* NONSCALING (optional) - Will make it so the filter can not scale
* VALIDATESCALETO validatescaleto (optional) - Checks if the filter could scale to this capacity and if not show an error and don’t create the bloom filter
* ITEMS (optional) - Items we will add to the bloom filter

## Examples
```
127.0.0.1:6379> BF.INSERT key ITEMS item1 item2
1) (integer) 1
2) (integer) 1
# This does not update the capcity but uses the origianl filters values
127.0.0.1:6379> BF.INSERT key CAPACITY 1000 ITEMS item2 item3
1) (integer) 0
2) (integer) 1
127.0.0.1:6379> BF.INSERT key_new CAPACITY 1000
[]
```

```
127.0.0.1:6379> BF.INSERT key NONSCALING VALIDATESCALETO 100
cannot use NONSCALING and VALIDATESCALETO options together
127.0.0.1:6379> BF.INSERT key CAPACITY 1000  VALIDATESCALETO 999999999999999999999 ITEMS item2 item3
provided VALIDATESCALETO causes bloom object to exceed memory limit
127.0.0.1:6379> BF.INSERT key VALIDATESCALETO 999999999999999999999 EXPANSION 1 ITEMS item2 item3
provided VALIDATESCALETO causes false positive to degrade to 0
```
```
127.0.0.1:6379> BF.INSERT key NOCREATE ITEMS item1 item2
not found
```
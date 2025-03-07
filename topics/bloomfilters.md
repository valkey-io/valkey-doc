---
title: "Bloom Filters"
description: >
    Introduction to Bloom Filters
---

The bloom filter data type is taken from a [separate module](https://github.com/valkey-io/valkey-bloom) that users will need to install in order to use. 

Bloom filters are a space efficient probabilistic data structure that allows checking whether an element is member of a set. False positives are possible, but it guarantees no false negatives.

## Basic Bloom commands

* `BF.ADD` adds an item to a bloom filter
* `BF.CARD` returns the cardinality of a bloom filter
* `BF.EXISTS` checks if an item has been added to a bloom filter
* `BF.INFO` returns information about a bloom filter

See the [complete list of bloom filter commands](../commands/#bloom).

## Common use cases for bloom filters

### Financial fraud detection

Bloom filters can help answer the question "Has this card been flagged as stolen?", use a bloom filter that has cards reported stolen added to it. Check a card on use that it is not present in the bloom filter. If it isn't then the card is not marked as stolen, if present then a check to the main database can happen or deny the purchase.

### Ad placement

Bloom filters can help answer the following questions to advertisers:
* Has the user already seen this ad?
* Has the user already bought this product?

Use a Bloom filter for every user, storing all bought products. The recommendation engine can then suggest a new product and checks if the product is in the user's Bloom filter.

* If no, the ad is shown to the user and is added to the Bloom filter.
* If yes, the process restarts and repeats until it finds a product that is not present in the filter.

### Check if URL's are malicious

Bloom filters can answer the question "is a URL malicious?". Any URL inputted would be checked against a malicious URL bloom filter. 

* If no then we allow access to the site
* If yes then we can deny access or perform a full check of the URL

### Check if a username is taken

Bloom filters can answer the question: Has this username/email/domain name/slug already been used?

For example for usernames. Use a Bloom filter for every username that has signed up. A new user types in the desired username. The app checks if the username exists in the Bloom filter.

* If no, the user is created and the username is added to the Bloom filter.
* If yes, the app can decide to either check the main database or reject the username.

## Scaling and non scaling bloom filters

The difference between scaling and non scaling bloom filters is that scaling bloom filters do not have a fixed capacity, but a capacity that can grow. While non-scaling bloom filters will have a fixed capacity which also means a fixed size. 

When a scaling filter reaches its capacity, adding a new unique item will cause a new bloom filter to be created and added to the vector of bloom filters. This new bloom filter will have a larger capacity (previous bloom filter's capacity * expansion rate of the bloom object).

When a non scaling filter reaches its capcity, if a user tries to add a new unique item an error will be returned

The expansion rate is the rate that a scaling bloom filter will have its capacity increased by on the scale out. For example we have a bloom filter with capacity 100 at creation with an expansion rate of 2. After adding 101 unique items we will scale out and create a new filter with capacity 200. Then after adding 200 more unique items (301 items total) we will create a new filter of capacity 400 and so on. 

### When should you use scaling vs non-scaling filters

If the data size is known and fixed then using a non-scaling bloom filter is preferred, for example a static dictionary could use a non scaling bloom filter as the amount of items should be fixed. Likewise the reverse case for dynamic data and unknown final sizes is when you should use a scaling bloom filters.   

## Default bloom properties

Capacity - 100

Error rate - 0.01

Expansion - 2

As bloom filters have a default expansion of 2 this means all default bloom objects will be scaling. These options are used when not specified explicitly in the commands used to create a new bloom object. For example doing a BF.ADD for a new filter will create a filter with the exact above qualities. These default properties can be configured through configs on the bloom module.
Example of default bloom objects information:

```
127.0.0.1:6379> BF.ADD default_filter item
1
127.0.0.1:6379> BF.INFO default_filter
 1) Capacity
 2) (integer) 100
 3) Size
 4) (integer) 384
 5) Number of filters
 6) (integer) 1
 7) Number of items inserted
 8) (integer) 1
 9) Error rate
10) "0.01"
11) Expansion rate
12) (integer) 2
13) Max scaled capacity
14) (integer) 26214300
```

### Advanced Properties

Seed - The seed used by the bloom filter can be specified by the user in the BF.INSERT command. This property is only useful if you have a specific 32 byte seed that you want your bloom filter to use. By defualt every bloom filter will use a random seed. 

Tightening Ratio - We do not recommend fine tuning this unless there is a specific use case for lower memory usage with higher false positive or vice versa. 

## Performance

Most bloom commands are O(n * k) where n is the number of hash functions used by the bloom filter and k is the number of elements being inserted. This means that both BF.ADD and BF.EXISTS are both O(n) as they only work with one 1 item.

There are a few bloom commands that are O(1): BF.CARD, BF.INFO, BF.RESERVE, and BF.INSERT (if no items are specified). These commands have constant time complexity since they don't work on items but instead work on the data about the bloom filter itself.

## Limits

The consumption of memory by a single Bloom object is limited to a default of 128 MB (configurable in the bloom module), which is the size of the in-memory data structure not the capacity of the Bloom object. You can check the amount of memory consumed by a Bloom object by using the BF.INFO command. When a bloom filter scales out it will add another filter, there is a limit on the number of filters that can be added. This filter limit will change depending on the false positive rate, capacity, expansion and tightening ratio, where this filter limit is specified on the memory limit of the bloom objects.

We have implemented an optional argument into BF.INSERT (VALIDATESCALETO) that can help you determine the max capacity of the objects on creation. The VALIDATESCALETO when specified would check a few things, the first is that when a bloom filter has scaled out to the desired capacity will the tightening ratio reach zero, and if so we will reject the creation. The second thing it will check is that once we reach the capacity that is desired will the bloom object be less than the max memory limit (by default 128 MB).

There is also a way to check the max capacity that can be reached for Bloom objects. Using MAXSCALEDCAPACITY in BF.INFO will provide the exact capacity that the bloom object can reach.

Example usage for a default bloom object:
```
127.0.0.1:6379> BF.INSERT validate_scale_fail VALIDATESCALETO 26214301
(error) ERR provided VALIDATESCALETO causes bloom object to exceed memory limit
127.0.0.1:6379> BF.INSERT validate_scale_valid VALIDATESCALETO 26214300
[]
127.0.0.1:6379> BF.INFO validate_scale_valid MAXSCALEDCAPACITY
(integer) 26214300
```

As you can see above when trying to create a bloom object that the user wants to achieve a capacity more than what is possible given the memory limits the command will output an error and not create the bloom object. However if the wanted capacity is within the limits then the creation of the bloom object will succeed.  

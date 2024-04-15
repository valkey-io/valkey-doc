---
title: "Understand Redis data types"
linkTitle: "Understand data types"
description: Overview of data types supported by Redis
weight: 35
aliases:
    - /docs/manual/data-types
    - /topics/data-types
    - /docs/data-types/tutorial
---

Redis is a data structure server.
At its core, Redis provides a collection of native data types that help you solve a wide variety of problems, from [caching](/docs/manual/client-side-caching/) to [queuing](/docs/data-types/lists/) to [event processing](/docs/data-types/streams/).
Below is a short description of each data type, with links to broader overviews and command references.

If you'd like to try a comprehensive tutorial for each data structure, see their overview pages below.


## Core

### Strings 

[Strings](/docs/data-types/strings) are the most basic Redis data type, representing a sequence of bytes.
For more information, see:

* [Overview of Strings](/docs/data-types/strings/)
* [String command reference](/commands/?group=string)

### Lists

[Lists](/docs/data-types/lists) are lists of strings sorted by insertion order.
For more information, see:

* [Overview of Lists](/docs/data-types/lists/)
* [List command reference](/commands/?group=list)

### Sets

[Sets](/docs/data-types/sets) are unordered collections of unique strings that act like the sets from your favorite programming language (for example, [Java HashSets](https://docs.oracle.com/javase/7/docs/api/java/util/HashSet.html), [Python sets](https://docs.python.org/3.10/library/stdtypes.html#set-types-set-frozenset), and so on).
With a Set, you can add, remove, and test for existence in O(1) time (in other words, regardless of the number of set elements).
For more information, see:

* [Overview of Sets](/docs/data-types/sets/)
* [Set command reference](/commands/?group=set)

### Hashes

[Hashes](/docs/data-types/hashes) are record types modeled as collections of field-value pairs.
As such, Hashes resemble [Python dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries), [Java HashMaps](https://docs.oracle.com/javase/8/docs/api/java/util/HashMap.html), and [Ruby hashes](https://ruby-doc.org/core-3.1.2/Hash.html).
For more information, see:

* [Overview of Hashes](/docs/data-types/hashes/)
* [Hashes command reference](/commands/?group=hash)

### Sorted sets

[Sorted sets](/docs/data-types/sorted-sets) are collections of unique strings that maintain order by each string's associated score.
For more information, see:

* [Overview of Sorted sets](/docs/data-types/sorted-sets)
* [Sorted set command reference](/commands/?group=sorted-set)

### Streams

A [Stream](/docs/data-types/streams) is a data structure that acts like an append-only log.
Streams help record events in the order they occur and then syndicate them for processing.
For more information, see:

* [Overview of Streams](/docs/data-types/streams)
* [Streams command reference](/commands/?group=stream)

### Geospatial indexes

[Geospatial indexes](/docs/data-types/geospatial) are useful for finding locations within a given geographic radius or bounding box.
For more information, see:

* [Overview of Geospatial indexes](/docs/data-types/geospatial/)
* [Geospatial indexes command reference](/commands/?group=geo)

### Bitmaps

[Bitmaps](/docs/data-types/bitmaps/) let you perform bitwise operations on strings. 
For more information, see:

* [Overview of Bitmaps](/docs/data-types/bitmaps/)
* [Bitmap command reference](/commands/?group=bitmap)

### Bitfields

[Bitfields](/docs/data-types/bitfields/) efficiently encode multiple counters in a string value.
Bitfields provide atomic get, set, and increment operations and support different overflow policies.
For more information, see:

* [Overview of Bitfields](/docs/data-types/bitfields/)
* The `BITFIELD` command.

### HyperLogLog

The [HyperLogLog](/docs/data-types/hyperloglogs) data structures provide probabilistic estimates of the cardinality (i.e., number of elements) of large sets. For more information, see:

* [Overview of HyperLogLog](/docs/data-types/hyperloglogs)
* [HyperLogLog command reference](/commands/?group=hyperloglog)

## Extensions

To extend the features provided by the included data types, use one of these options:

1. Write your own custom [server-side functions in Lua](/docs/manual/programmability/).
1. Write your own Redis module using the [modules API](/docs/reference/modules/) or check out the [community-supported modules](/docs/modules/).

<hr>

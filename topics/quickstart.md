---
title: "Valkey as an in-memory data structure store quick start guide"
linkTitle: "Data structure store"
weight: 1
description: Understand how to use basic Valkey data types
---

This quick start guide shows you how to:

1. Get started with Valkey 
2. Store data under a key in Valkey
3. Retrieve data with a key from Valkey
4. Scan the keyspace for keys that match a specific pattern

The examples in this article refer to a simple bicycle inventory.

## Setup

See the [installation guides](installation.md) to install Valkey on your local machine.

## Connect

The first step is to connect to Valkey. There are client connectors for [most programming languages](../clients/).
You can also connect using [valkey-cli](cli.md), the command line interface.
The following example shows how to connect to a Valkey server that runs on localhost (`-h 127.0.0.1`) and listens on the default port (`-p 6379`):

```sh
$ valkey-cli -h 127.0.0.1 -p 6379
```

## Store and retrieve data

Valkey stands for Remote Dictionary Server. You can use the same data types as in your local programming environment but on the server side within Valkey.

Similar to byte arrays, Strings store sequences of bytes, including text, serialized objects, counter values, and binary arrays. The following example shows you how to set and get a string value:

```valkey-cli
127.0.0.1:6379> SET bike:1 "Process 134"
OK
127.0.0.1:6379> GET bike:1
"Process 134"
```

Hashes are the equivalent of dictionaries (dicts or hash maps). Among other things, you can use hashes to represent plain objects and to store groupings of counters. The following example explains how to set and access field values of an object:

```valkey-cli
127.0.0.1:6379> HSET bike:1 model Deimos brand Ergonom type 'Enduro bikes' price 4972
(integer) 4
127.0.0.1:6379> HGET bike:1 model
"Deimos"
127.0.0.1:6379> HGET bike:1 price
"4972"
127.0.0.1:6379> HGETALL bike:1
1) "model"
2) "Deimos"
3) "brand"
4) "Ergonom"
5) "type"
6) "Enduro bikes"
7) "price"
8) "4972"
```

You can get a complete overview of available data types in this documentation site's [data types section](data-types.md). Each data type has commands allowing you to manipulate or retrieve data. The [commands reference](../commands/) provides a sophisticated explanation.

## Scan the keyspace

Each item within Valkey has a unique key. All items live within the Valkey [keyspace](keyspace.md). You can scan the Valkey keyspace via the [SCAN command](../commands/scan.md). Here is an example that scans for the first 100 keys that have the prefix `bike:`:

```valkey-cli
127.0.0.1:6379> SCAN 0 MATCH "bike:*" COUNT 100
1) "0"
2) 1) "bike:4"
   2) "bike:3"
   3) "bike:5"
   4) "bike:1"
   5) "bike:2"
```

[SCAN](../commands/scan.md) returns a cursor position, allowing you to scan iteratively for the next batch of keys until you reach the cursor value 0.

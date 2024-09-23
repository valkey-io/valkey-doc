---
title: "Valkey geospatial"
linkTitle: "Geospatial"
description: >
    Introduction to the Valkey Geospatial data type
---

Geospatial indexes let you store coordinates and search for them.
This data structure is useful for finding nearby points within a given radius or bounding box.

## Basic commands

* `GEOADD` adds a location to a given geospatial index (note that longitude comes before latitude with this command).
* `GEOSEARCH` returns locations with a given radius or a bounding box.

See the [complete list of geospatial index commands](../commands/#geo).


## Examples

Suppose you're building a mobile app that lets you find all of the bike rental stations closest to your current location.

Add several locations to a geospatial index:
```
127.0.0.1:6379> GEOADD bikes:rentable -122.27652 37.805186 station:1
(integer) 1
127.0.0.1:6379> GEOADD bikes:rentable -122.2674626 37.8062344 station:2
(integer) 1
127.0.0.1:6379> GEOADD bikes:rentable -122.2469854 37.8104049 station:3
(integer) 1
```

Find all locations within a 5 kilometer radius of a given location, and return the distance to each location:
```
127.0.0.1:6379> GEOSEARCH bikes:rentable FROMLONLAT -122.2612767 37.7936847 BYRADIUS 5 km WITHDIST
1) 1) "station:1"
   2) "1.8523"
2) 1) "station:2"
   2) "1.4979"
3) 1) "station:3"
   2) "2.2441"
```

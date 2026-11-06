---
title: "Path Hashes"
description: Store field-value records at byte paths and query them by prefix
---

Available since Valkey 9.2.

A Path Hash stores multiple records under one Valkey key.
Each record has a **path** and a map of **fields** to **values**.
For example, a routing table might store a default backend at `app` and a different backend at `app/api`.
The paths share a prefix, but each has its own fields.

## Store and read records

Use [`PHSET`](../commands/phset.md) to write one path and [`PHMSET`](../commands/phmset.md) to write multiple paths at the same key in one atomic operation.
Each `FIELDS` group specifies the number of field-value pairs that follow.

```
> PHMSET routes app FIELDS 1 backend main app/api FIELDS 1 backend api
OK
> PHGET routes app/api backend
1) "api"
> PHGET routes app/api/v1 backend
1) (nil)
```

[`PHGET`](../commands/phget.md), [`PHGETALL`](../commands/phgetall.md), [`PHMGET`](../commands/phmget.md), and [`PHPATHEXISTS`](../commands/phpathexists.md) use exact paths.
A prefix shared by several paths only exists as a record if it has fields of its own.

`PHSET` can apply a condition to the entire set of fields at a path.
Use `FNX` to write only if all the named fields are absent, or `FXX` to write only if all of them exist.
If any field fails the condition, the command returns null and writes nothing.

## Find ancestors and descendants

[`PHPREFIXES`](../commands/phprefixes.md) finds stored paths that are prefixes of a query, from longest to shortest.
Use `COUNT 1` for the longest match, or omit it to get all matching ancestors.
In the routing example, you can ask for the nearest backend in a single call:

```
> PHPREFIXES routes app/api/v1 COUNT 1 FIELDS 1 backend
1) 1) "app/api"
   2) 1) "api"
```

Paths, fields, and values are binary-safe strings.
Prefix matching compares bytes and has no special handling for separators.
For example, `app` matches both `app/api` and `apple`.
For slash-separated paths, use `app/` when scanning descendants under that directory boundary.
The empty path is valid and, if stored, serves as a default ancestor for every query.

To go in the other direction, use `PREFIX` with [`PHPATHSCAN`](../commands/phpathscan.md) or [`PHPATHCOUNT`](../commands/phpathcount.md).
They list or count stored paths that start with the supplied bytes, including the exact path if present.
Counting with a nonempty prefix traverses the matching paths.

## Iterate over paths and fields

* [`PHPATHSCAN`](../commands/phpathscan.md) lists paths in byte lexicographic order.
  Its `COUNT` sets a maximum page size, and its cursor is an opaque string that resumes after the last path returned.
* [`PHSCAN`](../commands/phscan.md) scans field-value pairs at a single exact path.
  It uses a numeric cursor like [`HSCAN`](../commands/hscan.md), supports glob filtering of field names with `MATCH`, and treats `COUNT` as a work hint.

Start both scans with `0`, reuse each returned cursor with the same key and filter, and stop when the returned cursor is `0`.
Neither scan takes a snapshot, so changes during iteration can affect which entries are returned.

## Delete records and expire keys

[`PHDEL`](../commands/phdel.md) removes specified fields, or the entire exact path if no fields are specified.
Removing the last field at a path removes that path.
[`PHPATHDEL`](../commands/phpathdel.md) removes an exact path, and `WITHSUBPATHS` also removes every path that starts with the given bytes.
With an empty path and `WITHSUBPATHS`, it removes the entire tree.

When the last path is removed, Valkey deletes the top-level key.
An expiration set with [`EXPIRE`](../commands/expire.md) applies to the entire key.

## Choose a data type

Use a Path Hash when records have their own fields and you need to query related paths by prefix.
For example, a routing table can find a fallback record among the ancestors of a request path, and a prefix cache index can store worker placement metadata at each cached prefix.
Use a [Hash](hashes.md) when one flat map of fields is enough, or a [Sorted Set](sorted-sets.md) when you need score-based ordering or ranges.

## Server integration

[`TYPE`](../commands/type.md) and [`OBJECT ENCODING`](../commands/object-encoding.md) report `pathhash`.
Use `SCAN TYPE pathhash` to discover keys and the [ACL](acl.md) category `@pathhash` to control access to Path Hash commands.
Enable the `p` [keyspace notification flag](notifications.md) to subscribe to Path Hash command events.

Path Hash keys support [RDB and AOF persistence](persistence.md).
For RDB readers, the Path Hash object type is 23, introduced in RDB format version 81.
For modules, [`ValkeyModule_KeyType()`](modules-api-ref.md#ValkeyModule_KeyType) returns `VALKEYMODULE_KEYTYPE_PATH_HASH` for a Path Hash key.

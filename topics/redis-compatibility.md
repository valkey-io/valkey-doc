---
title: Redis compatibility
description: How Valkey maintains compatibility with Redis OSS
---

Valkey is a fork of Redis OSS 7.2.4 and maintains backward compatibility with Redis OSS 7.2 and all earlier open-source Redis versions.
This page describes how Valkey handles compatibility at the protocol, API, and scripting levels.

## Version compatibility

Valkey 7.2.4 was forked from Redis 7.2.4.
All commands, data structures, and behaviors present in Redis OSS 7.2.4 work the same way in Valkey.

Valkey versions 8.0 and later add new features on top of this base.
These features are Valkey-specific and are not present in Redis OSS.

Redis Community Edition (CE) 7.4 and later are not open source and are not compatible with Valkey.
Data files produced by Redis CE 7.4+ cannot be loaded by Valkey.

For migration steps, refer to [Migration from Redis to Valkey](migration.md).

## Protocol compatibility

Valkey uses the same RESP (REdis Serialization Protocol) wire protocol as Redis, supporting both RESP2 and RESP3.
Existing Redis client libraries (such as Jedis, redis-py, node-redis, ioredis, and go-redis) connect to Valkey without code changes.

## Persistence format compatibility

Valkey reads and writes the same RDB and AOF file formats as Redis OSS 7.2.
You can copy an RDB snapshot from Redis OSS to Valkey and load it directly.
RDB files produced by Redis CE 7.4+ are not compatible.

## Configuration compatibility

Valkey accepts Redis-style configuration files.
An existing `redis.conf` can be used as-is with `valkey-server`.
Configuration directives are the same as Redis OSS 7.2, with additional Valkey-specific options for new features.

## CLI compatibility

The `redis-cli` tool works with Valkey servers, and `valkey-cli` works with Redis OSS servers.
Both tools use the same RESP protocol and command set.

## The `redis_version` and `server_name` INFO fields

To maintain compatibility with existing clients and tools that check the server version, Valkey reports a fixed `redis_version` field in the [INFO](../commands/info.md) server output:

```
redis_version:7.2.4
```

This value does not change across Valkey releases.
Clients and libraries that rely on `redis_version` to detect feature support continue to work without modification.

The actual Valkey version is reported in separate fields:

```
server_name:valkey
valkey_version:8.1.1
```

Use `valkey_version` to check the Valkey version.
Use `redis_version` only for backward compatibility with Redis-era tooling.

## Lua scripting compatibility

Valkey supports both the `redis` and `server` namespaces in Lua scripts and functions.
The following calls are equivalent:

```lua
-- Redis-style (backward compatible)
redis.call('SET', 'key', 'value')
redis.pcall('GET', 'key')
redis.log(redis.LOG_NOTICE, 'message')
redis.status_reply('OK')
redis.error_reply('ERR something')

-- Valkey-style
server.call('SET', 'key', 'value')
server.pcall('GET', 'key')
server.log(server.LOG_NOTICE, 'message')
server.status_reply('OK')
server.error_reply('ERR something')
```

Existing Lua scripts that use `redis.call()` and `redis.pcall()` work without changes.
New scripts can use either namespace.

Valkey also provides Lua globals for version detection:

- `SERVER_NAME` - returns `"valkey"`
- `SERVER_VERSION` - returns the Valkey version string (e.g. `"8.1.1"`)
- `SERVER_VERSION_NUM` - returns the Valkey version as a number (e.g. `0x00080101`)

The Redis-era globals (`REDIS_VERSION`, `REDIS_VERSION_NUM`) remain available and return the fixed Redis compatibility version (`7.2.4`).

## Module API compatibility

Valkey supports both the `RedisModule_` and `ValkeyModule_` prefixed APIs for modules.
The header files `redismodule.h` and `valkeymodule.h` are both available.

Modules written for Redis OSS using the `RedisModule_` API work in Valkey without modification.
New modules can use either API prefix.

For example, both of these are valid:

```c
// Redis-style (backward compatible)
int RedisModule_OnLoad(RedisModuleCtx *ctx, RedisModuleString **argv, int argc) {
    if (RedisModule_Init(ctx, "mymodule", 1, REDISMODULE_APIVER_1) == REDISMODULE_ERR)
        return REDISMODULE_ERR;
    return REDISMODULE_OK;
}

// Valkey-style
int ValkeyModule_OnLoad(ValkeyModuleCtx *ctx, ValkeyModuleString **argv, int argc) {
    if (ValkeyModule_Init(ctx, "mymodule", 1, VALKEYMODULE_APIVER_1) == VALKEYMODULE_ERR)
        return VALKEYMODULE_ERR;
    return VALKEYMODULE_OK;
}
```

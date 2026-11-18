---
title: "Valkey Large Object - Use Cases and Examples"
description: Common use cases and worked examples for the Valkey Large Object module
---

> **Note:** [valkey-large-object](https://github.com/valkey-io/valkey-large-object) is at version 0.x.
> Commands, arguments, replies, and configuration can change before version 1.0.

This page shows common patterns for the large object module.
The TCP examples use `valkey-cli`.
The RDMA examples show the flow of an RDMA-capable client, because `valkey-cli` cannot do RDMA transfers.
See [Valkey Large Object - RDMA Transfers](large-object-rdma.md) for the details of each RDMA step.

## Common use cases

### Offload and share an LLM inference KV cache

Large language model (LLM) inference engines calculate attention key/value tensors (the KV cache) for each prompt prefix.
When GPU memory is full, the engine discards blocks of this cache, and it must calculate them again when a similar prompt comes.
A cache connector in the inference engine can store the blocks in Valkey instead.
Other GPU servers that connect to the same Valkey nodes can then use the blocks again.

A common key pattern is a hash of the token prefix and the model identity, for example `kv:<model>:<prefix-hash>:<layer-range>`.
With RDMA, the server writes each block directly into a registered host buffer of the inference engine.
GPU memory (`FI_HMEM`) is not supported as a client buffer.
To read more blocks in parallel, a client can send requests for different keys to many Valkey nodes at the same time.

### Stage model weights, embeddings, and artifacts

Many workers can need the same large artifact at the same time, for example model weight shards, embedding tables, or tokenizer files.
Load each shard into Valkey one time, and let the workers read it from Valkey.
Use `Tiered` mode when the total size of the artifacts is larger than the DRAM that you want to use.
Frequently read objects are then served from the DRAM cache.

### Large blob cache in front of object storage

Applications can put a cache in front of an object store for large immutable blobs, for example images, media segments, or data set files.
On a miss, the application reads the blob from the object store and writes it to Valkey with a TTL.
Later reads come from Valkey.
The module does not persist objects, so the object store stays the source of truth.

## Example: store and read a blob over TCP

Store a file, look at its metadata, and read it again:

```bash
valkey-cli -x BLOB.TCP_SET artifact:tokenizer:v3 < tokenizer.json
valkey-cli BLOB.INFO artifact:tokenizer:v3
```

Use the cache-aside pattern with a TTL.
In this example, the value `123456789` represents the bytes from the object store:

```
127.0.0.1:6379> BLOB.TCP_GET blob:images:4711
(nil)
127.0.0.1:6379> BLOB.TCP_SET blob:images:4711 123456789
OK
127.0.0.1:6379> EXPIRE blob:images:4711 3600
(integer) 1
127.0.0.1:6379> BLOB.INFO blob:images:4711 LEN
(integer) 9
127.0.0.1:6379> TTL blob:images:4711
(integer) 3600
```

To make sure that a blob did not change, compare the CRC32C that your application calculates with the stored value:

```
127.0.0.1:6379> BLOB.INFO blob:images:4711 CRC
(integer) 3808858755
```

In `Tiered` mode, `BLOB.INFO` shows where the object is now:

```
127.0.0.1:6379> BLOB.INFO artifact:tokenizer:v3 TIER
disk
127.0.0.1:6379> BLOB.TCP_GET artifact:tokenizer:v3
"..."
127.0.0.1:6379> BLOB.INFO artifact:tokenizer:v3 TIER
dram
```

With the default `largeobj.promote-min-hits` (1), the first read promotes the object into the DRAM cache.
After the promotion is complete, `TIER` shows `dram`.
Objects larger than `largeobj.max-promote-size` stay on disk.

## Example: KV cache blocks over RDMA

This pseudo-flow shows how a cache connector can store and load KV cache blocks with RDMA.
`fi_*` are libfabric calls in the client.
`valkey.call` sends a Valkey command on one connection.

```
# One time for each Valkey connection
ep        = fi_endpoint(...)
my_addr   = fi_getname(ep)
servers   = valkey.call("BLOB.RDMA_HELLO", hex(my_addr))
for s in servers:
    fi_av_insert(unhex(s))

# One time for each buffer (registration is expensive, so do it at startup)
# Host memory only: GPU memory (FI_HMEM) is not supported
mr        = fi_mr_reg(buffer, buffer_size)
rkey      = fi_mr_key(mr)

# Save one block (the block is in buffer at offset off, size n)
crc       = crc32c(buffer[off : off + n])
valkey.call("BLOB.RDMA_SET", key, n, "CRC", crc, rkey, addr(buffer) + off, n)
# Reply "OK": the server has read all bytes and stored the object

# Load one block into buffer at offset off
reply     = valkey.call("BLOB.RDMA_GET", key, rkey, addr(buffer) + off, n)
if reply is nil:
    # Cache miss: calculate the block again
else:
    obj_len, crc = reply
    # Optional end-to-end check
    assert crc32c(buffer[off : off + obj_len]) == crc
```

One block can span several buffers.
Send one triple for each buffer, in the order of the bytes:

```
BLOB.RDMA_GET kv:m1:9f2c:layers-0-15 1001 140230000000000 4194304 1002 140230100000000 4194304
```

The total length of the regions must be equal to or larger than the object.
If the reply is `[6291456, <crc>]`, the first 4MB are in the first buffer and the remaining 2MB are at the start of the second buffer.

## Tips

* Send `BLOB.RDMA_HELLO` one time on each connection, and keep the connection open.
  A connection pool with a session on each connection prevents a handshake on each request.
* Register buffers one time and use them again.
  Memory registration is expensive.
* To send many large object commands together, use a [pipeline](pipelining.md).
  The data commands are not permitted in transactions or scripts (see [Limitations](large-object.md#limitations)).
* Keep each object at or below `largeobj.max-object-size`.
  Split larger data into more keys, for example one key for each layer range or each shard.
* Do not use large objects as the only copy of data.
  The module has no persistence and no replication.

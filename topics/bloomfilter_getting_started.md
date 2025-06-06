---
title: "Quick start guide for bloom filters"
description: Understand how to use the bloom filter data type
---

This quick start guide shows you how to:

1. Set up Valkey with the valkey-bloom module (using Docker or manual installation)
2. Create and customize bloom filters
3. Use bloom filters on the valkey-cli
4. Use bloom filters with valkey-py
5. Use bloom filters from the docker image
6. Configure bloom filter default settings

## Setup

To use bloom filters with Valkey, you need to:

1. **Install Valkey**: Follow the [installation guides](installation.md) to install Valkey on your system.

2. **Get the valkey-bloom module**: You have three options:
   - Use the Docker image: [valkey-extensions](https://hub.docker.com/r/valkey/valkey-extensions)
   - Download a pre-built binary from the [releases page](https://github.com/valkey-io/valkey-bloom/releases)
   - Build from source by following the [build instructions](https://github.com/valkey-io/valkey-bloom/blob/unstable/README.md#build-instructions)

## Running a Valkey Server with valkey-bloom

Once valkey-bloom is built, you can run the Valkey server with the module loaded in two different ways, on server start up:
```bash
./valkey-server --loadmodule ./target/release/libvalkey_bloom.so
```
You can also load the valkey bloom module on an already running server by running the following command in [valkey-cli](cli.md):
```bash
127.0.0.1:6379> MODULE LOAD /path/to/libvalkey_bloom.so
```

## Examples of bloom filter commands in Valkey CLI

After starting a [valkey-cli](cli.md) session, you can use the following commands to work with bloom filters:

- [`BF.ADD`](../commands/bf.add.md) - Creates a filter if it doesn't exist and adds an item
- [`BF.INSERT`](../commands/bf.insert.md) - Creates a filter with custom parameters and adds items
- [`BF.RESERVE`](../commands/bf.reserve.md) - Creates an empty filter with custom parameters
- [`BF.MADD`](../commands/bf.madd.md) - Adds multiple items to an existing filter
- [`BF.EXISTS`](../commands/bf.exists.md) - Checks if an item exists in the filter
- [`BF.MEXISTS`](../commands/bf.mexists.md) - Checks if multiple items exist in the filter
- [`BF.INFO`](../commands/bf.info.md) - Gets information about a filter
- [`BF.CARD`](../commands/bf.card.md) - Gets the cardinality (count of items) in a filter

Here's a complete example session showing how to use bloom filters in the Valkey CLI:

```bash
# Create a bloom filter with custom parameters
127.0.0.1:6379> BF.RESERVE mybloom 0.001 10000
OK

# Add items to the filter
127.0.0.1:6379> BF.ADD mybloom item1
(integer) 1

# Add multiple items at once
127.0.0.1:6379> BF.MADD mybloom item2 item3 item4
1) (integer) 1
2) (integer) 1
3) (integer) 1

# Check if items exist
127.0.0.1:6379> BF.EXISTS mybloom item1
(integer) 1
127.0.0.1:6379> BF.EXISTS mybloom nonexistent
(integer) 0

# Check if multiple items are present in the bloomfilter at once
127.0.0.1:6379> BF.MEXISTS mybloom item1 nonexistent item3
1) (integer) 1
2) (integer) 0
3) (integer) 1

# Create a non-scaling bloom filter
127.0.0.1:6379> BF.RESERVE fixed_bloom 0.01 1000 NONSCALING
OK

# Create a bloom filter with a custom expansion rate
127.0.0.1:6379> BF.RESERVE expanding_bloom 0.001 1000 EXPANSION 4
OK

# Get information about a bloom filter
127.0.0.1:6379> BF.INFO mybloom
 1) Capacity
 2) (integer) 10000
 3) Size
 4) (integer) 23912
 5) Number of filters
 6) (integer) 1
 7) Number of items inserted
 8) (integer) 4
 9) Error rate
10) "0.001"
11) Expansion rate
12) (integer) 2
13) Tightening ratio
14) "0.5"
15) Max scaled capacity
16) (integer) 26214300

# Get the cardinality (number of items) in a bloom filter
127.0.0.1:6379> BF.CARD mybloom
(integer) 4
```

## Using bloom filters with Python

You can also interact with bloom filters using the valkey-py client. Here's a simple example:

```python
import valkey

# Connect to Valkey server
client = valkey.Valkey(host='localhost', port=6379)

# Create a bloom filter with specific parameters
client.bf().create("myfilter", 0.01, 1000)

# Add items to the filter
client.bf().add("myfilter", "item1")
client.bf().madd("myfilter", "item2", "item3")

# Check if items exist
exists1 = client.bf().exists("myfilter", "item1")
exists2 = client.bf().exists("myfilter", "nonexistent")

print(f"item1 exists: {exists1 == 1}")  # True
print(f"nonexistent exists: {exists2 == 1}")  # False

# Insert multiple items at once
client.bf().insert("myfilter", ["value1", "value2"])

# Get information about the filter
info = client.bf().info("myfilter")
print(f"Capacity: {info.get('capacity')}")
print(f"Items inserted: {info.get('insertedNum')}")
print(f"Number of filters: {info.get('filterNum')}")
```

## Docker Development

You can easily run Valkey with bloom filter (and other modules) using Docker.

### Pull a docker image that contains the bloom module and other modules

You can easily pull a docker image by navigating to the [valkey-extensions](https://hub.docker.com/r/valkey/valkey-extensions) docker page. Next you can go to tags and choose the image you want and run the command for that image. For example: 

```bash
$ docker pull valkey/valkey:latest
```

This page also has a set of instructions for developing and using the image.

### Starting a basic Valkey instance with modules loaded

```bash
$ docker run --name my-valkey-extensions -d valkey/valkey-extensions
```

### Connecting via valkey-cli

To connect to your Valkey instance using valkey-cli:

```bash
$ docker run -it --network some-network --rm valkey/valkey-extensions valkey-cli -h my-valkey-extensions
```

Make sure your container is on the same network you are trying to connect to it from, this connection can be done by:

```bash
$ docker network connect some-network my-valkey-extensions
```

After connecting you can run commands as you would using the valkey-cli

```bash
my-valkey-extensions:6379> bf.add bloom_name bloom_item
(integer) 1
```


## Configuration for the bloom filter module

As you've seen, you don't need to specify all the attributes of a bloom filter when you create one. The module will use default values for any parameters not explicitly provided. There are five main configuration options that control the default behavior of bloom filters:

1. `bf.bloom-capacity` - Default capacity (100)
2. `bf.bloom-expansion` - Default expansion rate (2)
3. `bf.bloom-fp-rate` - Default false positive rate (0.01)
4. `bf.bloom-tightening-ratio` - Default tightening ratio (0.5)
5. `bf.bloom-use-random-seed` - Boolean flag for using random seeds (true/false)

### When to adjust default configurations

Adjusting the default configurations can be beneficial in several scenarios:

- **Higher capacity (bf.bloom-capacity)**: Increase this value when you expect to store many items in most of your bloom filters. This reduces the need for scaling operations which can improve performance.

- **Lower false positive rate (bf.bloom-fp-rate)**: Decrease this value when accuracy is critical for your application. For example, in fraud detection or security applications where false positives are costly.

- **Higher expansion rate (bf.bloom-expansion)**: Increase this value when you want faster growth of bloom filters that need to scale. This reduces the number of scaling operations but uses more memory quicker.

- **Lower tightening ratio (bf.bloom-tightening-ratio)**: Adjust this when you want to maintain a more consistent false positive rate across multiple scaling operations. (Not advisable to change this default)

- **Random seed (bf.bloom-use-random-seed)**: Set to false only when you need deterministic behavior for testing or reproducibility.

You can modify these default values using the CONFIG SET command:

Example usage of changing all the different properties:
```bash
CONFIG SET bf.bloom-fp-rate 0.001
CONFIG SET bf.bloom-capacity 1000
CONFIG SET bf.bloom-expansion 4
CONFIG SET bf.bloom-tightening-ratio 0.6
CONFIG SET bf.bloom-use-random-seed false
```

## Memory usage limit

The `bf.bloom-memory-usage-limit` configuration (default 128MB) controls the maximum memory that a single bloom filter can use:

Example usage of increasing the limit:
```bash
CONFIG SET bf.bloom-memory-usage-limit 256mb
```

This setting is particularly important for production environments for several reasons:

- **Resource protection**: Prevents a single bloom filter from consuming excessive memory
- **Denial of service prevention**: Protects against attacks that might try to create enormous filters
- **Predictable scaling**: Ensures bloom filters have a known upper bound on resource usage

If your use case requires exceptionally large bloom filters, you can increase this limit. However, be aware that very large bloom filters might impact overall system performance and memory availability for other operations.

When a bloom filter reaches this memory limit, any operation that would cause it to exceed the limit will fail with an error message indicating that the memory limit would be exceeded.
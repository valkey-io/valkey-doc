---
title: "Valkey Search"
description: >
    Introduction to Vector Similarity Search
---

# Valkey-Search

**Valkey-Search** (BSD-3-Clause), provided as a Valkey module, is a high-performance Vector Similarity Search engine
optimized for AI-driven workloads. It delivers single-digit millisecond latency and high QPS, capable of handling billions
of vectors with over 99% recall.

Valkey-Search allows users to create indexes and perform similarity searches, incorporating complex filters.
It supports Approximate Nearest Neighbor (ANN) search with HNSW and exact matching using K-Nearest Neighbors (KNN).
Users can index data using either **[Valkey Hash](hashes.md)** or **[Valkey-JSON](valkey-json.md)** data types.

While Valkey-Search currently focuses on Vector Search, its goal is to extend Valkey into a full-fledged search engine,
supporting full-text search and additional indexing options.

## Use-Cases Where **Valkey-Search** Shines

Valkey-Search's ability to search billions of vectors with millisecond latencies makes it ideal for real-time applications such as:

- Personalized Recommendations – Deliver instant, highly relevant recommendations based on real-time user interactions.
- Fraud Detection & Security – Identify anomalies and suspicious activity with ultra-fast similarity matching.
- Conversational AI & Chatbots – Enhance response accuracy and relevance by leveraging rapid vector-based retrieval.
- Image & Video Search – Enable multimedia search through real-time similarity detection.
- GenAI & Semantic Search – Power advanced AI applications with efficient vector retrieval for natural language understanding.


## Supported Commands

```plaintext
FT.CREATE
FT.DROPINDEX
FT.INFO
FT._LIST
FT.SEARCH
```

For a detailed description of the supported commands, examples and configuration options, see the [Command Reference](../commands/#search).

## Scaling

Valkey-Search supports both **Standalone** and **Cluster** modes. Query processing and ingestion scale linearly with CPU
cores in both modes. For large storage requirements, users can leverage Cluster mode for horizontal scaling of the keyspace.

If replica lag is acceptable, users can achieve horizontal query scaling by directing clients to read from replicas.

## Hybrid Queries

Valkey-Search supports hybrid queries, combining vector similarity search with filtering on indexed fields, such as
**Numeric** and **Tag indexes**.

### Tag index

Tags are text fields that are interpreted as a list of tags delimited by a separator character.
Generally, tags are small sets of values with finite possible values like color, book genre, city name, or author.

- Only indexed fields can be used as a tag filter.
- TAG fields are tokenized by a separator character, which is a comma "," by default but configurable during index creation.
- Only prefix, exact pre filters can be performed on a tag field. Suffix, infix queries are not supported.
- By default, tags are case insensitive. For example, "Blue" and "BLUE" both will be indexed as "blue" and will yield the
    same result in a hybrid query.
- Empty strings are neither indexed or queried.
- During indexing and querying, any trailing whitespace is removed.

#### Syntax

Below are some examples of building filter query on a field named: `color`.

Here `{` and `}` are part of syntax and `|` is used as a OR operator to support multiple tags, general syntax is:

```
@<field_name>:{<tag>}
or
@<field_name>:{<tag1> | <tag2>}
or
@<field_name>:{<tag1> | <tag2> | ...}
```

For example, the following query will return documents with blue OR black OR green color.

```
@color:{blue | black | green}
```

As another example, the following query will return documents containing "hello world" or "hello universe"

```
@color:{hello world | hello universe}
```

### Numeric Index

Numeric indexes allow for filtering queries to only return values that are in between a given start and end value.

- Both inclusive and exclusive queries are supported.
- For open ended queries, `+inf`, `-inf` can be used to express start and end ranges.

As an example, the following query will return books published between 2021 and 2024 (Both inclusive).
The equivalent mathematical expression is `2021 <= year <= 2024`.

```
"@year:[2021 2024]"
```

While The following query will return books published between 2021 (exclusive) and 2024 (inclusive).
The equivalent mathematical expression is `2021 < year <= 2024`:

```
"@year:[(2021 2024]"
```

The following query will return books published before 2024 (inclusive). The equivalent mathematical expression is year `<= 2024`:

```
@year:[(-inf 2024]
```

The following query will return books published after 2015 (exclusive). The equivalent mathematical expression is year `>= 2015`:

```
@year:[2015 +inf]
```

### Query planner

A query that utilizes a filter expression to filter results is called a hybrid query.
Any combination of tag and numeric indexes can form a hybrid query.

- `Pre-filtering`: Pre-filtering relies on secondary indexes (e.g. tag, numeric) to first find the matches to the filter
 expression regardless of vector similarity. Once the filtered results are calculated a brute-force search is
 performed to sort by vector similarity.
- `Inline-filtering`: Inline-filtering performs the vector search algorithm (e.g. HNSW), ignoring found vectors which
 don't match the filter.

`Pre-filtering` is faster when the filtered search space is much smaller than the original search space. When the
filtered search space is large, `inline-filtering` becomes faster. The query planner for Valkey-Search automatically
chooses between the two strategies based on the provided filter.

## Monitoring

To check the server's overall search metrics, you can use the `INFO SEARCH` or `INFO MODULES` commands.

The following metrics are added to the `INFO` command's output:

- `search_used_memory_human`: A human-friendly readable version of the `search_used_memory_bytes` metric
- `search_used_memory_bytes`: The total bytes of memory that all indexes occupy
- `search_number_of_indexes`: Index schema total count
- `search_number_of_attributes`: Total count of attributes for all indexes
- `search_total_indexed_documents`: Total count of all keys for all indexes
- `search_background_indexing_status` (String) The status of the indexing process. `NO_ACTIVITY` indicates idle indexing
- `search_failure_requests_count`: A count of all failed requests, including syntax errors
- `search_successful_requests_count`: A count of all successful requests
- `search_hnsw_create_exceptions_count`: Count of HNSW creation unexpected errors
- `search_hnsw_search_exceptions_count`: Count of HNSW search unexpected errors
- `search_hnsw_remove_exceptions_count`: Count of HNSW removal unexpected errors
- `search_hnsw_add_exceptions_count`: Count of HNSW addition unexpected errors
- `search_hnsw_modify_exceptions_count`: Count of HNSW modification unexpected errors
- `search_modify_subscription_skipped_count`: Count of skipped subscription modifications
- `search_remove_subscription_successful_count`: Count of successful subscription removals
- `search_remove_subscription_skipped_count`: Count of skipped subscription removals
- `search_remove_subscription_failure_count`: Count of failed subscription removals
- `search_add_subscription_successful_count`: Count of successfully added subscriptions
- `search_add_subscription_failure_count`: Count of failures of adding subscriptions
- `search_add_subscription_skipped_count`: Count of skipped subscription adding processes
- `search_modify_subscription_failure_count`: Count of failed subscription modifications
- `search_modify_subscription_successful_count`: Count of successful subscription modifications

## Configuration

### Static configuration

The following list of configurations can be passed to the `loadmodule` command:

1. `--reader-threads`: (Optional) Controls the amount of threads executing queries. (Default: number of physical CPU cores on the host machine)
2. `--writer-threads`: (Optional) Controls the amount of threads processing index mutations. (Default: number of physical CPU cores on the host machine)
3. `--use-coordinator`: (Optional) Cluster mode enabler. Default: `false`.
4. `--hnsw-block-size`:  (Optional) Specifies the allocation block size used by the HNSW graph for storing new vectors. Larger block
   sizes may improve performance by enhancing CPU cache efficiency, but come at the cost of increased memory usage due
   to pre-allocation for potential future growth. (Default: 10K)
5. `--log-level` Controls the log verbosity level. Possible values are: `debug`, `verbose`, `notice` and `warning`. (Default: Valkey's log level)

### Runtime configuration

The following list of configurations can be modified at runtime using the `CONFIG SET` command:

1. `search.hnsw-block-size:`: Specifies the allocation block size used by the HNSW graph for storing new vectors. Larger block
   sizes may improve performance by enhancing CPU cache efficiency, but come at the cost of increased memory usage due
   to pre-allocation for potential future growth. (Default: 10K)



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
Users can index data using either **[Valkey Hash](/topics/hashes)** or **[Valkey-JSON](/topics/valkey-json)** data types.

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

For a detailed description of the supported commands, examples and configuration options, see the [Command Reference](/commands/#search).

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
6. `--query-string-bytes`: (Optional) Controls the maximum length in bytes of the query string for FT.SEARCH commands. (Default: 10240)
7. `--query-string-depth`: (Optional) Controls the maximum depth of query string parsing for FT.SEARCH commands. (Default: 1000)
8. `--query-string-terms-count`: (Optional) Controls the maximum number of terms allowed in a query string. (Default: 16)
9. `--max-indexes`: (Optional) Controls the maximum number of search indexes that can be created. (Default: 10)
10. `--max-prefixes`: (Optional) Controls the maximum number of key prefixes per index during FT.CREATE. (Default: 8)
11. `--max-tag-field-length`: (Optional) Controls the maximum length of tag field identifiers during index creation. (Default: 256)
12. `--max-numeric-field-length`: (Optional) Controls the maximum length of numeric field identifiers during index creation. (Default: 128)
13. `--max-vector-attributes`: (Optional) Controls the maximum number of attributes per index. (Default: 50)
14. `--max-vector-dimensions`: (Optional) Controls the maximum number of dimensions for vector indexes. (Default: 32768)
15. `--max-vector-m`: (Optional) Controls the maximum M parameter for HNSW algorithm. (Default: 2000000)
16. `--max-vector-ef-construction`: (Optional) Controls the maximum EF_CONSTRUCTION parameter for HNSW algorithm. (Default: 4096)
17. `--max-vector-ef-runtime`: (Optional) Controls the maximum EF_RUNTIME parameter for HNSW algorithm. (Default: 4096)
18. `--max-vector-knn`: (Optional) Controls the maximum K value for K-nearest neighbor searches. (Default: 128)
19. `--max-search-result-record-size`: (Optional) Controls the maximum size in bytes for search result records. (Default: 5242880)
20. `--max-search-result-fields-count`: (Optional) Controls the maximum number of fields in search result records. (Default: 500)

### Runtime configuration

The following list of configurations can be modified at runtime using the `CONFIG SET` command:

1. `search.hnsw-block-size:`: Specifies the allocation block size used by the HNSW graph for storing new vectors. Larger block
   sizes may improve performance by enhancing CPU cache efficiency, but come at the cost of increased memory usage due
   to pre-allocation for potential future growth. (Default: 10K)

2. `search.query-string-bytes`: Controls the maximum length in bytes of the query string for FT.SEARCH commands. 

3. `search.query-string-depth`: Controls the maximum depth of query string parsing for FT.SEARCH commands, preventing 
   overly complex nested queries. (Default: 1000, Min: 1, Max: UINT_MAX)

4. `search.query-string-terms-count`: Controls the maximum number of terms (nodes in the predicate tree) allowed in a 
   query string for FT.SEARCH commands. (Default: 16, Min: 1, Max: 32)

5. `search.max-indexes`: Controls the maximum number of search indexes that can be created. 
   (Default: 10, Min: 1, Max: 10)

6. `search.max-prefixes`: Controls the maximum number of key prefixes that can be specified per index during FT.CREATE. 
   (Default: 8, Min: 1, Max: 16)

7. `search.max-tag-field-length`: Controls the maximum length of tag field identifiers during index creation. 
    (Default: 256, Min: 1, Max: 10000)

8. `search.max-numeric-field-length`: Controls the maximum length of numeric field identifiers during index creation. 
    (Default: 128, Min: 1, Max: 256)

9. `search.max-vector-attributes`: Controls the maximum number of attributes that can be defined per index. 
    (Default: 50, Min: 1, Max: 100)

10. `search.max-vector-dimensions`: Controls the maximum number of dimensions allowed for vector indexes. 
    (Default: 32768, Min: 1, Max: 64000)

11. `search.max-vector-m`: Controls the maximum M parameter for HNSW algorithm, which affects the connectivity of the graph. 
    Higher values improve recall but increase memory usage. (Default: 2000000, Min: 1, Max: 2000000)

12. `search.max-vector-ef-construction`: Controls the maximum EF_CONSTRUCTION parameter for HNSW algorithm during index 
    building. Higher values improve index quality but slow down construction. (Default: 4096, Min: 1, Max: 4096)

13. `search.max-vector-ef-runtime`: Controls the maximum EF_RUNTIME parameter for HNSW algorithm during search. Higher 
    values improve recall but slow down search. (Default: 4096, Min: 1, Max: 4096)

14. `search.max-vector-knn`: Controls the maximum K value for K-nearest neighbor searches. 
    (Default: 128, Min: 1, Max: 1000)

15. `search.max-search-result-record-size`: Controls the maximum size in bytes for individual search result records. 
    Records exceeding this limit will be dropped from results. (Default: 5MB, Min: 100, Max: 10MB)

16. `search.max-search-result-fields-count`: Controls the maximum number of fields allowed in individual search result records. 
    Records exceeding this limit will be dropped from results. (Default: 500, Min: 1, Max: 1000)

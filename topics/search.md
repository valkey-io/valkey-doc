# Valkey-Search

**Valkey-Search** (BSD-3-Clause), provided as a Valkey module, is a high-performance Vector Similarity Search engine optimized for AI-driven workloads. It delivers single-digit millisecond latency and high QPS, capable of handling billions of vectors with over 99% recall.

Valkey-Search allows users to create indexes and perform similarity searches, incorporating complex filters. It supports Approximate Nearest Neighbor (ANN) search with HNSW and exact matching using K-Nearest Neighbors (KNN). Users can index data using either **Valkey Hash** or **[Valkey-JSON](https://github.com/valkey-io/valkey-json)** data types.

While Valkey-Search currently focuses on Vector Search, its goal is to extend Valkey into a full-fledged search engine, supporting Full Text Search and additional indexing options.

## Supported Commands

```plaintext
FT.CREATE
FT.DROPINDEX
FT.INFO
FT._LIST
FT.SEARCH
```

For a detailed description of the supported commands and configuration options, see the [Command Reference](https://github.com/valkey-io/valkey-search/blob/main/COMMANDS.md).

For comprehensive examples, refer to the [Quick Start Guide](https://github.com/valkey-io/valkey-search/blob/main/QUICK_START.md).

## Scaling

Valkey-Search supports both **Standalone** and **Cluster** modes. Query processing and ingestion scale linearly with CPU cores in both modes. For large storage requirements, users can leverage Cluster mode for horizontal scaling of the keyspace.

If replica lag is acceptable, users can achieve horizontal query scaling by directing clients to read from replicas.

## Performance

Valkey-Search achieves high performance by storing vectors in-memory and applying optimizations throughout the stack to efficiently utilize the host resources, such as:

- **Parallelism:**  Threading model that enables lock-free execution in the read path.
- **CPU Cache Efficiency:** Designed to promote efficient use of CPU cache.
- **SIMD Optimizations:** Leveraging SIMD (Single Instruction, Multiple Data) for enhanced vector processing.

## Hybrid Queries

Valkey-Search supports hybrid queries, combining Vector Similarity Search with filtering on indexed fields, such as **Numeric** and **Tag indexes**.

There are two primary approaches to hybrid queries:

- **Pre-filtering:** Begin by filtering the dataset and then perform an exact similarity search. This works well when the filtered result set is small but can be costly with larger datasets.
- **Post-filtering:** Perform the similarity search first, then filter the results. This is suitable when the filter-qualified result set is large but may lead to empty or lower than expected amount of results.

Valkey-Search uses a **hybrid approach** with a query planner that selects the most efficient query execution path between:

- **Pre-filtering**
- **Inline-filtering:** Filters results during the similarity search process.

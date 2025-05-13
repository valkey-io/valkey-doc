# Valkey-Search

**Valkey-Search** (BSD-3-Clause), provided as a Valkey module, is a high-performance Vector Similarity Search engine
optimized for AI-driven workloads. It delivers single-digit millisecond latency and high QPS, capable of handling billions
of vectors with over 99% recall.

Valkey-Search allows users to create indexes and perform similarity searches, incorporating complex filters.
It supports Approximate Nearest Neighbor (ANN) search with HNSW and exact matching using K-Nearest Neighbors (KNN).
Users can index data using either **Valkey Hash** or **[Valkey-JSON](https://github.com/valkey-io/valkey-json)** data types.

While Valkey-Search currently focuses on Vector Search, its goal is to extend Valkey into a full-fledged search engine,
supporting Full Text Search and additional indexing options.

## Supported Commands

```plaintext
FT.CREATE
FT.DROPINDEX
FT.INFO
FT._LIST
FT.SEARCH
```

For a detailed description of the supported commands, examples and configuration options, see the [Command Reference](valkey.io/commands/#search).

## Scaling

Valkey-Search supports both **Standalone** and **Cluster** modes. Query processing and ingestion scale linearly with CPU
cores in both modes. For large storage requirements, users can leverage Cluster mode for horizontal scaling of the keyspace.

If replica lag is acceptable, users can achieve horizontal query scaling by directing clients to read from replicas.

## Hybrid Queries

Valkey-Search supports hybrid queries, combining Vector Similarity Search with filtering on indexed fields, such as **Numeric** and **Tag indexes**.

### Tag index

Tags are text fields that are interpreted as a list of tags delimited by a separator character.
Generally, tags are small sets of values with finite possible values like color, book genre, city name, or author.

- Only indexed fields can be used as a tag filter.
- TAG fields are tokenized by a separator character, which is a comma "," by default but configurable during index creation.
- No stemming is performed while indexing a tag field.
- Only prefix, exact pre filters can be performed on a tag field. Suffix, infix queries are not supported.
- By default, tags are case insensitive. For example, "Blue" and "BLUE" both will be indexed as "blue" and will yield the
    same result in a hybrid query.
- Empty strings are neither indexed or queried.
- During indexing and querying, any trailing whitespace is removed.

**Syntax**

Here `{` and `}` are part of syntax and `|` is used as a OR operator to support multiple tags:

```
@:{  |  | ...}
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

There are two primary approaches to hybrid queries:

- **Pre-filtering:** Begin by filtering the dataset and then perform an exact similarity search. This works well when the filtered result set is small but can be costly with larger datasets.
- **Post-filtering:** Perform the similarity search first, then filter the results. This is suitable when the filter-qualified result set is large but may lead to empty or lower than expected amount of results.

Valkey-Search uses a **hybrid approach** with a query planner that selects the most efficient query execution path between:

- **Pre-filtering**
- **Inline-filtering:** Filters results during the similarity search process.

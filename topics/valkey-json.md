---
title: "Valkey-JSON"
description: >
    Introduction to Valkey-JSON
---

Valkey-JSON is a Valkey module written in C++ that provides native JSON (JavaScript Object Notation) support for Valkey. The implementation complies with [RFC7159](https://www.ietf.org/rfc/rfc7159.txt) and [ECMA-404](https://www.ietf.org/rfc/rfc7159.txt) JSON data interchange standards. Users can natively store, query, and modify JSON data structures using the JSONPath query language. The query expressions support advanced capabilities including wildcard selections, filter expressions, array slices, union operations, and recursive searches.

Valkey-JSON leverages RapidJSON, a high-performance JSON parser and generator for C++, chosen for its small footprint and exceptional performance and memory efficiency. As a header-only library with no external dependencies, RapidJSON provides robust Unicode support while maintaining a compact memory profile of just 16 bytes per JSON value on most 32/64-bit machines.

## Example Valkey-JSON Commands

* `JSON.ARRINSERT` inserts one or more values into the array values at path before the index.
* `JSON.MGET` gets serialized JSON objects from multiple document keys at the specified path.
* `JSON.MSET` sets JSON values for multiple keys.
* `JSON.ARRLEN` gets the length of the array at the path.

See the [complete list of Valkey-JSON commands](../commands/#json).

## JSON Properties

* Document Structure - Valkey-JSON supports deeply nested structures including objects and arrays, allowing for complex data representation within a single key. 
 
* Max Depth - The maximum nesting level for JSON objects and arrays. If a JSON object or array contains another object or array, it is considered nested. The maximum allowed nesting depth is 128. Any attempt to exceed this limit will result in an error.

* Path Syntax - Valkey JSON supports two types of path syntaxes:
    * Enhanced syntax 
    * Restricted syntax

* Multi-Key Operations - Some commands like `JSON.MGET` allow operations on multiple JSON keys in a single command, improving performance for batch operations.

* Atomicity - All operations on JSON values are atomic, ensuring data consistency even in multi-threaded environments.

## Performance

* Memory Usage - JSON values are stored in a memory-efficient binary format, optimizing storage while maintaining fast access.

* Indexing - Valkey supports creating indexes on JSON fields, significantly improving query performance on large datasets.

* Partial Updates - JSON commands allow efficient in-place updates to parts of a document without rewriting the entire value.

## Document Size Limit

* JSON documents are stored internally in a format that's optimized for rapid access and modification. This format typically results in consuming somewhat more memory than the equivalent serialized representation of the same document.

* The consumption of memory by a single JSON document is limited to 64 MB, which is the size of the in-memory data structure, not the JSON string. You can check the amount of memory consumed by a JSON document by using the `JSON.DEBUG MEMORY` command.

## JSON ACLs

* Similar to the existing per-datatype categories (@string, @hash, etc.), a new category @json is added to simplify managing access to JSON commands and data. No other existing Valkey or Redis OSS commands are members of the @json category. All JSON commands enforce any keyspace or command restrictions and permissions.

* There are five existing Valkey and Redis OSS ACL categories that are updated to include the new JSON commands: @read, @write, @fast, @slow and @admin. The following table indicates the mapping of JSON commands to the appropriate categories.

## JSON ACL Command Mapping

| JSON Command       | @read | @write | @fast | @slow | @admin |
|--------------------|:-----:|:------:|:-----:|:-----:|:------:|
| JSON.ARRAPPEND     |       |   y    |   y   |       |        |
| JSON.ARRINDEX      |   y   |        |   y   |       |        |
| JSON.ARRINSERT     |       |   y    |   y   |       |        |
| JSON.ARRLEN        |   y   |        |   y   |       |        |
| JSON.ARRPOP        |       |   y    |   y   |       |        |
| JSON.ARRTRIM       |       |   y    |   y   |       |        |
| JSON.CLEAR         |       |   y    |   y   |       |        |
| JSON.DEBUG         |   y   |        |       |   y   |   y    |
| JSON.DEL           |       |   y    |   y   |       |        |
| JSON.FORGET        |       |   y    |   y   |       |        |
| JSON.GET           |   y   |        |   y   |       |        |
| JSON.MGET          |   y   |        |   y   |       |        |
| JSON.MSET          |       |   y    |       |   y   |        |
| JSON.NUMINCRBY     |       |   y    |   y   |       |        |
| JSON.NUMMULTBY     |       |   y    |   y   |       |        |
| JSON.OBJKEYS       |   y   |        |   y   |       |        |
| JSON.OBJLEN        |   y   |        |   y   |       |        |
| JSON.RESP          |   y   |        |   y   |       |        |
| JSON.SET           |       |   y    |       |   y   |        |
| JSON.STRAPPEND     |       |   y    |   y   |       |        |
| JSON.STRLEN        |   y   |        |   y   |       |        |
| JSON.TOGGLE        |       |   y    |   y   |       |        |
| JSON.TYPE          |   y   |        |   y   |       |        |

## Command Syntax

Most commands require a key name as the first argument. Some commands also have a path argument. The path argument defaults to the root if it's optional and not provided.

**Notation**
* Required arguments are enclosed in angle brackets. For example: <key> 
* Optional arguments are enclosed in square brackets. For example: [path]
* Additional optional arguments are indicated by an ellipsis ("…"). For example: [json ...]

## Path Syntax
Redis JSON supports two kinds of path syntaxes:

* **Enhanced syntax** – Follows the JSONPath syntax described by [Goessner](https://goessner.net/articles/JsonPath/), as shown in the following table. We've reordered and modified the descriptions in the table for clarity.
* **Restricted syntax** – Has limited query capabilities.

If a query path starts with `$`, it uses the enhanced syntax. Otherwise, the restricted syntax is used.

**Enhanced Syntax Symbols & Expressions**

| Symbol/Expression     | Description                                                       |
|-----------------------|-------------------------------------------------------------------|
| `$`                   | The root element.                                                 |
| `.` or `[]`           | Child operator.                                                   |
| `..`                  | Recursive descent.                                                |
| `*`                   | Wildcard. All elements in an object or array.                     |
| `[]`                  | Array subscript operator. Index is 0-based.                       |
| `[ , ]`               | Union operator.                                                   |
| `[start:end:step]`    | Array slice operator.                                             |
| `?()`                 | Applies a filter (script) expression to the current array or object. |
| `()`                  | Filter expression.                                                |
| `@`                   | Used in filter expressions that refer to the current node being processed. |
| `==`                  | Equal to, used in filter expressions.                             |
| `!=`                  | Not equal to, used in filter expressions.                         |
| `>`                   | Greater than, used in filter expressions.                         |
| `>=`                  | Greater than or equal to, used in filter expressions.             |
| `<`                   | Less than, used in filter expressions.                            |
| `<=`                  | Less than or equal to, used in filter expressions.                |
| `&&`                  | Logical AND, used to combine multiple filter expressions.         |
| `\|\|`                  | Logical OR, used to combine multiple filter expressions.        |

**Examples** \
The following examples are built on [Goessner's](https://goessner.net/articles/JsonPath/) example XML data, which we have modified by adding additional fields.

```
{ "store": {
    "book": [ 
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95,
        "in-stock": true,
        "sold": true
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99,
        "in-stock": false,
        "sold": true
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99,
        "in-stock": true,
        "sold": false
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99,
        "in-stock": false,
        "sold": false
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95,
      "in-stock": true,
      "sold": false
    }
  }
}
```

| Path                                                              | Description                                                                                   |
|-------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| `'$.store.book[*].author'`                                        | The authors of all books in the store.                                                        |
| `'$..author'`                                                     | All authors.                                                                                  |
| `'$.store.*'`                                                     | All members of the store.                                                                     |
| `'$["store"].*'`                                                  | All members of the store.                                                                     |
| `'$.store..price'`                                                | The price of everything in the store.                                                         |
| `'$..*'`                                                          | All recursive members of the JSON structure.                                                  |
| `'$..book[*]'`                                                    | All books.                                                                                     |
| `'$..book[0]'`                                                    | The first book.                                                                               |
| `'$..book[-1]'`                                                   | The last book.                                                                                |
| `'$..book[0:2]'`                                                  | The first two books.                                                                          |
| `'$..book[0,1]'`                                                  | The first two books.                                                                          |
| `'$..book[0:4]'`                                                  | Books from index 0 to 3 (ending index is not inclusive).                                      |
| `'$..book[0:4:2]'`                                                | Books at index 0 and 2.                                                                       |
| `'$..book[?(@.isbn)]'`                                            | All books with an ISBN number.                                                                |
| `'$..book[?(@.price < 10)]'`                                      | All books cheaper than $10.                                                                   |
| `'$..book[?(@["price"] < 10)]'`                                   | All books cheaper than $10. (alternate syntax)                                                |
| `'$..book[?(@.["price"] < 10)]'`                                  | All books cheaper than $10. (alternate syntax)                                                |
| `'$..book[?(@.price >= 10 && @.price <= 100)]'`                   | All books in the price range of $10 to $100, inclusive.                                       |
| `'$..book[?(@.sold == true || @.in-stock == false)]'`            | All books sold or out of stock.                                                               |
| `'$.store.book[?(@.["category"] == "fiction")]'`                  | All books in the fiction category.                                                            |
| `'$.store.book[?(@.["category"] != "fiction")]'`                  | All books in nonfiction categories.                                                           |

Additional filter expression examples:

```
127.0.0.1:6379> JSON.SET k1 . '{"books": [{"price":5,"sold":true,"in-stock":true,"title":"foo"}, {"price":15,"sold":false,"title":"abc"}]}'
OK
127.0.0.1:6379> JSON.GET k1 $.books[?(@.price>1&&@.price<20&&@.in-stock)]
"[{\"price\":5,\"sold\":true,\"in-stock\":true,\"title\":\"foo\"}]"
127.0.0.1:6379> JSON.GET k1 '$.books[?(@.price>1 && @.price<20 && @.in-stock)]'
"[{\"price\":5,\"sold\":true,\"in-stock\":true,\"title\":\"foo\"}]"
127.0.0.1:6379> JSON.GET k1 '$.books[?((@.price>1 && @.price<20) && (@.sold==false))]'
"[{\"price\":15,\"sold\":false,\"title\":\"abc\"}]"
127.0.0.1:6379> JSON.GET k1 '$.books[?(@.title == "abc")]'
[{"price":15,"sold":false,"title":"abc"}]

127.0.0.1:6379> JSON.SET k2 . '[1,2,3,4,5]'
127.0.0.1:6379> JSON.GET k2 $.*.[?(@>2)]
"[3,4,5]"
127.0.0.1:6379> JSON.GET k2 '$.*.[?(@ > 2)]'
"[3,4,5]"

127.0.0.1:6379> JSON.SET k3 . '[true,false,true,false,null,1,2,3,4]'
OK
127.0.0.1:6379> JSON.GET k3 $.*.[?(@==true)]
"[true,true]"
127.0.0.1:6379> JSON.GET k3 '$.*.[?(@ == true)]'
"[true,true]"
127.0.0.1:6379> JSON.GET k3 $.*.[?(@>1)]
"[2,3,4]"
127.0.0.1:6379> JSON.GET k3 '$.*.[?(@ > 1)]'
"[2,3,4]"
```

**Restricted Syntax Symbols and Expressions**

| Symbol/Expression     | Description                                                       |
|-----------------------|-------------------------------------------------------------------|
| `.` or `[]`           | Child operator.                                                   |
| `[]`                  | Array subscript operator. Index is 0-based.                       |


| Path                                  | Description                        |
|---------------------------------------|------------------------------------|
| `.store.book[0].author`               | The author of the first book.      |
| `.store.book[-1].author`              | The author of the last book.       |
| `.address.city`                       | City name.                         |
| `["store"]["book"][0]["title"]`       | The title of the first book.       |
| `["store"]["book"][-1]["title"]`      | The title of the last book.        |

## Common error prefixes

Each error message has a prefix. The following is a list of common error prefixes.

| Prefix           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `ERR`            | A general error.                                                            |
| `LIMIT`          | An error that occurs when the size limit is exceeded. For example, the document size limit or nesting depth limit was exceeded. |
| `NONEXISTENT`    | A key or path does not exist.                                               |
| `OUTOFBOUNDARIES`| Array index out of bounds.                                                  |
| `SYNTAXERR`      | Syntax error.                                                               |
| `WRONGTYPE`      | Wrong value type.                 

## JSON-related metrics

| Info                     | Description                                                   |
|--------------------------|---------------------------------------------------------------|
| `json_total_memory_bytes`| Total memory allocated to JSON objects.                       |
| `json_num_documents`     | Total number of documents in Valkey or Redis OSS.             |

To query core metrics, run the following command: `info json_core_metrics`
## FT.CREATE

The `FT.CREATE` command creates an empty index and initiates the backfill process. Each index consists of a number of field definitions. Each field definition specifies a field name, a field type and a path within each indexed key to locate a value of the declared type. Some field type definitions have additional sub-type specifiers.

For indexes on HASH keys, the path is the same as the hash member name. The optional `AS` clause can be used to rename the field if desired.
Renaming of fields is especially useful when the member name contains special characters.

For indexes on JSON keys, the path is a JSON path to the data of the declared type. Because the JSON path always contains special characters, the `AS` clause is required.


```bash
FT.CREATE <index-name>
    ON HASH
    [PREFIX <count> <prefix> [<prefix>...]]
    SCHEMA
        (
            <field-identifier> [AS <field-alias>]
                  NUMERIC
                | TAG [SEPARATOR <sep>] [CASESENSITIVE]
                | VECTOR [HNSW | FLAT] <attr_count> [<attribute_name> <attribute_value>]+)
        )+
```


- **\<index-name\>** (required): This is the name you give to your index. If an index with the same name exists already, an error is returned.

- **ON HASH | JSON** (optional): Only keys that match the specified type are included into this index. If omitted, HASH is assumed.

- **PREFIX \<prefix-count\> \<prefix\>** (optional): If this clause is specified, then only keys that begin with the same bytes as one or more of the specified prefixes will be included into this index. If this clause is omitted, all keys of the correct type will be included. A zero-length prefix would also match all keys of the correct type.

### Field types

**TAG**: A tag field is a string that contains one or more tag values.

- **SEPARATOR \<sep\>** (optional): One of these characters `,.<>{}[]"':;!@#$%^&*()-+=~` used to delimit individual tags. If omitted the default value is `,`.
- **CASESENSITIVE** (optional): If present, tag comparisons will be case sensitive. The default is that tag comparisons are NOT case sensitive

**NUMERIC**: A numeric field contains a number.

**VECTOR**: A vector field contains a vector. Two vector indexing algorithms are currently supported: HNSW (Hierarchical Navigable Small World) and FLAT (brute force). Each algorithm has a set of additional attributes, some required and other optional.

- **FLAT:** The Flat algorithm provides exact answers, but has runtime proportional to the number of indexed vectors and thus may not be appropriate for large data sets.
  - **DIM \<number\>** (required): Specifies the number of dimensions in a vector.
  - **TYPE FLOAT32** (required): Data type, currently only FLOAT32 is supported.
  - **DISTANCE\_METRIC \[L2 | IP | COSINE\]** (required): Specifies the distance algorithm
  - **INITIAL\_CAP \<size\>** (optional): Initial index size.
- **HNSW:** The HNSW algorithm provides approximate answers, but operates substantially faster than FLAT.
  - **DIM \<number\>** (required): Specifies the number of dimensions in a vector.
  - **TYPE FLOAT32** (required): Data type, currently only FLOAT32 is supported.
  - **DISTANCE\_METRIC \[L2 | IP | COSINE\]** (required): Specifies the distance algorithm
  - **INITIAL\_CAP \<size\>** (optional): Initial index size.
  - **M \<number\>** (optional): Number of maximum allowed outgoing edges for each node in the graph in each layer. on layer zero the maximal number of outgoing edges will be 2\*M. Default is 16, the maximum is 512\.
  - **EF\_CONSTRUCTION \<number\>** (optional): controls the number of vectors examined during index construction. Higher values for this parameter will improve recall ratio at the expense of longer index creation times. The default value is 200\. Maximum value is 4096\.
  - **EF\_RUNTIME \<number\>** (optional):  controls  the number of vectors to be examined during a query operation. The default is 10, and the max is 4096\. You can set this parameter value for each query you run. Higher values increase query times, but improve query recall.

**RESPONSE** `OK` or error.

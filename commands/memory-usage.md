The `MEMORY USAGE` command reports the number of bytes that a key and its value
require to be stored in RAM.

The reported usage is the total of memory allocations for data and
administrative overheads that a key and its value require.

For aggregate data types (lists, sets, hashes, sorted sets, and streams), the
optional `SAMPLES` option can be provided, where `count` is the number of
sampled elements. The sampled elements are averaged to estimate the total size.
By default, this option is set to `5`. To sample all of the elements, use
`SAMPLES 0`. The `SAMPLES` option has no effect on strings, whose size is
always measured exactly.

## Examples

With Valkey v7.2.4 64-bit and **jemalloc**, the empty string measures as follows:

```
> SET "" ""
OK
> MEMORY USAGE ""
(integer) 56
```

These bytes are pure overhead at the moment as no actual data is stored, and are
used for maintaining the internal data structures of the server (include internal allocator fragmentation). Longer keys and
values show asymptotically linear usage.

```
> SET foo bar
OK
> MEMORY USAGE foo
(integer) 56
> SET foo2 mybar
OK
> MEMORY USAGE foo2
(integer) 64
> SET foo3 0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
OK
> MEMORY USAGE foo3
(integer) 160
```

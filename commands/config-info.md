The `CONFIG INFO` command returns metadata about configuration parameters matching
the given patterns. This is similar to how [`COMMAND INFO`](command-info.md) returns
metadata about commands, but for configuration parameters. It is useful for
discovering valid values programmatically, e.g., when automated tools need to
generate valid config values without having to maintain hardcoded enum options or numeric ranges.

`CONFIG INFO` takes one or more glob-style patterns and returns an array of maps,
one per matching configuration parameter. Each map contains:

* `name`: The canonical name of the configuration parameter.
* `type`: The type of the parameter (e.g., `bool`, `numeric`, `string`, `enum`, `special`).
* `flags`: An array of flags associated with the parameter (e.g., `immutable`, `sensitive`, `protected`, `alias`, `module`, `multi-arg`, `debug`, `deny-loading`).
* `alias`: The alternate name for this config (only present if one exists). Configuration parameters looked up by their alias will include `alias` in the flags array.
* `values`: An array of valid values (only present for `enum` type configs).
* `range`: A two-element array `[min, max]` representing the valid bounds (only present for `numeric` type configs).

## Examples

### Enum config

```
127.0.0.1:6379> CONFIG INFO repl-diskless-load
1) 1) "name"
   2) "repl-diskless-load"
   3) "type"
   4) "enum"
   5) "flags"
   6) 1) "debug"
      2) "deny-loading"
   7) "values"
   8) 1) "disabled"
      2) "on-empty-db"
      3) "swapdb"
      4) "flush-before-load"
```

### Numeric config

```
127.0.0.1:6379> CONFIG INFO timeout
1) 1) "name"
   2) "timeout"
   3) "type"
   4) "numeric"
   5) "flags"
   6) (empty array)
   7) "range"
   8) 1) "0"
      2) "2147483647"
```

### Boolean config

```
127.0.0.1:6379> CONFIG INFO activedefrag
1) 1) "name"
   2) "activedefrag"
   3) "type"
   4) "bool"
   5) "flags"
   6) 1) "debug"
```

### Alias handling

The `alias` field is only present when a config has an alternate name.
Configuration parameters looked up by their alias include `alias` in the flags array:

```
127.0.0.1:6379> CONFIG INFO replicaof
1) 1) "name"
   2) "replicaof"
   3) "type"
   4) "special"
   5) "flags"
   6) 1) "immutable"
      2) "multi-arg"
   7) "alias"
   8) "slaveof"
```

```
127.0.0.1:6379> CONFIG INFO slaveof
1) 1) "name"
   2) "slaveof"
   3) "type"
   4) "special"
   5) "flags"
   6) 1) "immutable"
      2) "multi-arg"
      3) "alias"
   7) "alias"
   8) "replicaof"
```

### Multiple patterns

`CONFIG INFO` supports multiple patterns and glob matching:

```
127.0.0.1:6379> CONFIG INFO active* timeout
1) 1) "name"
   2) "active-defrag-cycle-max"
   3) "type"
   4) "numeric"
   ...
2) 1) "name"
   2) "active-defrag-cycle-min"
   3) "type"
   4) "numeric"
   ...
...
```

Results are sorted alphabetically by config name and deduplicated when multiple
patterns match the same config.

## Special configuration parameters

Configuration parameters with type `special` (such as `save`, `client-output-buffer-limit`) return
only the `name`, `type`, and `flags` fields without additional metadata about their
expected values.

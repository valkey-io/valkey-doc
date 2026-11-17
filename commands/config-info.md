The `CONFIG INFO` command returns metadata about the configuration parameters
that match the given patterns.
It is similar to [`COMMAND INFO`](command-info.md), which returns metadata about
commands.
It is useful for discovering valid values programmatically, for example when
automated tools need to generate valid config values without maintaining
hardcoded enum options or numeric ranges.
To get the current values of configuration parameters, use
[`CONFIG GET`](config-get.md).

`CONFIG INFO` takes one or more glob-style patterns and returns one map for each
matching configuration parameter.
Each map contains:

* `name`: The name of the configuration parameter.
* `type`: The type of the parameter: `bool`, `numeric`, `string`, `enum`, or
  `special`.
* `flags`: An array of the flags set on the parameter.
* `alias`: The other name of the parameter.
  Only present when the parameter has another name.
* `values`: An array of the valid values.
  Only present for `enum` parameters.
* `range`: A two-element array `[min, max]` with the valid bounds.
  Only present for `numeric` parameters.

The `flags` array can contain:

* `immutable`: The parameter can only be set at startup, not with
  [`CONFIG SET`](config-set.md).
* `sensitive`: The value can contain sensitive information, such as a password.
* `debug`: The parameter is useful for debugging.
* `multi-arg`: The parameter takes multiple arguments.
* `hidden`: The parameter is only matched by its exact name, not by glob
  patterns.
* `protected`: The parameter can only be changed when
  `enable-protected-configs` allows it.
* `deny-loading`: The parameter cannot be changed while the server is loading
  data.
* `alias`: This entry is another name for a parameter.
* `module`: The parameter is defined by a module.
* `volatile`: The value refers to data outside the configuration, such as a
  file, so setting the same value again still applies it.

Results are sorted by name.
A parameter that matches more than one pattern is returned once.
If no parameter matches, the reply is an empty array.

### Aliases

A parameter that has another name is returned as two separate entries, one for
each name.
For example, `CONFIG INFO *` returns both `replicaof` and `slaveof`.
The entry for the other name has `name` set to that name, and includes `alias`
in its `flags`.
This applies to exact names and to glob patterns such as `slave*`.
Tools that only need one entry per parameter can skip the entries with the
`alias` flag.

### Numeric ranges

The bounds in `range` are in the parameter's base unit, for example bytes for
memory parameters.
Some parameters give negative values a special meaning.
For example, `maxmemory-clients` stores a percentage as a negative number, and
`commandlog-request-larger-than` uses `-1` to disable a feature.
`CONFIG INFO` does not report this, so check the parameter's description in
`valkey.conf`.
The upper bound of an unsigned parameter can be as large as
`18446744073709551615`.

### Enum values

The `values` array can contain synonyms.
For example, `oom-score-adj` returns `no`, `yes`, `relative`, and `absolute`,
where `yes` and `relative` mean the same thing.
An enum parameter with the `multi-arg` flag, such as `shutdown-on-sigterm`,
accepts several values combined, although not every combination is valid.
For example, `shutdown-on-sigterm` does not accept `save` together with
`nosave`.

### Special parameters

Parameters with type `special`, such as `save` and
`client-output-buffer-limit`, have no `values` or `range` field.
They return `name`, `type`, `flags`, and `alias` if they have another name.

## Reply

Array of maps, one map for each matching configuration parameter.
In RESP2, each map is returned as an array of alternating field names and
values.

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

### String config

```
127.0.0.1:6379> CONFIG INFO dbfilename
1) 1) "name"
   2) "dbfilename"
   3) "type"
   4) "string"
   5) "flags"
   6) 1) "protected"
```

### Config with another name

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

```
127.0.0.1:6379> CONFIG INFO shutdown-on-* maxmemory
1) 1) "name"
   2) "maxmemory"
   3) "type"
   4) "numeric"
   5) "flags"
   6) (empty array)
   7) "range"
   8) 1) "0"
      2) "18446744073709551615"
2) 1) "name"
   2) "shutdown-on-sigint"
   3) "type"
   4) "enum"
   5) "flags"
   6) 1) "multi-arg"
   7) "values"
   8) 1) "default"
      2) "save"
      3) "nosave"
      4) "now"
      5) "force"
      6) "safe"
      7) "failover"
3) 1) "name"
   2) "shutdown-on-sigterm"
   3) "type"
   4) "enum"
   5) "flags"
   6) 1) "multi-arg"
   7) "values"
   8) 1) "default"
      2) "save"
      3) "nosave"
      4) "now"
      5) "force"
      6) "safe"
      7) "failover"
```

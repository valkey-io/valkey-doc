The command returns the stream entries matching a given range of IDs.
The range is specified by a minimum and maximum ID. All the entries having
an ID between the two specified or exactly one of the two IDs specified
(closed interval) are returned.

The `XRANGE` command has a number of applications:

* Returning items in a specific time range. This is possible because
  Stream IDs are [related to time](../topics/streams-intro.md).
* Iterating a stream incrementally, returning just
  a few items at every iteration. However it is semantically much more
  robust than the `SCAN` family of functions.
* Fetching a single entry from a stream, providing the ID of the entry
  to fetch two times: as start and end of the query interval.

The command also has a reciprocal command returning items in the
reverse order, called `XREVRANGE`, which is otherwise identical.

## `-` and `+` special IDs

The `-` and `+` special IDs mean respectively the minimum ID possible
and the maximum ID possible inside a stream, so the following command
will just return every entry in the stream:

```
> XRANGE somestream - +
1) 1) 1526985054069-0
   2) 1) "duration"
      2) "72"
      3) "event-id"
      4) "9"
      5) "user-id"
      6) "839248"
2) 1) 1526985069902-0
   2) 1) "duration"
      2) "415"
      3) "event-id"
      4) "2"
      5) "user-id"
      6) "772213"
... other entries here ...
```

The `-` and `+` special IDs mean, respectively, the minimal and maximal range IDs,
however they are nicer to type.

## Incomplete IDs

Stream IDs are composed of two parts, a Unix millisecond time stamp and a
sequence number for entries inserted in the same millisecond. It is possible
to use `XRANGE` specifying just the first part of the ID, the millisecond time,
like in the following example:

```
> XRANGE somestream 1526985054069 1526985055069
```

In this case, `XRANGE` will auto-complete the start interval with `-0`
and end interval with `-18446744073709551615`, in order to return all the
entries that were generated between a given millisecond and the end of
the other specified millisecond. This also means that repeating the same
millisecond two times, we get all the entries within such millisecond,
because the sequence number range will be from zero to the maximum.

Used in this way `XRANGE` works as a range query command to obtain entries
in a specified time. This is very handy in order to access the history
of past events in a stream.

## Exclusive ranges

The range is close (inclusive) by default, meaning that the reply can include
entries with IDs matching the query's start and end intervals. It is possible
to specify an open interval (exclusive) by prefixing the ID with the
character `(`. This is useful for iterating the stream, as explained below.

## Returning a maximum number of entries

Using the **COUNT** option it is possible to reduce the number of entries
reported. This is a very important feature even if it may look marginal,
because it allows, for instance, to model operations such as *give me
the entry greater or equal to the following*:

```
> XRANGE somestream 1526985054069-0 + COUNT 1
1) 1) 1526985054069-0
   2) 1) "duration"
      2) "72"
      3) "event-id"
      4) "9"
      5) "user-id"
      6) "839248"
```

In the above case the entry `1526985054069-0` exists, otherwise the server
would have sent us the next one. Using `COUNT` is also the base in order to
use `XRANGE` as an iterator.

## Iterating a stream

In order to iterate a stream, we can proceed as follows. Let's assume that
we want two elements per iteration. We start fetching the first two
elements, which is trivial:

```
> XRANGE writers - + COUNT 2
1) 1) 1526985676425-0
   2) 1) "name"
      2) "Virginia"
      3) "surname"
      4) "Woolf"
2) 1) 1526985685298-0
   2) 1) "name"
      2) "Jane"
      3) "surname"
      4) "Austen"
```

Then instead of starting the iteration again from `-`, as the start
of the range we use the entry ID of the *last* entry returned by the
previous `XRANGE` call as an exclusive interval.

The ID of the last entry is `1526985685298-0`, so we just prefix it
with a '(', and continue our iteration:

```
> XRANGE writers (1526985685298-0 + COUNT 2
1) 1) 1526985691746-0
   2) 1) "name"
      2) "Toni"
      3) "surname"
      4) "Morrison"
2) 1) 1526985712947-0
   2) 1) "name"
      2) "Agatha"
      3) "surname"
      4) "Christie"
```

And so forth. Eventually this will allow to visit all the entries in the
stream. Obviously, we can start the iteration from any ID, or even from
a specific time, by providing a given incomplete start ID. Moreover, we
can limit the iteration to a given ID or time, by providing an end
ID or incomplete ID instead of `+`.

The command `XREAD` is also able to iterate the stream.
The command `XREVRANGE` can iterate the stream reverse, from higher IDs
(or times) to lower IDs (or times).

## Fetching single items

If you look for an `XGET` command you'll be disappointed because `XRANGE`
is effectively the way to go in order to fetch a single entry from a
stream. All you have to do is to specify the ID two times in the arguments
of XRANGE:

```
> XRANGE mystream 1526984818136-0 1526984818136-0
1) 1) 1526984818136-0
   2) 1) "duration"
      2) "1532"
      3) "event-id"
      4) "5"
      5) "user-id"
      6) "7782813"
```

## Additional information about streams

For further information about streams please check our
[introduction to Streams document](../topics/streams-intro.md).

## Examples

```
127.0.0.1:6379> XADD writers * name Virginia surname Woolf
"1714701492065-0"
127.0.0.1:6379> XADD writers * name Jane surname Austen
"1714701492075-0"
127.0.0.1:6379> XADD writers * name Toni surname Morrison
"1714701492084-0"
127.0.0.1:6379> XADD writers * name Agatha surname Christie
"1714701492094-0"
127.0.0.1:6379> XADD writers * name Ngozi surname Adichie
"1714701492104-0"
127.0.0.1:6379> XLEN writers
(integer) 5
127.0.0.1:6379> XRANGE writers - + COUNT 2
1) 1) "1714701492065-0"
   2) 1) "name"
      2) "Virginia"
      3) "surname"
      4) "Woolf"
2) 1) "1714701492075-0"
   2) 1) "name"
      2) "Jane"
      3) "surname"
      4) "Austen"
```

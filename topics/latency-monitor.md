---
title: "Latency monitoring"
description: Discovering slow server events in Valkey
---

Valkey is often used for demanding use cases, where it
serves a large number of queries per second per instance, but also has strict latency requirements for the average response
time and the worst-case latency.

While Valkey is an in-memory system, it deals with the operating system in
different ways, for example, in the context of persisting to disk.
Moreover, Valkey implements a rich set of commands. Certain commands
are fast and run in constant or logarithmic time. Other commands have
`O(N)` complexity and can cause latency spikes.

Finally, Valkey is *mostly* single-threaded. This is usually an advantage
from the point of view of the amount of work it can perform per core, and in
the latency figures it is able to provide. However, it poses
a challenge for latency, since the single-thread
must be able to perform certain tasks incrementally, for
example key expiration, in a way that does not impact the other clients
that are served.
Some other operations, such as reading, parsing, polling, and writing to the socket, can be offloaded to a configurable pool of I/O threads, but command execution itself still happens on the main thread.

For all these reasons, there is a feature called
**Latency Monitoring**, that helps the user to check and troubleshoot possible
latency problems. Latency monitoring is composed of the following conceptual
parts:

* Latency hooks that sample different latency-sensitive code paths.
* Time series recording of latency spikes, split by different events.
* Reporting engine to fetch raw data from the time series.
* Analysis engine to provide human-readable reports and hints according to the measurements.

The rest of this document covers the latency monitoring subsystem
details. For more information about the general topic of Valkey
and latency, see [Valkey latency problems troubleshooting](latency.md).

## Events and time series

Different monitored code paths have different names and are called *events*.
For example, `command` is an event that measures latency spikes of possibly slow
command executions, while `fast-command` is the event name for the monitoring
of the O(1) and O(log N) commands. Other events are less generic and monitor
specific operations performed by Valkey. For example, the `fork` event
only monitors the time taken by Valkey to execute the `fork(2)` system call.

A latency spike is an event that takes more time to run than the configured latency
threshold. There is a separate time series associated with every monitored
event. This is how the time series work:

* Every time a latency spike happens, it is logged in the appropriate time series.
* Every time series is composed of 160 elements.
* Each element is a pair made of a Unix timestamp of the time the latency spike was measured and the number of milliseconds the event took to execute.
* Latency spikes for the same event that occur in the same second are merged by taking the maximum latency. Even if continuous latency spikes are measured for a given event, which could happen with a low threshold, at least 160 seconds of history are available.
* Records the all-time maximum latency for every element.

The framework monitors and logs latency spikes in the execution time of these events:

* `command`: regular commands.
* `fast-command`: O(1) and O(log N) commands.
* `fork`: the `fork(2)` system call.
* `rdb-unlink-temp-file`: the `unlink(2)` system call.
* `aof-fsync-always`: the `fsync(2)` system call when invoked by the `appendfsync always` policy.
* `aof-write`: writing to the AOF - a catchall event for `write(2)` system calls.
* `aof-write-pending-fsync`: the `write(2)` system call when there is a pending fsync.
* `aof-write-active-child`: the `write(2)` system call when there are active child processes.
* `aof-write-alone`: the `write(2)` system call when no pending fsync and no active child process.
* `aof-fstat`: the `fstat(2)` system call.
* `aof-rename`: the `rename(2)` system call for renaming the temporary file after completing `BGREWRITEAOF`.
* `aof-rewrite-diff-write`: writing the differences accumulated while performing `BGREWRITEAOF`.
* `active-defrag-cycle`: the active defragmentation cycle.
* `expire-cycle`: the expiration cycle.
* `eviction-cycle`: the eviction cycle.
* `eviction-del`: deletes during the eviction cycle.

## How to enable latency monitoring

The acceptable latency depends on the application.
Some applications require all queries to complete within 1 millisecond. Other applications may tolerate occasional latency of 2 seconds for a small number of clients.

Set a **latency threshold** in milliseconds to enable latency monitoring.
The default threshold is `0`, which disables latency monitoring.

Valkey logs events that exceed the configured threshold as latency spikes.
Set the threshold according to the application's latency requirements.

For example, if the application requires a maximum latency of 100 milliseconds, set the threshold to 100:

```bash
CONFIG SET latency-monitor-threshold 100
```

Latency monitoring is disabled by default.
Latency monitoring requires very little memory. However, enabling it increases the baseline memory usage of a Valkey instance.

## Report information with the LATENCY command

The user interface to the latency monitoring subsystem is the [`LATENCY`](/commands/latency.md) command.
Like many other Valkey commands, `LATENCY` accepts subcommands that modify its behavior.
These subcommands are:

* [`LATENCY LATEST`](/commands/latency-latest.md) - returns the latest latency samples for all events.
* [`LATENCY HELP`](/commands/latency-help.md) - returns helpful text about the different subcommands.
* [`LATENCY HISTORY`](/commands/latency-history.md) - returns timestamp-latency samples for an event.
* [`LATENCY HISTOGRAM`](/commands/latency-histogram.md) - returns the cumulative distribution of latencies of a subset or all commands.
* [`LATENCY RESET`](/commands/latency-reset.md) - resets the latency data for one or more events.
* [`LATENCY GRAPH`](/commands/latency-graph.md) - returns a latency graph for an event.
* [`LATENCY DOCTOR`](/commands/latency-doctor.md) - returns a human-readable latency analysis report.

Refer to each subcommand's documentation page for further information.

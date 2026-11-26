---
title: "Client handling"
description: >
    How the Valkey server manages client connections
---

This document provides information about how Valkey handles clients at the network layer level: connections, timeouts, buffers, and other similar topics are covered here.

## Accepting Client Connections

Valkey accepts clients connections on the configured TCP port and on the Unix socket if enabled. When a new client connection is accepted the following operations are performed:

* The client socket is put in the non-blocking state since Valkey uses multiplexing and non-blocking I/O.
* The `TCP_NODELAY` option is set in order to ensure that there are no delays to the connection.
* A *readable* file event is created so that Valkey is able to collect the client queries as soon as new data is available to read on the socket.

After the client is initialized, Valkey checks if it is already at the limit
configured for the number of simultaneous clients (configured using the `maxclients` configuration directive, see the next section of this document for further information).

When Valkey can't accept a new client connection because the maximum number of clients
has been reached, it tries to send an error to the client in order to
make it aware of this condition, closing the connection immediately.
The error message will reach the client even if the connection is
closed immediately by Valkey because the new socket output buffer is usually
big enough to contain the error, so the kernel will handle transmission
of the error.

## What Order are Client Requests Served In?

The order is determined by a combination of the client socket file descriptor
number and order in which the kernel reports events, so the order should be 
considered as unspecified.

However, Valkey does the following two things when serving clients:

* It only performs a single `read()` system call every time there is something new to read from the client socket. This ensures that if we have multiple clients connected, and a few send queries at a high rate, other clients are not penalized and will not experience latency issues.
* However once new data is read from a client, all the queries contained in the current buffers are processed sequentially. This improves locality and does not need iterating a second time to see if there are clients that need some processing time.

## Maximum Concurrent Connected Clients

The limit for the maximum number of clients that can be handled simultaneously
is configurable using the `maxclients` directive in `valkey.conf`. The default
is 10,000 clients.

However, Valkey checks with the kernel what the maximum number of file
descriptors that we are able to open is (the *soft limit* is checked). If the
limit is less than the maximum number of clients we want to handle, plus
32 (that is the number of file descriptors Valkey reserves for internal uses),
then the maximum number of clients is updated to match the number
of clients it is *really able to handle* under the current operating system
limit.

When `maxclients` is set to a number greater than Valkey can support, a message is logged at startup:

```
$ ./valkey-server --maxclients 100000
41422:M 03 Dec 2025 17:00:00.000 # You requested maxclients of 100000 requiring at least 100032 max file descriptors.
41422:M 03 Dec 2025 17:00:00.000 # Server can't set maximum open files to 100032 because of OS error: Operation not permitted.
41422:M 03 Dec 2025 17:00:00.000 # Current maximum open files is 10000. maxclients has been reduced to 9968 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.
```

When Valkey is configured in order to handle a specific number of clients it
is a good idea to make sure that the operating system limit for the maximum
number of file descriptors per process is also set accordingly.

Under Linux these limits can be set both in the current session and as a
system-wide setting with the following commands:

* `ulimit -Sn 100000 # This will only work if hard limit is big enough.`
* `sysctl -w fs.file-max=100000`

### Reserved Connections for Priority Clients

Starting with Valkey 9.2, you can reserve a part of `maxclients` capacity for critical administrative traffic, such as control plane or monitoring connections, so that operators are not locked out when `maxclients` reaches its limit.

Two configurations control this:

* `priority-subnets` is a comma- or space-separated list of IPv4 or IPv6 addresses or CIDR subnets.
Connections whose source address matches an entry are considered priority clients.
The default is an empty `""` string (disabled).
* `maxclients-reserved` is the number of guaranteed connections, within `maxclients`, for priority clients.
The default is `0` (disabled).

The reservation takes effect only when both configurations are set. Admission then follows these rules:

* The total number of connections never exceeds `maxclients`.
* Connections that are not priority clients are capped at `maxclients` minus `maxclients-reserved`.
Cluster bus connections, and replica connections that don't come from a priority subnet, count toward this cap.
* Priority clients can use any free slot up to `maxclients`.

For example:

```
maxclients 10000
priority-subnets "192.168.1.0/24 10.0.0.0/8"
maxclients-reserved 128
```

In this configuration example, ordinary clients are capped at 9,872 connections (10000 - 128), and clients from `192.168.1.0/24` or `10.0.0.0/8` can always open at least 128 connections, and up to 10,000 if the slots are free.

Both configurations can be changed at runtime using the [`CONFIG SET`](../commands/config-set.md) command, the changes apply to new connections only.
If you set or increase `maxclients-reserved` while ordinary clients already hold the slots being reserved, Valkey doesn't evict them.
Instead, it rejects new incoming normal connections until enough existing ones close.

Priority clients are also served ahead of ordinary clients by the event loop, as described in [Event Loop Prioritization](#event-loop-prioritization).

If you want to monitor priority clients, use the following:

* `connected_priority_clients` in [`INFO clients`](../commands/info.md) reports
  the number of connected priority clients.
* `rejected_priority_connections` in `INFO stats` counts priority connections rejected because `maxclients` was reached.
These are also counted in `rejected_connections`.
* Priority connections show the `H` flag in [`CLIENT LIST`](../commands/client-list.md).

## Event Loop Prioritization

Starting with Valkey 9.2, Valkey processes events from system-critical internal connections ahead of ordinary client traffic. This keeps the cluster bus heartbeats, replication streams, and slot migration links responsive under heavy command workloads, helping to prevent false failovers.

The following connections are high priority:

* Cluster bus links.
* Replication links, on both the primary and the replica side.
* Slot migration links.
* Clients connecting from `priority-subnets` (see [Reserved Connections for Priority Clients](#reserved-connections-for-priority-clients)).

At the start of each event loop cycle, Valkey processes pending high-priority events first.
When a batch of ordinary client events takes several milliseconds, for example with heavy pipelining or multi-key commands, Valkey also interrupts the batch periodically to drain pending high-priority events.

The `priority-preemptive-poll-interval-us` configuration sets the maximum time, in microseconds, between these checks while processing ordinary events with the default being `2000` (2 milliseconds).
Tuning guidelines:

* Smaller values, such as `500` to `1000`, give tighter latency bounds for cluster heartbeats and replication during client traffic bursts.
* Larger values, such as `5000` to `10000`, favor client throughput.
* `0` disables mid-batch preemption.
High-priority events are then processed only at the start of each event loop cycle.

Event loop prioritization requires the epoll (Linux) or kqueue (macOS and BSD) event multiplexer.
On other platforms, Valkey logs a notice at startup and processes all events without prioritization.

The `eventloop_priority_*` fields in [`INFO`](../commands/info.md) report how much time Valkey spends on high-priority events.

## Output Buffer Limits

Valkey needs to handle a variable-length output buffer for every client, since
a command can produce a large amount of data that needs to be transferred to the
client.

However it is possible that a client sends more commands producing more output
to serve at a faster rate than that which Valkey can send the existing output to the
client. This is especially true with Pub/Sub clients in case a client is not
able to process new messages fast enough.

Both conditions will cause the client output buffer to grow and consume
more and more memory. For this reason by default Sets limits to the
output buffer size for different kind of clients. When the limit is reached
the client connection is closed and the event logged in the Valkey log file.

There are two kind of limits Valkey uses:

* The **hard limit** is a fixed limit that when reached will make Valkey close the client connection as soon as possible.
* The **soft limit** instead is a limit that depends on the time, for instance a soft limit of 32 megabytes per 10 seconds means that if the client has an output buffer bigger than 32 megabytes for, continuously, 10 seconds, the connection gets closed.

Different kind of clients have different default limits:

* **Normal clients** have a default limit of 0, that means, no limit at all, because most normal clients use blocking implementations sending a single command and waiting for the reply to be completely read before sending the next command, so it is always not desirable to close the connection in case of a normal client.
* **Pub/Sub clients** have a default hard limit of 32 megabytes and a soft limit of 8 megabytes per 60 seconds.
* **Replicas** have a default hard limit of 256 megabytes and a soft limit of 64 megabyte per 60 seconds.

It is possible to change the limit at runtime using the `CONFIG SET` command or in a permanent way using the Valkey configuration file `valkey.conf`. See the example `valkey.conf` in the Valkey distribution for more information about how to set the limit.

## Query Buffer Hard Limit

Every client is also subject to a query buffer limit. This is a hard limit that will close the connection when the client query buffer (that is the buffer we use to accumulate commands from the client) reaches 1 GB by default, and is actually only an extreme limit to avoid a server crash in case of client or server software bugs.
The limit can be changed with the `client-query-buffer-limit` configuration directive, also at runtime using `CONFIG SET`.
Starting with Valkey 8.0, when authentication is required, a client that has not yet authenticated is limited to 1 MB regardless of this setting.

## Client Eviction

Valkey is built to handle a very large number of client connections.
Client connections tend to consume memory, and when there are many of them, the aggregate memory consumption can be extremely high, leading to data eviction or out-of-memory errors.
These cases can be mitigated to an extent using [output buffer limits](#output-buffer-limits), but Valkey allows us a more robust configuration to limit the aggregate memory used by all clients' connections.


This mechanism is called **client eviction**, and it's essentially a safety mechanism that will disconnect clients once the aggregate memory usage of all clients is above a threshold.
The mechanism first attempts to disconnect clients that use the most memory.
It disconnects the minimal number of clients needed to return below the `maxmemory-clients` threshold.

`maxmemory-clients` defines the maximum aggregate memory usage of all clients connected to Valkey.
The aggregation takes into account all the memory used by the client connections: the [query buffer](#query-buffer-hard-limit), the output buffer, and other intermediate buffers.

Note that replica and primary connections aren't affected by the client eviction mechanism. Therefore, such connections are never evicted.

`maxmemory-clients` can be set permanently in the configuration file (`valkey.conf`) or via the `CONFIG SET` command.
This setting can either be 0 (meaning no limit), a size in bytes (possibly with `mb`/`gb` suffix),
or a percentage of `maxmemory` by using the `%` suffix (e.g. setting it to `10%` would mean 10% of the `maxmemory` configuration).

The default setting is 0, meaning client eviction is turned off by default.
However, for any large production deployment, it is highly recommended to configure some non-zero `maxmemory-clients` value.
A value `5%`, for example, can be a good place to start.

It is possible to flag a specific client connection to be excluded from the client eviction mechanism.
This is useful for control path connections.
If, for example, you have an application that monitors the server via the `INFO` command and alerts you in case of a problem, you might want to make sure this connection isn't evicted.
You can do so using the following command (from the relevant client's connection):

`CLIENT NO-EVICT` `on`

And you can revert that with:

`CLIENT NO-EVICT` `off`

For more information and an example refer to the `maxmemory-clients` section in the default `valkey.conf` file.

Client eviction is available from Redis OSS 7.0.

## Client Timeouts

By default recent versions of Valkey don't close the connection with the client
if the client is idle for many seconds: the connection will remain open forever.

However if you don't like this behavior, you can configure a timeout, so that
if the client is idle for more than the specified number of seconds, the client connection will be closed.

You can configure this limit via `valkey.conf` or simply using `CONFIG SET timeout <value>`.

Note that the timeout only applies to normal clients and it **does not apply to Pub/Sub clients**, since a Pub/Sub connection is a *push style* connection so a client that is idle is the norm.

Even if by default connections are not subject to timeout, there are two conditions when it makes sense to set a timeout:

* Mission critical applications where a bug in the client software may saturate the Valkey server with idle connections, causing service disruption.
* As a debugging mechanism in order to be able to connect with the server if a bug in the client software saturates the server with idle connections, making it impossible to interact with the server.

Timeouts are not to be considered very precise: Valkey avoids setting timer events or running O(N) algorithms in order to check idle clients, so the check is performed incrementally from time to time. This means that it is possible that while the timeout is set to 10 seconds, the client connection will be closed, for instance, after 12 seconds if many clients are connected at the same time.

## The CLIENT Command

The Valkey `CLIENT` command allows you to inspect the state of every connected client, to kill a specific client, and to name connections. It is a very powerful debugging tool if you use Valkey at scale.

`CLIENT LIST` is used in order to obtain a list of connected clients and their state:

```
127.0.0.1:6379> client list
addr=127.0.0.1:52555 fd=5 name= age=855 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=32768 obl=0 oll=0 omem=0 events=r cmd=client
addr=127.0.0.1:52787 fd=6 name= age=6 idle=5 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=ping
```

In the above example two clients are connected to the Valkey server. Let's look at what some of the data returned represents:

* **addr**: The client address, that is, the client IP and the remote port number it used to connect with the Valkey server.
* **fd**: The client socket file descriptor number.
* **name**: The client name as set by `CLIENT SETNAME`.
* **age**: The number of seconds the connection existed for.
* **idle**: The number of seconds the connection is idle.
* **flags**: The kind of client (N means normal client, check the [full list of flags](../commands/client-list.md)).
* **omem**: The amount of memory used by the client for the output buffer.
* **cmd**: The last executed command.

See the [`CLIENT LIST`](../commands/client-list.md) documentation for the full listing of fields and their purpose.

Once you have the list of clients, you can close a client's connection using the `CLIENT KILL` command, specifying the client address as its argument.

The commands `CLIENT SETNAME` and `CLIENT GETNAME` can be used to set and get the connection name. Starting with Redis OSS 4.0, the client name is shown in the
`SLOWLOG` output, to help identify clients that create latency issues.

## TCP keepalive

Valkey has TCP keepalive (`SO_KEEPALIVE` socket option) enabled by default and set to about 300 seconds. This option is useful in order to detect dead peers (clients that cannot be reached even if they look connected). Moreover, if there is network equipment between clients and servers that need to see some traffic in order to take the connection open, the option will prevent unexpected connection closed events.

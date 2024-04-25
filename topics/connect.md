---
title: Connect to Valkey
linkTitle: Connect
description: Learn how to use user interfaces and client libraries
weight: 35
aliases:
  - /docs/ui
---

You can connect to Valkey in the following ways:

* With the `valkey-cli` command line tool
* Via a client library for your programming language

## Valkey command line interface

The [Valkey command line interface](cli.md) (also known as `valkey-cli`) is a terminal program that sends commands to and reads replies from the Valkey server. It has the following two main modes:

1. An interactive Read Eval Print Loop (REPL) mode where the user types commands and receives replies.
2. A command mode where `valkey-cli` is executed with additional arguments, and the reply is printed to the standard output.

## Client libraries

It's easy to connect your application to a Valkey database. Here are some examples for a few languages:

* [C#/.NET](dotnet.md)
* [Go](go.md)
* [Java](java.md)
* [Node.js](nodejs.md)
* [Python](python.md)

You can find a complete list of all client libraries on the [clients page](/resources/clients/).

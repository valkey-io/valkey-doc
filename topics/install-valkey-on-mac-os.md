---
title: "Install Valkey on macOS"
linkTitle: "MacOS"
weight: 1
description: Use Homebrew to install and start Valkey on macOS
aliases:
- /docs/getting-started/installation/install-redis-on-mac-os
---

This guide shows you how to install Valkey on macOS using Homebrew. Homebrew is the easiest way to install Valkey on macOS. If you'd prefer to build Valkey from the source files on macOS, see [Installing Valkey from Source](install-valkey-from-source.md).

## Prerequisites

First, make sure you have Homebrew installed. From the terminal, run:

{{< highlight bash  >}}
brew --version
{{< / highlight >}}

If this command fails, you'll need to [follow the Homebrew installation instructions](https://brew.sh/).

## Installation

From the terminal, run:

{{< highlight bash  >}}
brew install valkey
{{< / highlight >}}

This will install Valkey on your system.

## Starting and stopping Valkey in the foreground

To test your Valkey installation, you can run the `valkey-server` executable from the command line:

{{< highlight bash  >}}
valkey-server
{{< / highlight >}}

If successful, you'll see the startup logs for Valkey, and Valkey will be running in the foreground.

To stop Valkey, enter `Ctrl-C`.

### Starting and stopping Valkey using launchd

As an alternative to running Valkey in the foreground, you can also use `launchd` to start the process in the background:

{{< highlight bash  >}}
brew services start valkey
{{< / highlight >}}

This launches Valkey and restarts it at login. You can check the status of a `launchd` managed Valkey by running the following:

{{< highlight bash  >}}
brew services info valkey
{{< / highlight >}}

If the service is running, you'll see output like the following:

{{< highlight bash  >}}
valkey (homebrew.mxcl.valkey)
Running: ✔
Loaded: ✔
User: miranda
PID: 67975
{{< / highlight >}}

To stop the service, run:

{{< highlight bash  >}}
brew services stop valkey
{{< / highlight >}}

## Connect to Valkey

Once Valkey is running, you can test it by running `valkey-cli`:

{{< highlight bash  >}}
valkey-cli
{{< / highlight >}}

This will open the Valkey REPL. Try running some commands:

{{< highlight bash >}}
127.0.0.1:6379> lpush demos valkey-macOS-demo
OK
127.0.0.1:6379> rpop demos
"valkey-macOS-demo"
{{< / highlight >}}

## Next steps

Once you have a running Valkey instance, you may want to:

* Try the Valkey CLI tutorial
* Connect using one of the Valkey clients

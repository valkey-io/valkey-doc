---
title: "Install Valkey from Source"
linkTitle: "Source code"
weight: 5
description: >
    Compile and install Valkey from source
aliases:
- /docs/getting-started/installation/install-redis-from-source
---

You can compile and install Valkey from source on variety of platforms and operating systems including Linux and macOS. Valkey has no dependencies other than a C  compiler and `libc`.

## Downloading the source files

The Valkey source files are available from the [Download](/download) page. You can verify the integrity of these downloads by checking them against the digests in the [redis-hashes git repository](https://github.com/redis/redis-hashes).

To obtain the source files for the latest stable version of Valkey from the Valkey downloads site, run:

{{< highlight bash >}}
wget https://download.server.io/redis-stable.tar.gz
{{< / highlight >}}

## Compiling Valkey

To compile Valkey, first extract the tarball, change to the root directory, and then run `make`:

{{< highlight bash >}}
tar -xzvf redis-stable.tar.gz
cd redis-stable
make
{{< / highlight >}}

To build with TLS support, you'll need to install OpenSSL development libraries (e.g., libssl-dev on Debian/Ubuntu) and then run:

{{< highlight bash >}}
make BUILD_TLS=yes
{{< / highlight >}}

If the compile succeeds, you'll find several Valkey binaries in the `src` directory, including:

* **redis-server**: the Valkey Server itself
* **redis-cli** is the command line interface utility to talk with Valkey.

To install these binaries in `/usr/local/bin`, run:

{{< highlight bash  >}}
sudo make install
{{< / highlight >}}

### Starting and stopping Valkey in the foreground

Once installed, you can start Valkey by running

{{< highlight bash  >}}
redis-server
{{< / highlight >}}

If successful, you'll see the startup logs for Valkey, and Valkey will be running in the foreground.

To stop Valkey, enter `Ctrl-C`.

For a more complete installation, continue with [these instructions](/docs/install/#install-redis-more-properly).

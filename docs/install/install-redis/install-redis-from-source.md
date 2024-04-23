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

The Valkey source releases are available from the GitHub [Releases](https://github.com/valkey-io/valkey/releases) page.

## Compiling Valkey

To compile Valkey, first extract the tarball, change to the root directory, and then run `make`:

```sh
tar -xzvf valkey-7.2.5.tar.gz
cd valkey-7.2.5
make
```

To build with TLS support, you'll need to install OpenSSL development libraries (e.g., libssl-dev on Debian/Ubuntu) and then run:

```sh
make BUILD_TLS=yes
```

If the compile succeeds, you'll find several Valkey binaries in the `src` directory, including:

* **valkey-server**: the Valkey Server itself
* **valkey-cli** is the command line interface utility to talk with Valkey.

To install these binaries in `/usr/local/bin`, run:

```sh
sudo make install
```

### Starting and stopping Valkey in the foreground

Once installed, you can start Valkey by running

```sh
valkey-server
```

If successful, you'll see the startup logs for Valkey, and Valkey will be running in the foreground.

To stop Valkey, enter `Ctrl-C`.

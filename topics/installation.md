---
title: "Installation"
description: >
  Install Valkey on Linux, macOS, and Windows
---

In this installation guide you will learn how to install, run, and experiment with the Valkey server.

**Note**: For more detailed administrative tips after the installation is complete, see [Valkey Administration](admin.md).

## Prerequisites

Ensure you check the [Valkey Releases page](https://valkey.io/download/releases/) first, which lists the latest release and all prior releases.

**Note:** We recommend you install the latest release.

## Install Valkey

You can install Valkey using multiple methods, choose which one you need from the below options.

### Install Valkey using tarballs

Once you have downloaded the release, unpack the tarball (e.g. `tar -xzvf valkey-8.0.1.tar.gz`) and follow the instructions in the included README.md.

### Install Valkey using Docker

Run in your CLI:

```bash
docker run --name valkey-name -d valkey/valkey
```

You can find more information on images and the configuration options, together with tags, on [Valkey's Docker Hub](https://hub.docker.com/r/valkey/valkey).

### Install Valkey on MacOS

You can install Valkey on MacOS using [Homebrew](https://brew.sh/):

```bash
brew install valkey
# To run Valkey as a service, use
brew services start valkey
# Check that it's running using
brew services info valkey
# and stop it using
brew services stop valkey
```

Or by using [MacPorts](https://www.macports.org/):

```bash
sudo port install valkey
```

### Install Valkey on Linux/BSD package managers

The following package managers are known to be supported, but the list is not exhaustive and is not kept constantly up to date.

You can use the [pkgs.org](https://pkgs.org/download/valkey) website (linux/unix only) or [repology.org](https://repology.org/project/valkey/versions) to check which versions of Valkey are available for your distributions.

**Note:** Please submit a PR to update the below list if you encounter any issues.

#### apt (Debian based)

Valkey is currently available on the following Debian based OS's: Debian/Ubuntu/Mint/Devuan/Raspbian/PureOS.

Install Valkey using the following apt commands:

```bash
sudo apt update
sudo apt install valkey
# For symlinked binaries to redis-cli and other redis-* tools (on Ubuntu)
sudo apt install valkey-redis-compat
```

#### apk (Alpine Linux/Kali Linux/Wolfi)

Install Valkey using the following apk commands:

```bash
sudo apk update
sudo apk add valkey
# Below relevant for Alpine.
# For valkey-cli
sudo apk add valkey-cli
# For symlinked binaries to redis-cli and redis-server
sudo apk add valkey-compat
```

#### yum (CentOS/RHEL/Fedora)

Install Valkey using the following yum commands:

```bash
sudo yum install valkey
# For symlinked binaries to redis-cli and redis-server
sudo yum install valkey-compat-redis
# For valkey-doc (can be used with man, e.g. `man hgetall`, `man valkey.conf`, etc.)
sudo yum install valkey-doc
```

**Note:** Some versions of CentOS and RHEL may not have Valkey in their default repositories.
You can use the [EPEL repository](https://fedoraproject.org/wiki/EPEL) to install Valkey.

#### dnf (Fedora)

Install Valkey using the following dnf commands:

```bash
sudo dnf install valkey
# For symlinked binaries to redis-cli and redis-server
sudo dnf install valkey-compat-redis
# For valkey-doc (can be used with man, e.g. `man hgetall`, `man valkey.conf`, etc.)
sudo dnf install valkey-doc
```

#### Other distributions

Install Valkey using the following commands:

```bash
# ALT Linux
sudo apt-get install valkey
# Arch Linux/Manjaro
sudo pacman -Sy valkey
# FreeBSD
sudo pkg install valkey
# NixOS
nix-env -i valkey
# openSUSE
sudo zypper install valkey
# Solus
sudo eopkg install valkey
# Void Linux
sudo xbps-install -Su valkey
# Exherbo
cave resolve -x dev-db/valkey
```

#### Miscellaneous

Valkey is also available on [SlackBuilds](https://slackbuilds.org/repository/15.0/system/valkey/)
and openpkg on [OpenPKG](https://openpkg.com/).

### Install Valkey on Windows

Valkey is not officially supported on Windows. However, you can install Valkey
on Windows for development using [WSL](https://learn.microsoft.com/windows/wsl/install)
(Windows Subsystem for Linux). Once WSL is set up, follow the Linux instructions
above for your WSL distribution's package manager (e.g. `apt` for the default
Ubuntu distribution).

### Final configurations

The following points apply if you're running Valkey on Linux (including WSL):

* Set the Linux kernel overcommit memory setting to 1. Add `vm.overcommit_memory = 1` to `/etc/sysctl.conf`. Then, reboot or run the command `sysctl vm.overcommit_memory=1` to activate the setting. See [FAQ: Background saving fails with a fork() error on Linux?](faq.md#background-saving-fails-with-a-fork-error-on-linux) for details.

* To ensure the Linux kernel feature Transparent Huge Pages does not impact Valkey memory usage and latency, run the command: `echo never > /sys/kernel/mm/transparent_hugepage/enabled` to disable it. See [Latency Diagnosis - Latency induced by transparent huge pages](latency.md#latency-induced-by-transparent-huge-pages) for additional context.

## Test if you can connect to Valkey by using the CLI

External programs talk to Valkey using a TCP socket and a Valkey specific protocol. This protocol is implemented in the Valkey client libraries for the different programming languages. However, Valkey provides a command line utility that you can use to send commands to Valkey called [valkey-cli](https://valkey.io/topics/cli/).

**Note:** If you're not yet running Valkey as a system service, you can run Valkey in the foreground using `valkey-server` and stop it by pressing `Ctrl-C`.

To check if Valkey is working properly using the command-line interface, run:

```bash
$ valkey-cli ping
PONG
```

The command is sent to the Valkey instance running on localhost port 6379. For more information on valkey-cli arguments, see the documentation [here](https://valkey.io/topics/cli/).

You can run `valkey-cli` without arguments which prompts the program to enter interactive mode. For example:

```bash
$ valkey-cli
127.0.0.1:6379> ping
PONG
```

## Securing Valkey

By default Valkey binds to **all the interfaces** and has no authentication at all. We do not recommend exposing Valkey to the internet without a proper security posture in place, check the following steps in order to make Valkey more secure:

1. Make sure the port Valkey uses to listen for connections (by default 6379 and additionally 16379 if you run Valkey in cluster mode, plus 26379 for Sentinel) is firewalled, so that it is not possible to contact Valkey from the outside world.
2. Use a configuration file where the `bind` directive is set in order to guarantee that Valkey listens on only the network interfaces you are using. For example, only the loopback interface (127.0.0.1) if you are accessing Valkey locally from the same computer.
3. Set up authentication using [Access Control List (ACL)](acl.md) or use the `requirepass` option to add an additional layer of security so that clients will be required to authenticate using the `AUTH` command.
4. Use [TLS](tls.md) to encrypt traffic between Valkey servers and Valkey clients if your environment requires encryption.

Make sure you understand the above and apply **at least** a firewall layer. After the firewall is in place, try to connect with `valkey-cli` from an external host to confirm that the instance is not reachable.

For more information, please check our [security page](security.md) and the [quick start](quickstart.md) for details on how to secure Valkey.

## Use Valkey from your application

Using Valkey just from the command line interface is good but it might not be enough. To access Valkey from your application you need to download and install a Valkey client library for your programming language.

You'll find a [full list of clients for different languages on this page](../clients/).

## Valkey persistence

If you start Valkey with the default configuration, Valkey spontaneously saves the dataset only intermittently. For example, after at least five minutes if you have at least 100 changes in your data.

If you want your database to persist and be reloaded after a restart, make sure to call the [SAVE](../commands/save.md) command manually every time you want to force a data set snapshot. 

Alternatively, you can save the data on disk before quitting by using the [SHUTDOWN](../commands/shutdown.md) command:

```bash
$ valkey-cli shutdown
```

This way, Valkey saves the data on disk before quitting.

For more information on how persistence works, see [Persistence](persistence.md).

## Install Valkey as a system service

Running Valkey from the command line is fine for development. However, for an actual application to run on a real server, it's highly recommended to install Valkey as a system service so that everything starts properly after a system restart.
The available packages for supported Linux distributions already include the capability of starting the Valkey server as a service.

Valkey supports systemd, but this document was written for init scripts, before systemd was widely adapted.
There are many guides online for how to set up a systemd service.

The remainder of this section explains how to set up Valkey using an init script, for distros like Alpine Linux that don't use systemd.

If you have not yet run `make install` after building the Valkey source, you need to do so before continuing. By default, `make install` copies the `valkey-server` and `valkey-cli` binaries to `/usr/local/bin`.

1. Create a directory in which to store your Valkey config files and data:

  ```bash
  sudo mkdir /etc/valkey
  sudo mkdir /var/valkey
  ```

2. Copy the init script that you'll find in the Valkey distribution under the **utils** directory into `/etc/init.d`. We suggest calling it with the name of the port where you are running this instance of Valkey. Make sure the resulting file has `0755` permissions:

```bash
sudo cp utils/valkey_init_script /etc/init.d/valkey_6379
```

3. Edit the init script:

```bash
sudo vi /etc/init.d/valkey_6379
```

Make sure to set the `VALKEYPORT` variable to the port you are using.
Both the pid file path and the configuration file name depend on the port number.

4. Copy the template configuration file you'll find in the root directory of the Valkey distribution into `/etc/valkey/` using the port number as the name, for instance:

```bash
sudo cp valkey.conf /etc/valkey/6379.conf
```

5. Create a directory inside `/var/valkey` that will work as both data and working directory for this Valkey instance:

```bash
sudo mkdir /var/valkey/6379
```

6. Edit the configuration file, making sure to perform the following changes:

  * Set **daemonize** to yes (by default it is set to no).
  * Set the **pidfile** to `/var/run/valkey_6379.pid`, modifying the port as necessary.
  * Change the **port** accordingly. In our example it is not needed as the default port is already `6379`.
  * Set your preferred **loglevel**.
  * Set the **logfile** to `/var/log/valkey_6379.log`.
  * Set the **dir** to `/var/valkey/6379` (very important step!).

7. Finally, add the new Valkey init script to all the default runlevels using the following command:

```bash
sudo update-rc.d valkey_6379 defaults
```

You are done! Now you can try running your instance with:

```bash
sudo /etc/init.d/valkey_6379 start
```

Make sure that everything is working as expected:

1. Try pinging your instance within a `valkey-cli` session using the `PING` command.
2. Do a test save with `valkey-cli save` and check that a dump file is correctly saved to `/var/valkey/6379/dump.rdb`.
3. Check that your Valkey instance is logging to the `/var/log/valkey_6379.log` file.
4. If it's a new machine where you can try it without problems, make sure that after a reboot everything is still working.

## Further configuring Valkey

You can read the example [valkey.conf](https://github.com/valkey-io/valkey/blob/unstable/valkey.conf) file, which is heavily annotated to help guide you on making changes. Further details can also be found in the [configuration article on this site](valkey.conf.md) and advice for configuring and managing Valkey in production can be found in the [Administration](admin.md) topic.

The above instructions don't include all of the Valkey configuration parameters. We encourage you to explore the documentation, and feel free to leave us feedback.

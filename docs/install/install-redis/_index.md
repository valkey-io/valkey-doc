---
title: "Install Valkey"
linkTitle: "Install Valkey"
weight: 1
description: >
    Install Valkey on Linux, macOS, and Windows
aliases:
- /docs/getting-started/installation
- /docs/getting-started/tutorial
---

This is a an installation guide. You'll learn how to install, run, and experiment with the Valkey server process.

While you can install Valkey on any of the platforms listed below, you might also consider using Valkey Cloud by creating a [free account](https://redis.com/try-free?utm_source=redisio&utm_medium=referral&utm_campaign=2023-09-try_free&utm_content=cu-redis_cloud_users).

## Install Valkey

See the guide below that best fits your needs:

* [Install Valkey from Source](/docs/install/install-redis/install-redis-from-source)
* [Install Valkey on Linux](/docs/install/install-redis/install-redis-on-linux)
* [Install Valkey on macOS](/docs/install/install-redis/install-redis-on-mac-os)
* [Install Valkey on Windows](/docs/install/install-redis/install-redis-on-windows)

Refer to [Valkey Administration](/docs/management/admin/) for detailed setup tips.

## Test if you can connect using the CLI

After you have Valkey up and running, you can connect using `redis-cli`.

External programs talk to Valkey using a TCP socket and a Valkey specific protocol. This protocol is implemented in the Valkey client libraries for the different programming languages. However, to make hacking with Valkey simpler, Valkey provides a command line utility that can be used to send commands to Valkey. This program is called **redis-cli**.

The first thing to do to check if Valkey is working properly is sending a **PING** command using redis-cli:

```
$ redis-cli ping
PONG
```

Running **redis-cli** followed by a command name and its arguments will send this command to the Valkey instance running on localhost at port 6379. You can change the host and port used by `redis-cli` - just try the `--help` option to check the usage information.

Another interesting way to run `redis-cli` is without arguments: the program will start in interactive mode. You can type different commands and see their replies.

```
$ redis-cli
127.0.0.1:6379> ping
PONG
```

## Securing Valkey

By default Valkey binds to **all the interfaces** and has no authentication at all. If you use Valkey in a very controlled environment, separated from the external internet and in general from attackers, that's fine. However, if an unhardened Valkey is exposed to the internet, it is a big security concern. If you are not 100% sure your environment is secured properly, please check the following steps in order to make Valkey more secure:

1. Make sure the port Valkey uses to listen for connections (by default 6379 and additionally 16379 if you run Valkey in cluster mode, plus 26379 for Sentinel) is firewalled, so that it is not possible to contact Valkey from the outside world.
2. Use a configuration file where the `bind` directive is set in order to guarantee that Valkey listens on only the network interfaces you are using. For example, only the loopback interface (127.0.0.1) if you are accessing Valkey locally from the same computer.
3. Use the `requirepass` option to add an additional layer of security so that clients will be required to authenticate using the `AUTH` command.
4. Use [spiped](http://www.tarsnap.com/spiped.html) or another SSL tunneling software to encrypt traffic between Valkey servers and Valkey clients if your environment requires encryption.

Note that a Valkey instance exposed to the internet without any security [is very simple to exploit](http://antirez.com/news/96), so make sure you understand the above and apply **at least** a firewall layer. After the firewall is in place, try to connect with `redis-cli` from an external host to confirm that the instance is not reachable.

## Use Valkey from your application

Of course using Valkey just from the command line interface is not enough as the goal is to use it from your application. To do so, you need to download and install a Valkey client library for your programming language.

You'll find a [full list of clients for different languages in this page](/clients).


## Valkey persistence

You can learn [how Valkey persistence works on this page](/docs/management/persistence/). It is important to understand that, if you start Valkey with the default configuration, Valkey will spontaneously save the dataset only from time to time. For example, after at least five minutes if you have at least 100 changes in your data. If you want your database to persist and be reloaded after a restart make sure to call the **SAVE** command manually every time you want to force a data set snapshot. Alternatively, you can save the data on disk before quitting by using the **SHUTDOWN** command:

```
$ redis-cli shutdown
```

This way, Valkey will save the data on disk before quitting. Reading the [persistence page](/docs/management/persistence/) is strongly suggested to better understand how Valkey persistence works.

## Install Valkey properly

Running Valkey from the command line is fine just to hack a bit or for development. However, at some point you'll have some actual application to run on a real server. For this kind of usage you have two different choices:

* Run Valkey using screen.
* Install Valkey in your Linux box in a proper way using an init script, so that after a restart everything will start again properly.

A proper install using an init script is strongly recommended. 

{{% alert title="Note" color="warning" %}}
The available packages for supported Linux distributions already include the capability of starting the Valkey server from `/etc/init`.
{{% /alert  %}}

If you have not yet run `make install` after building the Valkey source, you will need to do so before continuing. By default, `make install` will copy the `redis-server` and `redis-cli` binaries to `/usr/local/bin`.

* Create a directory in which to store your Valkey config files and your data:

    ```
    sudo mkdir /etc/redis
    sudo mkdir /var/redis
    ```

* Copy the init script that you'll find in the Valkey distribution under the **utils** directory into `/etc/init.d`. We suggest calling it with the name of the port where you are running this instance of Valkey. Make sure the resulting file has `0755` permissions.
    
    ```
    sudo cp utils/redis_init_script /etc/init.d/redis_6379
    ```

* Edit the init script.

    ```
    sudo vi /etc/init.d/redis_6379
    ```

Make sure to set the **REDISPORT** variable to the port you are using.
Both the pid file path and the configuration file name depend on the port number.

* Copy the template configuration file you'll find in the root directory of the Valkey distribution into `/etc/redis/` using the port number as the name, for instance:

    ```
    sudo cp redis.conf /etc/redis/6379.conf
    ```

* Create a directory inside `/var/redis` that will work as both data and working directory for this Valkey instance:

    ```
    sudo mkdir /var/redis/6379
    ```

* Edit the configuration file, making sure to perform the following changes:
    * Set **daemonize** to yes (by default it is set to no).
    * Set the **pidfile** to `/var/run/redis_6379.pid`, modifying the port as necessary.
    * Change the **port** accordingly. In our example it is not needed as the default port is already `6379`.
    * Set your preferred **loglevel**.
    * Set the **logfile** to `/var/log/redis_6379.log`.
    * Set the **dir** to `/var/redis/6379` (very important step!).
* Finally, add the new Valkey init script to all the default runlevels using the following command:

    ```
    sudo update-rc.d redis_6379 defaults
    ```

You are done! Now you can try running your instance with:

```
sudo /etc/init.d/redis_6379 start
```

Make sure that everything is working as expected:

1. Try pinging your instance within a `redis-cli` session using the `PING` command.
2. Do a test save with `redis-cli save` and check that a dump file is correctly saved to `/var/redis/6379/dump.rdb`.
3. Check that your Valkey instance is logging to the `/var/log/redis_6379.log` file.
4. If it's a new machine where you can try it without problems, make sure that after a reboot everything is still working.

{{% alert title="Note" color="warning" %}}
The above instructions don't include all of the Valkey configuration parameters that you could change. For example, to use AOF persistence instead of RDB persistence, or to set up replication, and so forth.
{{% /alert  %}}

You should also read the example [redis.conf](/docs/management/config-file/) file, which is heavily annotated to help guide you on making changes. Further details can also be found in the [configuration article on this site](/docs/management/config/).

<hr>

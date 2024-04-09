---
title: "Valkey security"
linkTitle: "Security"
weight: 1
description: Security model and features in Valkey
aliases: [
    /topics/security,
    /docs/manual/security,
    /docs/manual/security.md
]
---

This document provides an introduction to the topic of security from the point of
view of Valkey. It covers the access control provided by Valkey, code security concerns,
attacks that can be triggered from the outside by selecting malicious inputs, and
other similar topics. 
You can learn more about access control, data protection and encryption, secure Valkey architectures, and secure deployment techniques by taking the PLEASE-REVIEW{[Redis University security course](https://university.redis.com/courses/ru330/)}.

For security-related contacts, open an issue on GitHub, or when you feel it
is really important to preserve the security of the communication, use the
GPG key at the end of this document.

## Security model

Valkey is designed to be accessed by trusted clients inside trusted environments.
This means that usually it is not a good idea to expose the Valkey instance
directly to the internet or, in general, to an environment where untrusted
clients can directly access the Valkey TCP port or UNIX socket.

For instance, in the common context of a web application implemented using Valkey
as a database, cache, or messaging system, the clients inside the front-end
(web side) of the application will query Valkey to generate pages or
to perform operations requested or triggered by the web application user.

In this case, the web application mediates access between Valkey and
untrusted clients (the user browsers accessing the web application).

In general, untrusted access to Valkey should
always be mediated by a layer implementing ACLs, validating user input,
and deciding what operations to perform against the Valkey instance.

## Network security

Access to the Valkey port should be denied to everybody but trusted clients
in the network, so the servers running Valkey should be directly accessible
only by the computers implementing the application using Valkey.

In the common case of a single computer directly exposed to the internet, such
as a virtualized Linux instance (Linode, EC2, ...), the Valkey port should be
firewalled to prevent access from the outside. Clients will still be able to
access Valkey using the loopback interface.

Note that it is possible to bind Valkey to a single interface by adding a line
like the following to the **valkey.conf** file:

    bind 127.0.0.1

Failing to protect the Valkey port from the outside can have a big security
impact because of the nature of Valkey. For instance, a single `FLUSHALL` command can be used by an external attacker to delete the whole data set.

## Protected mode

Unfortunately, many users fail to protect Valkey instances from being accessed
from external networks. Many instances are simply left exposed on the
internet with public IPs. PLEASE-REVIEW{Since version 3.2.0,} Valkey enters a special mode called **protected mode** when it is
executed with the default configuration (binding all the interfaces) and
without any password in order to access it. In this mode, Valkey only replies to queries from the
loopback interfaces, and replies to clients connecting from other
addresses with an error that explains the problem and how to configure
Valkey properly.

We expect protected mode to seriously decrease the security issues caused
by unprotected Valkey instances executed without proper administration. However,
the system administrator can still ignore the error given by Valkey and
disable protected mode or manually bind all the interfaces.

## Authentication

Valkey provides two ways to authenticate clients.
The recommended authentication method PLEASE-REVIEW{, introduced in Valkey 6,} is via Access Control Lists, allowing named users to be created and assigned fine-grained permissions.
Read more about Access Control Lists [here](/docs/management/security/acl/).

The legacy authentication method is enabled by editing the **valkey.conf** file, and providing a database password using the `requirepass` setting.
This password is then used by all clients.

When the `requirepass` setting is enabled, Valkey will refuse any query by
unauthenticated clients. A client can authenticate itself by sending the
**AUTH** command followed by the password.

The password is set by the system administrator in clear text inside the
valkey.conf file. It should be long enough to prevent brute force attacks
for two reasons:

* Valkey is very fast at serving queries. Many passwords per second can be tested by an external client.
* The Valkey password is stored in the **valkey.conf** file and inside the client configuration. Since the system administrator does not need to remember it, the password can be very long.

The goal of the authentication layer is to optionally provide a layer of
redundancy. If firewalling or any other system implemented to protect Valkey
from external attackers fail, an external client will still not be able to
access the Valkey instance without knowledge of the authentication password.

Since the `AUTH` command, like every other Valkey command, is sent unencrypted, it
does not protect against an attacker that has enough access to the network to
perform eavesdropping.

## TLS support

Valkey has optional support for TLS on all communication channels, including
client connections, replication links, and the Valkey Cluster bus protocol.

## Disallowing specific commands

It is possible to disallow commands in Valkey or to rename them as an unguessable
name, so that normal clients are limited to a specified set of commands.

For instance, a virtualized server provider may offer a managed Valkey instance
service. In this context, normal users should probably not be able to
call the Valkey **CONFIG** command to alter the configuration of the instance,
but the systems that provide and remove instances should be able to do so.

In this case, it is possible to either rename or completely shadow commands from
the command table. This feature is available as a statement that can be used
inside the valkey.conf configuration file. For example:

    rename-command CONFIG b840fc02d524045429941cc15f59e41cb7be6c52

In the above example, the **CONFIG** command was renamed into an unguessable name.  It is also possible to completely disallow it (or any other command) by renaming it to the empty string, like in the following example:

    rename-command CONFIG ""

## Attacks triggered by malicious inputs from external clients

There is a class of attacks that an attacker can trigger from the outside even
without external access to the instance. For example, an attacker might insert data into Valkey that triggers pathological (worst case)
algorithm complexity on data structures implemented inside Valkey internals.

An attacker could supply, via a web form, a set of strings that
are known to hash to the same bucket in a hash table in order to turn the
O(1) expected time (the average time) to the O(N) worst case. This can consume more
CPU than expected and ultimately cause a Denial of Service.

To prevent this specific attack, Valkey uses a per-execution, pseudo-random
seed to the hash function.

Valkey implements the SORT command using the qsort algorithm. Currently,
the algorithm is not randomized, so it is possible to trigger a quadratic
worst-case behavior by carefully selecting the right set of inputs.

## String escaping and NoSQL injection

The Valkey protocol has no concept of string escaping, so injection
is impossible under normal circumstances using a normal client library.
The protocol uses prefixed-length strings and is completely binary safe.

Since Lua scripts executed by the `EVAL` and `EVALSHA` commands follow the
same rules, those commands are also safe.

While it would be a strange use case, the application should avoid composing the body of the Lua script from strings obtained from untrusted sources.

## Code security

In a classical Valkey setup, clients are allowed full access to the command set,
but accessing the instance should never result in the ability to control the
system where Valkey is running.

Internally, Valkey uses all the well-known practices for writing secure code to
prevent buffer overflows, format bugs, and other memory corruption issues.
However, the ability to control the server configuration using the **CONFIG**
command allows the client to change the working directory of the program and
the name of the dump file. This allows clients to write RDB Valkey files
to random paths. This is [a security issue](http://antirez.com/news/96) that may lead to the ability to compromise the system and/or run untrusted code as the same user as Valkey is running.

Valkey does not require root privileges to run. It is recommended to
run it as an unprivileged *valkey* user that is only used for this purpose.

## GPG key

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
=J9BD
-----END PGP PUBLIC KEY BLOCK-----
```

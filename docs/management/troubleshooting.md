---
title: "Troubleshooting Valkey"
linkTitle: "Troubleshooting"
weight: 9
description: Problems with Valkey? Start here.
aliases: [
    /topics/problems,
    /docs/manual/troubleshooting,
    /docs/manual/troubleshooting.md
]
---

This page tries to help you with what to do if you have issues with Valkey. Part of the Valkey project is helping people that are experiencing problems because we don't like to leave people alone with their issues.

* If you have **latency problems** with Valkey, that in some way appears to be idle for some time, read our [Valkey latency troubleshooting guide](/topics/latency).
* Valkey stable releases are usually very reliable, however in the rare event you are **experiencing crashes** the developers can help a lot more if you provide debugging information. Please read our [Debugging Valkey guide](/topics/debugging).
* We have a long history of users experiencing crashes with Valkey that actually turned out to be servers with **broken RAM**. Please test your RAM using **valkey-server --test-memory** in case Valkey is not stable in your system. Valkey built-in memory test is fast and reasonably reliable, but if you can you should reboot your server and use [memtest86](http://memtest86.com).

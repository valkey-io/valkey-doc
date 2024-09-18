---
title: "Valkey release notes"
linkTitle: "Release notes"
description: Release notes for Valkey
---

## Upgrade urgency levels

* **LOW:**      No need to upgrade unless there are new features you want to use.
* **MODERATE:** Program an upgrade of the server, but it's not urgent.
* **HIGH:**     There is a critical bug that may affect a subset of users. Upgrade!
* **CRITICAL:** There is a critical bug affecting MOST USERS. Upgrade ASAP.
* **SECURITY:** There are security fixes in the release.

## Release notes index

* [Valkey 8.0 release notes](#80-valkey-release-notes)
  * [Valkey 8.0.0 GA - Released Sun 15 Sep 2024](#800-ga-valkey-800-ga-released-sun-15-sep-2024)
    * [Logging and Tooling Improvements](#800-ga-logging-and-tooling-improvements)
    * [Bug fixes](#800-ga-bug-fixes)
    * [Performance](#800-ga-performance)
    * [Behavior Changes](#800-ga-behavior-changes)
  * [Valkey 8.0.0 RC2 - Released Tue 2 Sep 2024](#800-rc2-valkey-released-tue-2-sep-2024)
    * [New Features](#800-rc2-new-features)
    * [Logging and Tooling Improvements](#800-rc2-logging-and-tooling-improvements)
    * [Bug fixes](#800-rc2-bug-fixes)
    * [Performance](#800-rc2-performance)
    * [Compatibility Improvements](#800-rc2-compatibility-improvements)
    * [Behavior Changes](#800-rc2-behavior-changes)
    * [Configuration Changes](#800-rc2-configuration-changes)
  * [Valkey 8.0.0 RC1 - Released Thu 1 Aug 2024](#800-rc1-valkey-released-thu-1-aug-2024)
    * [Un-deprecated Commands - Cluster](#800-rc1-un-deprecated-commands-cluster)
    * [New/Modified Commands - Core](#800-rc1-newmodified-commands-core)
    * [New/Modified Commands - Cluster](#800-rc1-newmodified-commands-cluster)
    * [New/Modified Metrics - Core](#800-rc1-newmodified-metrics-core)
    * [New Features - Core](#800-rc1-new-features-core)
    * [New Features - Cluster](#800-rc1-new-features-cluster)
    * [Compatibility Improvements - Core](#800-rc1-compatibility-improvements-core)
    * [Compatibility Improvements - Sentinel](#800-rc1-compatibility-improvements-sentinel)
    * [Performance/Efficiency Improvements - Core](#800-rc1-performanceefficiency-improvements-core)
    * [Performance/Efficiency Improvements - Cluster](#800-rc1-performanceefficiency-improvements-cluster)
    * [Reliability Improvements - Core](#800-rc1-reliability-improvements-core)
    * [Reliability Improvements - Cluster](#800-rc1-reliability-improvements-cluster)
    * [Usability Improvements - Core](#800-rc1-usability-improvements-core)
    * [Usability Improvements - Cluster](#800-rc1-usability-improvements-cluster)
    * [Usability Improvements - CLI](#800-rc1-usability-improvements-cli)
    * [Module Improvements - Core](#800-rc1-module-improvements-core)
    * [Module Improvements - Cluster](#800-rc1-module-improvements-cluster)
    * [Behavior Changes - Core](#800-rc1-behavior-changes-core)
    * [Behavior Changes - Cluster](#800-rc1-behavior-changes-cluster)
    * [Behavior Changes - Sentinel](#800-rc1-behavior-changes-sentinel)
    * [Bug Fixes - Core](#800-rc1-bug-fixes-core)
    * [Bug Fixes - Cluster](#800-rc1-bug-fixes-cluster)
    * [Bug Fixes - Tooling](#800-rc1-bug-fixes-tooling)
    * [Internal Codebase Improvements](#800-rc1-internal-codebase-improvements)
    * [Experimental](#800-rc1-experimental)
  * [Valkey 8.0 Acknowledgments](#80-valkey-acknowledgments)
* [Valkey 7.2 release notes](#72-valkey-release-notes)
  * [Valkey 7.2.6 GA - Released Tue 30 July 2024](#726-ga-valkey-released-tue-30-july-2024)
    * [Bug fixes - Core](#726-ga-bug-fixes-core)
    * [Bug fixes - Cluster](#726-ga-bug-fixes-cluster)
    * [Bug fixes - Sentinel](#726-ga-bug-fixes-sentinel)
    * [Bug fixes - CLI](#726-ga-bug-fixes-cli)
  * [Valkey 7.2.5 GA - Released Tue 16 Apr 2024](#725-ga-valkey-released-tue-16-apr-2024)
    * [Changes to support Valkey branding](#725-ga-changes-to-support-valkey-branding)
  * [Valkey 7.2.5 RC1 - Released Fri 12 Apr 2024](#725-rc1-valkey-released-fri-12-apr-2024)
    * [Changes to support Valkey branding](#725-rc1-changes-to-support-valkey-branding)
    * [Bug fixes](#725-rc1-bug-fixes)
  * [Valkey 7.2.4 RC1 - Released Tue 09 Apr 2024](#724-rc1-valkey-released-tue-09-apr-2024)
    * [Changes to support Valkey branding](#724-rc1-changes-to-support-valkey-branding)
    * [Bug fixes](#724-rc1-bug-fixes)
  * [Valkey 7.2 Acknowledgments](#72-valkey-acknowledgments)

## <a id="80-valkey-release-notes"></a>Valkey 8.0 release notes

### <a id="800-ga-valkey-800-ga-released-sun-15-sep-2024"></a>Valkey 8.0.0 GA - Released Sun 15 Sep 2024

Upgrade urgency **LOW**.

This is the first release of Valkey 8.0, which
includes stability and performance improvements over the second release
candidate. This release is fully compatible with Redis OSS 7.2.4.

#### <a id="800-ga-logging-and-tooling-improvements"></a>Logging and Tooling Improvements

* Added full client info to SHUTDOWN and CLUSTER FAILOVER logs for better traceability
  of requests. ([#875])

#### <a id="800-ga-bug-fixes"></a>Bug fixes

* Resolved issues in replicationSetPrimary where the primary node's IP/port updates were
  not correctly handled in the cluster gossip section. ([#965])
* Fixed AOF base suffix during rewrites when modifying the aof-use-rdb-preamble setting,
  ensuring correct suffix caching to prevent inconsistencies. ([#886])
* Addressed rare crashes in async IO threads with TLS by preventing concurrent read and
  write job overlap. ([#1011])
* Prevented AOF from being incorrectly disabled after loading RDB data, ensuring proper
  re-enabling of AOF. ([#1001])
* Triggered a save of the cluster configuration file before shutdown to prevent
  inconsistencies caused by unsaved node configuration changes. ([#822])
* Fixed timing issue in CLUSTER SETSLOT to ensure replicas handle migration correctly
  when receiving the command before the gossip update. ([#981])

#### <a id="800-ga-performance"></a>Performance

* Optimized the handling of temporary set objects in SUNION and SDIFF commands, resulting
  in a 41% performance improvement for SUNION and 27% for SDIFF. ([#996])

#### <a id="800-ga-behavior-changes"></a>Behavior Changes

* Replicas now flush old data after checking RDB file is valid during disk-based replication,
  preventing partial data loss and ensuring a clean data load. ([#926])

### <a id="800-rc2-valkey-released-tue-2-sep-2024"></a>Valkey 8.0.0 RC2 - Released Tue 2 Sep 2024

Upgrade urgency **LOW**.

This is the second release candidate of Valkey 8.0, which
generally includes stability and performance improvements over the first release
candidate. This release is fully compatible with Redis OSS 7.2.4.

#### <a id="800-rc2-new-features"></a>New Features

* Add support for setting the group on a unix domain socket. ([#901])
* Experimental - RDMA: Support user keepalive command. ([#916])

#### <a id="800-rc2-logging-and-tooling-improvements"></a>Logging and Tooling Improvements

* Improve logging when a cluster is unable to failover. ([#780])
* Add epoch information to failover auth denied logs. ([#816])
* Improve messaging when valkey-cli cluster --fix meet check failed. ([#867])
* Log unexpected $ENDOFF responses in dual channel replication. ([#839])
* Skip IPv6 tests when it is unsupported on TCLSH. ([#910])
* Add a light weight version of DEBUG OBJECT. ([#881])
* Add lfu support for DEBUG OBJECT command, added lfu_freq and
  lfu_access_time_minutes fields. ([#479])

#### <a name="800-rc2-bug-fixes"></a>Bug fixes

* Correctly expose client infomation in the slowlog when running commands in scripts. ([#805])
* Fix a bug where lastbgsave_status was unecessarily being updated when dual
  channel replication failed. ([#811])
* Fix a bug which caused dual channel replication to get stuck because of a TLS
  issue. ([#837])
* Fix a bug which caused bouncing `-REDIRECT` messages during a FAILOVER ([#871])
* Avoid re-establishing replication to a node that is already the primary in `CLUSTER REPLICATE`. ([#884])
* Fix `CLUSTER SETSLOT` with `BLOCK` to only wait for replicas that are online. ([#879])
* Fix `valkey-cli` to make source node ignore NOREPLICAS when doing the last CLUSTER SETSLOT ([#928])
* Exclude '.' and ':' from `isValidAuxChar`'s banned charset to better support
  IPV6 addresses. ([#963])
* Better handle `-REDIRECT` messages in the MULTI context. ([#895])

#### <a id="800-rc2-performance"></a>Performance

* Improve multithreaded performance with memory prefetching. ([#861])
* Optimize ZUNION[STORE] command by removing unnecessary accumulator dict. ([#829])
* Optimize linear search of WAIT and WAITAOF when unblocking the client. ([#787])
* Move prepareClientToWrite out of loop for lrange command to remove redundant calls. ([#860])
* Optimize various commands by using sdsAllocSize instead of sdsZmallocSize. ([#923])
* Using intrinsics to optimize counting HyperLogLog trailing bits. ([#846])
* Free client's MULTI state when it becomes dirty to reduce memory usage. ([#961])
* Optimize the fast path of SET if the expiration time has already expired. ([#865])

#### <a id="800-rc2-compatibility-improvements"></a>Compatibility Improvements

* Add 4 Sentinel command `GET-PRIMARY-ADDR-BY-NAME`, `PRIMARY`, `PRIMARIES`, and
  `IS-PRIMARY-DOWN-BY-ADDR` to allow clients to use inclusive language. ([#789])

#### <a id="800-rc2-behavior-changes"></a>Behavior Changes

* Block unsubscribe related commands for clients that are not in subscribed mode. ([#759])

#### <a id="800-rc2-configuration-changes"></a>Configuration Changes

* Change repl-backlog-size from 1MB to 10MB by default. ([#911])
* Remove the protected flag from `dual-channel-replication`. ([#908])

### <a id="800-rc1-valkey-released-thu-1-aug-2024"></a>Valkey 8.0.0 RC1 - Released Thu 1 Aug 2024

Upgrade urgency **LOW**.

This is the first release candidate of Valkey 8.0, with
performance, reliability, and observability improvements. It includes asynchronous
I/O threading, better cluster scaling reliability, dual primary-replica channel
for faster full synchronization, per-slot metrics for resource management, and
experimental RDMA support for increased throughput and reduced latency. This
release is fully compatible with Redis OSS 7.2.4.

#### <a id="800-rc1-un-deprecated-commands-cluster"></a>Un-deprecated Commands - Cluster

* Un-deprecate the `CLUSTER SLOTS` command. ([#536])

#### <a id="800-rc1-newmodified-commands-core"></a>New/Modified Commands - Core

* Add `SCRIPT SHOW` sub-command to dump scripts via SHA1. ([#617])
* Add `NOSCORES` option to `ZSCAN` command. ([#324])
* Add `NOVALUES` option to `HSCAN` command. (Redis#12765)
* Expose Lua `os.clock()` API to allow scripts to determine how long the
  script has been executing. (Redis#12971)
* Implement `CLIENT KILL MAXAGE <MAXAGE>`. (Redis#12299)
* Allow running `WAITAOF` in scripts, remove `NOSCRIPT` flag. (Redis#12977)
* Support `XREAD[GROUP]` with `BLOCK` option in scripts. (Redis#12596)
* Introduce `+` as a special ID for the last item in stream on `XREAD`
  Command. (Redis#7388, Redis#13117)

#### <a id="800-rc1-newmodified-commands-cluster"></a>New/Modified Commands - Cluster

* Introduce `CLUSTER SLOT-STATS` command which allows tracking of per slot
  metrics for key count, CPU utilization, network bytes in, and network
  bytes out. ([#20], [#351])
* Add `TIMEOUT` option to `CLUSTER SETSLOT` command. ([#556], [#445])

#### <a id="800-rc1-newmodified-metrics-core"></a>New/Modified Metrics - Core

* Introduce per-client metrics for network traffic and command execution
  in `CLIENT LIST` and `CLIENT INFO`. ([#327])
* Add metrics for DB memory overhead and rehashing status to `INFO MEMORY`
  and `MEMORY STATS`. (Redis#12913)
* Add `pubsub_clients` metric to `INFO CLIENTS`. (Redis#12849)
* Add metrics for client buffer limit disconnections to `INFO`. (Redis#12476)
* Add metrics for monitoring clients using `WATCH` command and watched keys.
  (Redis#12966)
* Added allocator muzzy memory metrics to `INFO MEMORY` and `MEMORY STATS`.
  (Redis#12996)

#### <a id="800-rc1-new-features-core"></a>New Features - Core

* Support replica redirect for read/write operations to primary in standalone
  mode. ([#325])
* Add server config for cluster blacklist TTL. ([#738])
* Add availability zone server config. ([#700])

#### <a id="800-rc1-new-features-cluster"></a>New Features - Cluster

* Support IPv4 and IPv6 dual stack and client-specific IPs in clusters. ([#736])
* Support `BY/GET` options for `SORT/SORT_RO` in cluster mode when pattern
  implies a single slot. (Redis#12728)

#### <a id="800-rc1-compatibility-improvements-core"></a>Compatibility Improvements - Core

* Derive RDB and module child process names based on server start name for
  compatibility. ([#454])
* Update server identity in `serverPanic` output based on `extended-redis-compatibility`
  config. ([#415])

#### <a id="800-rc1-compatibility-improvements-sentinel"></a>Compatibility Improvements - Sentinel

* Accept `redis-sentinel` to start Valkey in Sentinel mode. ([#731])

#### <a id="800-rc1-performanceefficiency-improvements-core"></a>Performance/Efficiency Improvements - Core

* Introduce dual channel for more efficient full sync replication. ([#60])
* Introduce async IO threading for improved multi-threaded performance.
  ([#763], [#758])
* Embed key directly in main dictionary entry for improved memory efficiency.
  ([#541])
* Use thread-local storage to reduce atomic contention in updating memory
  metrics. ([#674])
* Reduce redundant calls to `prepareClientToWrite` for continuous `addReply*`.
  ([#670])
* Optimize the logic for checking conversion to skip list during `ZADD` operations.
  ([#806])
* Optimize `sdsfree` with `zfree_with_size` to avoid redundant size calculation.
  ([#453])
* Combine events to eliminate redundant `kevent(2)` calls. ([#638])
* Introduce shared query buffer for client reads to reduce memory usage. ([#258])
* Optimize CRC64 performance for large batches by processing bytes in parallel.
  ([#350])
* Use `SOCK_NONBLOCK` to reduce system calls for outgoing connections. ([#293])
* Enable `accept4()` detection on specific versions of various platforms. ([#294])
* Convert CRC16 slot table to fixed-size array for improved memory efficiency.
  (Redis#13112)
* Run `SCRIPT FLUSH` truly asynchronously and close Lua interpreter in a
  background thread. (Redis#13087)
* Optimize `DEL` command to avoid redundant deletions for expired keys. (Redis#13080)
* Improve defragmentation for large bins to enhance memory efficiency. (Redis#12996)
* Optimize hash table resizing to include empty dictionaries. (Redis#12819)
* Reduce performance impact of dictionary rehashing by optimizing bucket processing.
  (Redis#12899)
* Optimize performance for simultaneous client `[P|S]UNSUBSCRIBE`. (Redis#12838)
* Optimize CPU cache efficiency during dictionary rehashing. (Redis#5692)
* Optimize `ZRANGE` offset location from linear search to skip list jump. (Redis#12450)
* Fix `aeSetDontWait` timing to avoid unnecessary waits in `aeProcessEvent`. (Redis#12068)

#### <a id="800-rc1-performanceefficiency-improvements-cluster"></a>Performance/Efficiency Improvements - Cluster

* Add lightweight cluster message header for Pub/Sub messages. ([#654])
* Minor performance improvement in Valkey cluster by avoid initializing key
  buffer in `getKeysResult`. ([#631])
* Cache `CLUSTER SLOTS` response to improve throughput and reduce latency. ([#53])
* Replace slots_to_channels radix tree with slot-specific dictionaries for
  shard channels. (Redis#12804)
* Optimize `KEYS` command when pattern includes hashtag and implies a single
  slot. (Redis#12754)
* Optimize `SCAN` command with `MATCH` when pattern implies a single slot.
  (Redis#12536)
* Replace cluster metadata with slot specific dictionaries to reduce memory
  usage when using Valkey cluster. (Redis#11695, Redis#12704)

#### <a id="800-rc1-reliability-improvements-core"></a>Reliability Improvements - Core

* Limit tracking custom errors (e.g. from Lua) while allowing normal errors
  to be tracked ([#500], Redis#13141)
* Manage maximum number of new connections per cycle to prevent connection
  storms. (Redis#12178)

#### <a id="800-rc1-reliability-improvements-cluster"></a>Reliability Improvements - Cluster

* Reduce failover time in Valkey cluster when multiple sequential failovers
  occurred by resetting `failover_auth_time` when the new primary node goes
  down. ([#782])
* Restrict node failure marking to primaries with assigned slots. ([#634])
* Enhance cluster meet reliability under link failures. ([#461])
* Improve reliability of slot migration in Valkey clusters. ([#445])

#### <a id="800-rc1-usability-improvements-core"></a>Usability Improvements - Core

* Re-brand and refine latency report messages. ([#644])
* Optimize `ACL LOAD` to avoid disconnecting clients whose users are unchanged.
  (Redis#12171)

#### <a id="800-rc1-usability-improvements-cluster"></a>Usability Improvements - Cluster

* Adjust log levels for various cluster-related logs to improve clarity. ([#633])
* Maintain deterministic ordering of replica(s) in `CLUSTER SLOTS` response. ([#265])

#### <a id="800-rc1-usability-improvements-cli"></a>Usability Improvements - CLI

* Add prompt message when Ctrl-C is pressed in `valkey-cli`. ([#702])
* Keep an in-memory history of all commands in `valkey-cli` so that sensitive
  commands can be shown within the same session. (Redis#12862)

#### <a id="800-rc1-module-improvements-core"></a>Module Improvements - Core

* Add `ValkeyModule_TryCalloc()` and `ValkeyModule_TryRealloc()` to handle
  allocation failures gracefully. (Redis#12985)
* Make `ValkeyModule_Yield` thread-safe by handling events in the main thread.
  (Redis#12905)
* Allow modules to declare new ACL categories. (Redis#12486)

#### <a id="800-rc1-module-improvements-cluster"></a>Module Improvements - Cluster

* Add API `ValkeyModule_ClusterKeySlot` and `ValkeyModule_ClusterCanonicalKeyNameInSlot`.
  (Redis#13069)

#### <a id="800-rc1-behavior-changes-core"></a>Behavior Changes - Core

* Re-brand the Lua debugger. ([#603])
* Change default pidfile from `redis.pid` to `valkey.pid`. ([#378])
* Abort transactions on nested `MULTI` or `WATCH` commands. ([#723])
* Ensure keys that match the `SCAN` filter are not lazily expired and return
  an error for invalid types. ([#501])
* Rename `redis` in AOF logs and proc title to `valkey-aof-rewrite`. ([#393])
* Change default syslog-ident from `redis` to `valkey`. ([#390])
* Update `Redis` to `Valkey` in `serverLog` messages in server.c file. ([#231])
* Remove `Redis` from various error reply messages. See GitHub PR for more
  details. ([#206])
* Reject empty strings for configs `dir`, `dbfilename`, and `cluster-config-file`.
  ([#636])
* Change key-spec flag from `RW` to `OW` for `SINTERSTORE` command. (Redis#12917)
* Return more precise error messages for some cases verifying keys during script
  execution. (Redis#12707)
* Return errors for `BITCOUNT` and `BITPOS` with non-existing keys or invalid
  arguments instead of zero. (Redis#11734)
* Validate `BITCOUNT` arguments before key existence check. (Redis#12394)
* Redact ACL username information and mark `*-key-file-pass` configs as
  sensitive. (Redis#12860)
* Allow `MULTI/EXEC` to use a small amount of additional memory beyond the
  used-memory limit. (Redis#12961)

#### <a id="800-rc1-behavior-changes-cluster"></a>Behavior Changes - Cluster

* Allow `CLUSTER NODES/INFO/MYID/MYSHARDID` during loading state. ([#596])
* Make cluster replicas return `ASK` and `TRYAGAIN` during slot migration. ([#495])

#### <a id="800-rc1-behavior-changes-sentinel"></a>Behavior Changes - Sentinel

* Replace `master-reboot-down-after-period` with `primary-reboot-down-after-period`
  in `sentinel.conf`. ([#647])

#### <a id="800-rc1-bug-fixes-core"></a>Bug Fixes - Core

* Fix a bug that caused LRU/LFU inconsistencies for some integer objects. ([#250])
* Fix a bug where Valkey may use a sub-optimal encoding for some data types.
  (Redis#13148)
* Fix propagation of `entries_read` by calling `streamPropagateGroupID`
  unconditionally. (Redis#12898)
* Fix race condition issues between the main thread and module threads.
  (Redis#12817)
* Wake blocked clients ASAP in next `beforeSleep` for `WAITAOF`. (Redis#12627)
* Fix crash in crash-report and improve thread management with RW locks.
  (Redis#12623)

#### <a id="800-rc1-bug-fixes-cluster"></a>Bug Fixes - Cluster

* Fix a bug where a shard returns the incorrect slot slot information in
  `CLUSTER SHARDS` command on primary failure. ([#790])
* Allow module authentication to succeed when the cluster is down. ([#693])
* Fix `PONG` message processing for primary-ship tracking during fail-overs.
  (Redis#13055)
* Prevent double freeing of cluster link with `DEBUG CLUSTERLINK KILL`.
  (Redis#12930)
* Unsubscribe all clients from replica for shard channel if the primary
  ownership changes. (Redis#12577)

#### <a id="800-rc1-bug-fixes-tooling"></a>Bug Fixes - Tooling

* Fix `valkey-check-aof` misidentifying data in manifest format as MP-AOF.
  (Redis#12958)
* Fix `valkey-cli` to respect the `--count` option without requiring
  `--pattern`. (Redis#13092)
* Fix `valkey-benchmark` to distribute operations across all slots owned by
  a node in cluster mode. (Redis#12986)

#### <a id="800-rc1-internal-codebase-improvements"></a>Internal Codebase Improvements

* Enable debug asserts for cluster and Sentinel tests. ([#588])
* Introduce a minimal debugger for Tcl integration test suite. ([#683])
* Set up clang-format GitHub action for automated code formatting checks. ([#538])
* Replace custom atomic logic with C11 _Atomics. ([#490])
* Add fast fail option for Tcl test cases. ([#482])
* Introduce a simple unit test framework. ([#460])
* An initial simple unit test framework. ([#344])
* Introduce Codecov for automated code coverage tracking. ([#316])
* Remove deprecated `redis-trib` CLI program. ([#281])
* Add `-fno-omit-frame-pointer` to default compilation flags to improve
  debuggability. (Redis#12973)
* Refactor the per-slot dict-array db.c into a new kvstore data structure.
  (Redis#12822)
* Unified database rehash method for both standalone and cluster modes.
  (Redis#12848)
* Clarify and decouple the sampling logic in eviction to improve readability.
  (Redis#12781)
* Rewrite large printf calls to smaller ones for readability. (Redis#12257)

#### <a id="800-rc1-experimental"></a>Experimental

* Introduce Valkey Over RDMA transport (experimental). ([#477])

### <a id="80-valkey-acknowledgments"></a>Valkey 8.0 Acknowledgments

We appreciate the efforts of all who contributed code to this release!

lan Slang, Binbin, Brennan, Chen Tianjie, Cui Fliter, Daniel House, Darren Jiang,
David Carlier, Debing Sun, Dingrui, Dmitry Polyakovsky, Eran Liberty, Gabi Ganam,
George Guimares, Guillaume Koenig, Guybe, Harkrishn Patro, Hassaan Khan, Hwang Si Yeon,
ICHINOSE Shogo, icy17, Ikko Eltociear Ashimine, iKun, Itamar Haber, Jachin, Jacob Murphy,
Jason Elbaum, Jeff Liu, John Sully, John Vandenberg, Jonathan Wright, Jonghoonpark, Joe Hu,
Josiah Carlson, Juho Kim, judeng, Jun Luo, K.G. Wang, Karthik Subbarao, Karthick Ariyaratnam,
kell0gg, Kyle Kim, Leibale Eidelman, LiiNen, Lipeng Zhu, Lior Kogan, Lior Lahav, Madelyn Olson,
Makdon, Maria Markova, Mason Hall, Matthew Douglass, meiravgri, michalbiesek, Mike Dolan,
Mikel Olasagasti Uranga, Moshe Kaplan, mwish, naglera, NAM UK KIM, Neal Gompa, nitaicaro,
Nir Rattner, Oran Agra, Ouri Half, Ozan Tezcan, Parth, PatrickJS, Pengfei Han, Pierre, Ping Xie,
poiuj, pshankinclarke, ranshid, Ronen Kalish, Roshan Khatri, Samuel Adetunji, Sankar, secwall,
Sergey Fedorov, Sher_Sun, Shivshankar, skyfirelee, Slava Koyfman, Subhi Al Hasan, sundb,
Ted Lyngmo, Thomas Fline, tison, Tom Morris, Tyler Bream, uriyage, Viktor Söderqvist, Vitaly,
Vitah Lin, VoletiRam, w. ian douglas, WangYu, Wen Hui, Wenwen Chen, Yaacov Hazan, Yanqi Lv,
Yehoshua Hershberg, Yves LeBras, zalj, Zhao Zhao, zhenwei pi, zisong.cw

## <a id="72-valkey-release-notes"></a>Valkey 7.2 release notes

### <a id="726-ga-valkey-released-tue-30-july-2024"></a>Valkey 7.2.6 GA - Released Tue 30 July 2024

Upgrade urgency **MODERATE**.

This release fixes an incompatibility issue with modules
compiled for Redis. For other users, it primarily fixes uncommon bugs.

#### <a id="726-ga-bug-fixes-core"></a>Bug fixes - Core

* Fix typo in REGISTER_API macro to prevent segfaults when loading Redis
  modules ([#608])
* Fix the command duration reset issue when clients are blocked and commands
  are reprocessed ([#526])
* Fix the data type conversion error in zrangeResultBeginStore (Redis#13148)
* Fix a crash caused by quicklist node merges (Redis#13040)
* Fix crashes in module blocking client timeout cases (Redis#13011)
* Fix conversion of numbers in Lua args to Redis args
  (Redis#13115, Fixes Redis#13113)
* Fix crash in LSET command when replacing small list items with larger ones,
  creating listpacks larger than 4GB (Redis#12955, Fixes Redis#12864)
* Fix blocking command timeout reset issue during reprocessing (Redis#13004)

#### <a id="726-ga-bug-fixes-cluster"></a>Bug fixes - Cluster

* Fix the CLUSTER SHARDS command to display accurate slot information even
  if a primary node fails ([#790], Fixes [Issue #784])
* Fix an issue where module authentication failed when the cluster was down
  ([#693], Fixes [Issue #619])
* Ensure only primary nodes with slots can mark another node as failed ([#634])
* Improve MEET command reliability under link failures to maintain cluster
  membership symmetry ([#461])
* Allow single primary node to mark potentially failed replica as FAIL in
  single-shard cluster (Redis#12824)

#### <a id="726-ga-bug-fixes-sentinel"></a>Bug fixes - Sentinel

* Accept redis-sentinel to start Valkey in Sentinel mode ([#731], Fixes [Issue #719])

#### <a id="726-ga-bug-fixes-cli"></a>Bug fixes - CLI

* Ensure the `--count` option in redis-cli works correctly even without
  `--pattern` (Redis#13092)
* Fix redis-check-aof misidentifying data in manifest format as MP-AOF
  (Redis#12951)  
* Update redis-check-rdb types to replace stream-v2 with stream-v3
  (Redis#12969)

### <a id="725-ga-valkey-released-tue-16-apr-2024"></a>Valkey 7.2.5 GA - Released Tue 16 Apr 2024

Upgrade urgency **LOW**.

This is the first stable release of Valkey 7.2.5.

#### <a id="725-ga-changes-to-support-valkey-branding"></a>Changes to support Valkey branding

* Update template config files to remove references of redis.io and replace them
  with valkey.io. ([#320])

### <a id="725-rc1-valkey-released-fri-12-apr-2024"></a>Valkey 7.2.5 RC1 - Released Fri 12 Apr 2024

Upgrade urgency **LOW**.

Second release candidate for Valkey with API compatibility
for OSS Redis 7.2.4. Moving to a release candidate on 7.2.5, to make it clearer
this is a patch iteration as opposed to an exact copy of OSS Redis. Also includes
fixes to minor bugs present in 7.2.4 RC1 and more compatibility changes.

#### <a id="725-rc1-changes-to-support-valkey-branding"></a>Changes to support Valkey branding

* Update README to remove Redis references.
* Update valkey-server and valkey-cli help info to show only Valkey ([#222])
* Add compatibility for lua debugger to use 'server' instead of redis. ([#303])

#### <a id="725-rc1-bug-fixes"></a>Bug fixes

* Fix module event name to maintain Redis compatibility. ([#289])
* Fix issue where Redis symlinks were created with the wrong name. ([#282])

### <a id="724-rc1-valkey-released-tue-09-apr-2024"></a>Valkey 7.2.4 RC1 - Released Tue 09 Apr 2024

Upgrade urgency **LOW**.

Initial release of Valkey with API compatibility for OSS
Redis 7.2.4. This release is based on OSS Redis 7.2.4, with additional
functionality to better brand the server as Valkey instead of Redis. All APIs
are fully backwards compatible and care was taken to minimize the number of
log lines that were changed to best support existing tooling around log parsing.

#### <a id="724-rc1-changes-to-support-valkey-branding"></a>Changes to support Valkey branding

* Rename the 6 Redis binaries to ones with `valkey` prefixes: `valkey-server`,
  `valkey-cli`, `valkey-benchmark`, `valkey-check-aof`, `valkey-check-rdb` and
  `valkey-sentinel`. ([#62])
* During install, create symlinks mapping the corresponding Redis binary names
  to the new Valkey binaries. ([#193])
* INFO fields: Introduce `valkey_version` and `server_name` fields. The
  `redis_version` will continue to be present and will indicate the Redis OSS
  version that the server is compatible with. ([#47], [#232])
* RDB file format: Introduce a `valkey-ver` RDB field to indicate an RDB file
  was produced by a Valkey server. This field is ignored when the file is
  loaded by Redis OSS. ([#47])
* Module API changes: Introduce Valkey Module API in a new file, valkeymodule.h,
  with functions and types prefixed by ValkeyModule. Valkey is still fully ABI
  compatible with the Redis Module API, meaning Valkey supports running modules
  compiled with either the Redis or Valkey Module APIs. For full source
  compatibility, the Redis Module API (redismodule.h) is also kept with the
  RedisModule prefixed functions and types. ([#194], [#243], [#262])
* Scripting: Introduce a new top level `server` object for functions and scripts
  that can be instead of the existing `redis` object. This allows users to
  replace calls like `redis.call(...)` with `server.call(...)`. ([#213])
* Makefile: Introduce `SERVER_CFLAGS` and `SERVER_LDFLAGS` as an alternative to
  `REDIS_CFLAGS` and `REDIS_LDFLAGS`. ([#46])
* Update template config files to replace references to Redis with Valkey. The
  file valkey.conf replaces redis.conf. ([#29], [#171])
* Logging: Update startup, shutdown, and help logs to reference Valkey instead of
  Redis. Valkey server will also show the Valkey logo at startup and show the
  Valkey repositories when crashing. ([#251], [#252], [#263], [#113])

#### <a id="724-rc1-bug-fixes"></a>Bug fixes

* Cluster: Fix an issue where cluster nodes running on Redis versions earlier
  than 7.0 would be unable to communicate with nodes running on Valkey 7.2. This
  change also introduces a slight delay when hostnames are not displayed when a
  node is first added to the cluster. ([#52])

### <a id="72-valkey-acknowledgments"></a>Valkey 7.2 Acknowledgments

A special thank you for the amount of work put into this release by:

- Viktor Söderqvist
- Madelyn Olson
- Wen Hui
- Ping Xie
- Parth Patel
- Roshan Katri
- Zhu Binbin
- Zhao Zhao
- Bany
- Harkrishn Patro
- Vitah Lin
- Ziyang Zeng (For creating the logo!)
- The many other community members who provided their support!

[#1045]: https://github.com/valkey-io/valkey/pull/1045
[#1044]: https://github.com/valkey-io/valkey/pull/1044
[#1043]: https://github.com/valkey-io/valkey/pull/1043
[#1042]: https://github.com/valkey-io/valkey/pull/1042
[#1041]: https://github.com/valkey-io/valkey/pull/1041
[#1040]: https://github.com/valkey-io/valkey/pull/1040
[#1039]: https://github.com/valkey-io/valkey/pull/1039
[#1038]: https://github.com/valkey-io/valkey/pull/1038
[#1037]: https://github.com/valkey-io/valkey/pull/1037
[#1036]: https://github.com/valkey-io/valkey/pull/1036
[#1035]: https://github.com/valkey-io/valkey/pull/1035
[#1034]: https://github.com/valkey-io/valkey/pull/1034
[#1033]: https://github.com/valkey-io/valkey/pull/1033
[#1032]: https://github.com/valkey-io/valkey/pull/1032
[#1031]: https://github.com/valkey-io/valkey/pull/1031
[#1030]: https://github.com/valkey-io/valkey/pull/1030
[#1029]: https://github.com/valkey-io/valkey/pull/1029
[#1028]: https://github.com/valkey-io/valkey/pull/1028
[#1027]: https://github.com/valkey-io/valkey/pull/1027
[#1026]: https://github.com/valkey-io/valkey/pull/1026
[#1025]: https://github.com/valkey-io/valkey/pull/1025
[#1024]: https://github.com/valkey-io/valkey/pull/1024
[#1023]: https://github.com/valkey-io/valkey/pull/1023
[#1022]: https://github.com/valkey-io/valkey/pull/1022
[#1021]: https://github.com/valkey-io/valkey/pull/1021
[#1020]: https://github.com/valkey-io/valkey/pull/1020
[#1019]: https://github.com/valkey-io/valkey/pull/1019
[#1018]: https://github.com/valkey-io/valkey/pull/1018
[#1017]: https://github.com/valkey-io/valkey/pull/1017
[#1016]: https://github.com/valkey-io/valkey/pull/1016
[#1015]: https://github.com/valkey-io/valkey/pull/1015
[#1014]: https://github.com/valkey-io/valkey/pull/1014
[#1013]: https://github.com/valkey-io/valkey/pull/1013
[#1012]: https://github.com/valkey-io/valkey/pull/1012
[#1011]: https://github.com/valkey-io/valkey/pull/1011
[#1010]: https://github.com/valkey-io/valkey/pull/1010
[#1009]: https://github.com/valkey-io/valkey/pull/1009
[#1008]: https://github.com/valkey-io/valkey/pull/1008
[#1007]: https://github.com/valkey-io/valkey/pull/1007
[#1006]: https://github.com/valkey-io/valkey/pull/1006
[#1005]: https://github.com/valkey-io/valkey/pull/1005
[#1004]: https://github.com/valkey-io/valkey/pull/1004
[#1003]: https://github.com/valkey-io/valkey/pull/1003
[#1002]: https://github.com/valkey-io/valkey/pull/1002
[#1001]: https://github.com/valkey-io/valkey/pull/1001
[#1000]: https://github.com/valkey-io/valkey/pull/1000
[#999]: https://github.com/valkey-io/valkey/pull/999
[#998]: https://github.com/valkey-io/valkey/pull/998
[#997]: https://github.com/valkey-io/valkey/pull/997
[#996]: https://github.com/valkey-io/valkey/pull/996
[#995]: https://github.com/valkey-io/valkey/pull/995
[#994]: https://github.com/valkey-io/valkey/pull/994
[#993]: https://github.com/valkey-io/valkey/pull/993
[#992]: https://github.com/valkey-io/valkey/pull/992
[#991]: https://github.com/valkey-io/valkey/pull/991
[#990]: https://github.com/valkey-io/valkey/pull/990
[#989]: https://github.com/valkey-io/valkey/pull/989
[#988]: https://github.com/valkey-io/valkey/pull/988
[#987]: https://github.com/valkey-io/valkey/pull/987
[#986]: https://github.com/valkey-io/valkey/pull/986
[#985]: https://github.com/valkey-io/valkey/pull/985
[#984]: https://github.com/valkey-io/valkey/pull/984
[#983]: https://github.com/valkey-io/valkey/pull/983
[#982]: https://github.com/valkey-io/valkey/pull/982
[#981]: https://github.com/valkey-io/valkey/pull/981
[#980]: https://github.com/valkey-io/valkey/pull/980
[#979]: https://github.com/valkey-io/valkey/pull/979
[#978]: https://github.com/valkey-io/valkey/pull/978
[#977]: https://github.com/valkey-io/valkey/pull/977
[#976]: https://github.com/valkey-io/valkey/pull/976
[#975]: https://github.com/valkey-io/valkey/pull/975
[#974]: https://github.com/valkey-io/valkey/pull/974
[#973]: https://github.com/valkey-io/valkey/pull/973
[#972]: https://github.com/valkey-io/valkey/pull/972
[#971]: https://github.com/valkey-io/valkey/pull/971
[#970]: https://github.com/valkey-io/valkey/pull/970
[#969]: https://github.com/valkey-io/valkey/pull/969
[#968]: https://github.com/valkey-io/valkey/pull/968
[#967]: https://github.com/valkey-io/valkey/pull/967
[#966]: https://github.com/valkey-io/valkey/pull/966
[#965]: https://github.com/valkey-io/valkey/pull/965
[#964]: https://github.com/valkey-io/valkey/pull/964
[#963]: https://github.com/valkey-io/valkey/pull/963
[#962]: https://github.com/valkey-io/valkey/pull/962
[#961]: https://github.com/valkey-io/valkey/pull/961
[#960]: https://github.com/valkey-io/valkey/pull/960
[#959]: https://github.com/valkey-io/valkey/pull/959
[#958]: https://github.com/valkey-io/valkey/pull/958
[#957]: https://github.com/valkey-io/valkey/pull/957
[#956]: https://github.com/valkey-io/valkey/pull/956
[#955]: https://github.com/valkey-io/valkey/pull/955
[#954]: https://github.com/valkey-io/valkey/pull/954
[#953]: https://github.com/valkey-io/valkey/pull/953
[#952]: https://github.com/valkey-io/valkey/pull/952
[#951]: https://github.com/valkey-io/valkey/pull/951
[#950]: https://github.com/valkey-io/valkey/pull/950
[#949]: https://github.com/valkey-io/valkey/pull/949
[#948]: https://github.com/valkey-io/valkey/pull/948
[#947]: https://github.com/valkey-io/valkey/pull/947
[#946]: https://github.com/valkey-io/valkey/pull/946
[#945]: https://github.com/valkey-io/valkey/pull/945
[#944]: https://github.com/valkey-io/valkey/pull/944
[#943]: https://github.com/valkey-io/valkey/pull/943
[#942]: https://github.com/valkey-io/valkey/pull/942
[#941]: https://github.com/valkey-io/valkey/pull/941
[#940]: https://github.com/valkey-io/valkey/pull/940
[#939]: https://github.com/valkey-io/valkey/pull/939
[#938]: https://github.com/valkey-io/valkey/pull/938
[#937]: https://github.com/valkey-io/valkey/pull/937
[#936]: https://github.com/valkey-io/valkey/pull/936
[#935]: https://github.com/valkey-io/valkey/pull/935
[#934]: https://github.com/valkey-io/valkey/pull/934
[#933]: https://github.com/valkey-io/valkey/pull/933
[#932]: https://github.com/valkey-io/valkey/pull/932
[#931]: https://github.com/valkey-io/valkey/pull/931
[#930]: https://github.com/valkey-io/valkey/pull/930
[#929]: https://github.com/valkey-io/valkey/pull/929
[#928]: https://github.com/valkey-io/valkey/pull/928
[#927]: https://github.com/valkey-io/valkey/pull/927
[#926]: https://github.com/valkey-io/valkey/pull/926
[#925]: https://github.com/valkey-io/valkey/pull/925
[#924]: https://github.com/valkey-io/valkey/pull/924
[#923]: https://github.com/valkey-io/valkey/pull/923
[#922]: https://github.com/valkey-io/valkey/pull/922
[#921]: https://github.com/valkey-io/valkey/pull/921
[#920]: https://github.com/valkey-io/valkey/pull/920
[#919]: https://github.com/valkey-io/valkey/pull/919
[#918]: https://github.com/valkey-io/valkey/pull/918
[#917]: https://github.com/valkey-io/valkey/pull/917
[#916]: https://github.com/valkey-io/valkey/pull/916
[#915]: https://github.com/valkey-io/valkey/pull/915
[#914]: https://github.com/valkey-io/valkey/pull/914
[#913]: https://github.com/valkey-io/valkey/pull/913
[#912]: https://github.com/valkey-io/valkey/pull/912
[#911]: https://github.com/valkey-io/valkey/pull/911
[#910]: https://github.com/valkey-io/valkey/pull/910
[#909]: https://github.com/valkey-io/valkey/pull/909
[#908]: https://github.com/valkey-io/valkey/pull/908
[#907]: https://github.com/valkey-io/valkey/pull/907
[#906]: https://github.com/valkey-io/valkey/pull/906
[#905]: https://github.com/valkey-io/valkey/pull/905
[#904]: https://github.com/valkey-io/valkey/pull/904
[#903]: https://github.com/valkey-io/valkey/pull/903
[#902]: https://github.com/valkey-io/valkey/pull/902
[#901]: https://github.com/valkey-io/valkey/pull/901
[#900]: https://github.com/valkey-io/valkey/pull/900
[#899]: https://github.com/valkey-io/valkey/pull/899
[#898]: https://github.com/valkey-io/valkey/pull/898
[#897]: https://github.com/valkey-io/valkey/pull/897
[#896]: https://github.com/valkey-io/valkey/pull/896
[#895]: https://github.com/valkey-io/valkey/pull/895
[#894]: https://github.com/valkey-io/valkey/pull/894
[#893]: https://github.com/valkey-io/valkey/pull/893
[#892]: https://github.com/valkey-io/valkey/pull/892
[#891]: https://github.com/valkey-io/valkey/pull/891
[#890]: https://github.com/valkey-io/valkey/pull/890
[#889]: https://github.com/valkey-io/valkey/pull/889
[#888]: https://github.com/valkey-io/valkey/pull/888
[#887]: https://github.com/valkey-io/valkey/pull/887
[#886]: https://github.com/valkey-io/valkey/pull/886
[#885]: https://github.com/valkey-io/valkey/pull/885
[#884]: https://github.com/valkey-io/valkey/pull/884
[#883]: https://github.com/valkey-io/valkey/pull/883
[#882]: https://github.com/valkey-io/valkey/pull/882
[#881]: https://github.com/valkey-io/valkey/pull/881
[#880]: https://github.com/valkey-io/valkey/pull/880
[#879]: https://github.com/valkey-io/valkey/pull/879
[#878]: https://github.com/valkey-io/valkey/pull/878
[#877]: https://github.com/valkey-io/valkey/pull/877
[#876]: https://github.com/valkey-io/valkey/pull/876
[#875]: https://github.com/valkey-io/valkey/pull/875
[#874]: https://github.com/valkey-io/valkey/pull/874
[#873]: https://github.com/valkey-io/valkey/pull/873
[#872]: https://github.com/valkey-io/valkey/pull/872
[#871]: https://github.com/valkey-io/valkey/pull/871
[#870]: https://github.com/valkey-io/valkey/pull/870
[#869]: https://github.com/valkey-io/valkey/pull/869
[#868]: https://github.com/valkey-io/valkey/pull/868
[#867]: https://github.com/valkey-io/valkey/pull/867
[#866]: https://github.com/valkey-io/valkey/pull/866
[#865]: https://github.com/valkey-io/valkey/pull/865
[#864]: https://github.com/valkey-io/valkey/pull/864
[#863]: https://github.com/valkey-io/valkey/pull/863
[#862]: https://github.com/valkey-io/valkey/pull/862
[#861]: https://github.com/valkey-io/valkey/pull/861
[#860]: https://github.com/valkey-io/valkey/pull/860
[#859]: https://github.com/valkey-io/valkey/pull/859
[#858]: https://github.com/valkey-io/valkey/pull/858
[#857]: https://github.com/valkey-io/valkey/pull/857
[#856]: https://github.com/valkey-io/valkey/pull/856
[#855]: https://github.com/valkey-io/valkey/pull/855
[#854]: https://github.com/valkey-io/valkey/pull/854
[#853]: https://github.com/valkey-io/valkey/pull/853
[#852]: https://github.com/valkey-io/valkey/pull/852
[#851]: https://github.com/valkey-io/valkey/pull/851
[#850]: https://github.com/valkey-io/valkey/pull/850
[#849]: https://github.com/valkey-io/valkey/pull/849
[#848]: https://github.com/valkey-io/valkey/pull/848
[#847]: https://github.com/valkey-io/valkey/pull/847
[#846]: https://github.com/valkey-io/valkey/pull/846
[#845]: https://github.com/valkey-io/valkey/pull/845
[#844]: https://github.com/valkey-io/valkey/pull/844
[#843]: https://github.com/valkey-io/valkey/pull/843
[#842]: https://github.com/valkey-io/valkey/pull/842
[#841]: https://github.com/valkey-io/valkey/pull/841
[#840]: https://github.com/valkey-io/valkey/pull/840
[#839]: https://github.com/valkey-io/valkey/pull/839
[#838]: https://github.com/valkey-io/valkey/pull/838
[#837]: https://github.com/valkey-io/valkey/pull/837
[#836]: https://github.com/valkey-io/valkey/pull/836
[#835]: https://github.com/valkey-io/valkey/pull/835
[#834]: https://github.com/valkey-io/valkey/pull/834
[#833]: https://github.com/valkey-io/valkey/pull/833
[#832]: https://github.com/valkey-io/valkey/pull/832
[#831]: https://github.com/valkey-io/valkey/pull/831
[#830]: https://github.com/valkey-io/valkey/pull/830
[#829]: https://github.com/valkey-io/valkey/pull/829
[#828]: https://github.com/valkey-io/valkey/pull/828
[#827]: https://github.com/valkey-io/valkey/pull/827
[#826]: https://github.com/valkey-io/valkey/pull/826
[#825]: https://github.com/valkey-io/valkey/pull/825
[#824]: https://github.com/valkey-io/valkey/pull/824
[#823]: https://github.com/valkey-io/valkey/pull/823
[#822]: https://github.com/valkey-io/valkey/pull/822
[#821]: https://github.com/valkey-io/valkey/pull/821
[#820]: https://github.com/valkey-io/valkey/pull/820
[#819]: https://github.com/valkey-io/valkey/pull/819
[#818]: https://github.com/valkey-io/valkey/pull/818
[#817]: https://github.com/valkey-io/valkey/pull/817
[#816]: https://github.com/valkey-io/valkey/pull/816
[#815]: https://github.com/valkey-io/valkey/pull/815
[#814]: https://github.com/valkey-io/valkey/pull/814
[#813]: https://github.com/valkey-io/valkey/pull/813
[#812]: https://github.com/valkey-io/valkey/pull/812
[#811]: https://github.com/valkey-io/valkey/pull/811
[#810]: https://github.com/valkey-io/valkey/pull/810
[#809]: https://github.com/valkey-io/valkey/pull/809
[#808]: https://github.com/valkey-io/valkey/pull/808
[#807]: https://github.com/valkey-io/valkey/pull/807
[#806]: https://github.com/valkey-io/valkey/pull/806
[#805]: https://github.com/valkey-io/valkey/pull/805
[#804]: https://github.com/valkey-io/valkey/pull/804
[#803]: https://github.com/valkey-io/valkey/pull/803
[#802]: https://github.com/valkey-io/valkey/pull/802
[#801]: https://github.com/valkey-io/valkey/pull/801
[#800]: https://github.com/valkey-io/valkey/pull/800
[#799]: https://github.com/valkey-io/valkey/pull/799
[#798]: https://github.com/valkey-io/valkey/pull/798
[#797]: https://github.com/valkey-io/valkey/pull/797
[#796]: https://github.com/valkey-io/valkey/pull/796
[#795]: https://github.com/valkey-io/valkey/pull/795
[#794]: https://github.com/valkey-io/valkey/pull/794
[#793]: https://github.com/valkey-io/valkey/pull/793
[#792]: https://github.com/valkey-io/valkey/pull/792
[#791]: https://github.com/valkey-io/valkey/pull/791
[#790]: https://github.com/valkey-io/valkey/pull/790
[#789]: https://github.com/valkey-io/valkey/pull/789
[#788]: https://github.com/valkey-io/valkey/pull/788
[#787]: https://github.com/valkey-io/valkey/pull/787
[#786]: https://github.com/valkey-io/valkey/pull/786
[#785]: https://github.com/valkey-io/valkey/pull/785
[#784]: https://github.com/valkey-io/valkey/pull/784
[#783]: https://github.com/valkey-io/valkey/pull/783
[#782]: https://github.com/valkey-io/valkey/pull/782
[#781]: https://github.com/valkey-io/valkey/pull/781
[#780]: https://github.com/valkey-io/valkey/pull/780
[#779]: https://github.com/valkey-io/valkey/pull/779
[#778]: https://github.com/valkey-io/valkey/pull/778
[#777]: https://github.com/valkey-io/valkey/pull/777
[#776]: https://github.com/valkey-io/valkey/pull/776
[#775]: https://github.com/valkey-io/valkey/pull/775
[#774]: https://github.com/valkey-io/valkey/pull/774
[#773]: https://github.com/valkey-io/valkey/pull/773
[#772]: https://github.com/valkey-io/valkey/pull/772
[#771]: https://github.com/valkey-io/valkey/pull/771
[#770]: https://github.com/valkey-io/valkey/pull/770
[#769]: https://github.com/valkey-io/valkey/pull/769
[#768]: https://github.com/valkey-io/valkey/pull/768
[#767]: https://github.com/valkey-io/valkey/pull/767
[#766]: https://github.com/valkey-io/valkey/pull/766
[#765]: https://github.com/valkey-io/valkey/pull/765
[#764]: https://github.com/valkey-io/valkey/pull/764
[#763]: https://github.com/valkey-io/valkey/pull/763
[#762]: https://github.com/valkey-io/valkey/pull/762
[#761]: https://github.com/valkey-io/valkey/pull/761
[#760]: https://github.com/valkey-io/valkey/pull/760
[#759]: https://github.com/valkey-io/valkey/pull/759
[#758]: https://github.com/valkey-io/valkey/pull/758
[#757]: https://github.com/valkey-io/valkey/pull/757
[#756]: https://github.com/valkey-io/valkey/pull/756
[#755]: https://github.com/valkey-io/valkey/pull/755
[#754]: https://github.com/valkey-io/valkey/pull/754
[#753]: https://github.com/valkey-io/valkey/pull/753
[#752]: https://github.com/valkey-io/valkey/pull/752
[#751]: https://github.com/valkey-io/valkey/pull/751
[#750]: https://github.com/valkey-io/valkey/pull/750
[#749]: https://github.com/valkey-io/valkey/pull/749
[#748]: https://github.com/valkey-io/valkey/pull/748
[#747]: https://github.com/valkey-io/valkey/pull/747
[#746]: https://github.com/valkey-io/valkey/pull/746
[#745]: https://github.com/valkey-io/valkey/pull/745
[#744]: https://github.com/valkey-io/valkey/pull/744
[#743]: https://github.com/valkey-io/valkey/pull/743
[#742]: https://github.com/valkey-io/valkey/pull/742
[#741]: https://github.com/valkey-io/valkey/pull/741
[#740]: https://github.com/valkey-io/valkey/pull/740
[#739]: https://github.com/valkey-io/valkey/pull/739
[#738]: https://github.com/valkey-io/valkey/pull/738
[#737]: https://github.com/valkey-io/valkey/pull/737
[#736]: https://github.com/valkey-io/valkey/pull/736
[#735]: https://github.com/valkey-io/valkey/pull/735
[#734]: https://github.com/valkey-io/valkey/pull/734
[#733]: https://github.com/valkey-io/valkey/pull/733
[#732]: https://github.com/valkey-io/valkey/pull/732
[#731]: https://github.com/valkey-io/valkey/pull/731
[#730]: https://github.com/valkey-io/valkey/pull/730
[#729]: https://github.com/valkey-io/valkey/pull/729
[#728]: https://github.com/valkey-io/valkey/pull/728
[#727]: https://github.com/valkey-io/valkey/pull/727
[#726]: https://github.com/valkey-io/valkey/pull/726
[#725]: https://github.com/valkey-io/valkey/pull/725
[#724]: https://github.com/valkey-io/valkey/pull/724
[#723]: https://github.com/valkey-io/valkey/pull/723
[#722]: https://github.com/valkey-io/valkey/pull/722
[#721]: https://github.com/valkey-io/valkey/pull/721
[#720]: https://github.com/valkey-io/valkey/pull/720
[#719]: https://github.com/valkey-io/valkey/pull/719
[#718]: https://github.com/valkey-io/valkey/pull/718
[#717]: https://github.com/valkey-io/valkey/pull/717
[#716]: https://github.com/valkey-io/valkey/pull/716
[#715]: https://github.com/valkey-io/valkey/pull/715
[#714]: https://github.com/valkey-io/valkey/pull/714
[#713]: https://github.com/valkey-io/valkey/pull/713
[#712]: https://github.com/valkey-io/valkey/pull/712
[#711]: https://github.com/valkey-io/valkey/pull/711
[#710]: https://github.com/valkey-io/valkey/pull/710
[#709]: https://github.com/valkey-io/valkey/pull/709
[#708]: https://github.com/valkey-io/valkey/pull/708
[#707]: https://github.com/valkey-io/valkey/pull/707
[#706]: https://github.com/valkey-io/valkey/pull/706
[#705]: https://github.com/valkey-io/valkey/pull/705
[#704]: https://github.com/valkey-io/valkey/pull/704
[#703]: https://github.com/valkey-io/valkey/pull/703
[#702]: https://github.com/valkey-io/valkey/pull/702
[#701]: https://github.com/valkey-io/valkey/pull/701
[#700]: https://github.com/valkey-io/valkey/pull/700
[#699]: https://github.com/valkey-io/valkey/pull/699
[#698]: https://github.com/valkey-io/valkey/pull/698
[#697]: https://github.com/valkey-io/valkey/pull/697
[#696]: https://github.com/valkey-io/valkey/pull/696
[#695]: https://github.com/valkey-io/valkey/pull/695
[#694]: https://github.com/valkey-io/valkey/pull/694
[#693]: https://github.com/valkey-io/valkey/pull/693
[#692]: https://github.com/valkey-io/valkey/pull/692
[#691]: https://github.com/valkey-io/valkey/pull/691
[#690]: https://github.com/valkey-io/valkey/pull/690
[#689]: https://github.com/valkey-io/valkey/pull/689
[#688]: https://github.com/valkey-io/valkey/pull/688
[#687]: https://github.com/valkey-io/valkey/pull/687
[#686]: https://github.com/valkey-io/valkey/pull/686
[#685]: https://github.com/valkey-io/valkey/pull/685
[#684]: https://github.com/valkey-io/valkey/pull/684
[#683]: https://github.com/valkey-io/valkey/pull/683
[#682]: https://github.com/valkey-io/valkey/pull/682
[#681]: https://github.com/valkey-io/valkey/pull/681
[#680]: https://github.com/valkey-io/valkey/pull/680
[#679]: https://github.com/valkey-io/valkey/pull/679
[#678]: https://github.com/valkey-io/valkey/pull/678
[#677]: https://github.com/valkey-io/valkey/pull/677
[#676]: https://github.com/valkey-io/valkey/pull/676
[#675]: https://github.com/valkey-io/valkey/pull/675
[#674]: https://github.com/valkey-io/valkey/pull/674
[#673]: https://github.com/valkey-io/valkey/pull/673
[#672]: https://github.com/valkey-io/valkey/pull/672
[#671]: https://github.com/valkey-io/valkey/pull/671
[#670]: https://github.com/valkey-io/valkey/pull/670
[#669]: https://github.com/valkey-io/valkey/pull/669
[#668]: https://github.com/valkey-io/valkey/pull/668
[#667]: https://github.com/valkey-io/valkey/pull/667
[#666]: https://github.com/valkey-io/valkey/pull/666
[#665]: https://github.com/valkey-io/valkey/pull/665
[#664]: https://github.com/valkey-io/valkey/pull/664
[#663]: https://github.com/valkey-io/valkey/pull/663
[#662]: https://github.com/valkey-io/valkey/pull/662
[#661]: https://github.com/valkey-io/valkey/pull/661
[#660]: https://github.com/valkey-io/valkey/pull/660
[#659]: https://github.com/valkey-io/valkey/pull/659
[#658]: https://github.com/valkey-io/valkey/pull/658
[#657]: https://github.com/valkey-io/valkey/pull/657
[#656]: https://github.com/valkey-io/valkey/pull/656
[#655]: https://github.com/valkey-io/valkey/pull/655
[#654]: https://github.com/valkey-io/valkey/pull/654
[#653]: https://github.com/valkey-io/valkey/pull/653
[#652]: https://github.com/valkey-io/valkey/pull/652
[#651]: https://github.com/valkey-io/valkey/pull/651
[#650]: https://github.com/valkey-io/valkey/pull/650
[#649]: https://github.com/valkey-io/valkey/pull/649
[#648]: https://github.com/valkey-io/valkey/pull/648
[#647]: https://github.com/valkey-io/valkey/pull/647
[#646]: https://github.com/valkey-io/valkey/pull/646
[#645]: https://github.com/valkey-io/valkey/pull/645
[#644]: https://github.com/valkey-io/valkey/pull/644
[#643]: https://github.com/valkey-io/valkey/pull/643
[#642]: https://github.com/valkey-io/valkey/pull/642
[#641]: https://github.com/valkey-io/valkey/pull/641
[#640]: https://github.com/valkey-io/valkey/pull/640
[#639]: https://github.com/valkey-io/valkey/pull/639
[#638]: https://github.com/valkey-io/valkey/pull/638
[#637]: https://github.com/valkey-io/valkey/pull/637
[#636]: https://github.com/valkey-io/valkey/pull/636
[#635]: https://github.com/valkey-io/valkey/pull/635
[#634]: https://github.com/valkey-io/valkey/pull/634
[#633]: https://github.com/valkey-io/valkey/pull/633
[#632]: https://github.com/valkey-io/valkey/pull/632
[#631]: https://github.com/valkey-io/valkey/pull/631
[#630]: https://github.com/valkey-io/valkey/pull/630
[#629]: https://github.com/valkey-io/valkey/pull/629
[#628]: https://github.com/valkey-io/valkey/pull/628
[#627]: https://github.com/valkey-io/valkey/pull/627
[#626]: https://github.com/valkey-io/valkey/pull/626
[#625]: https://github.com/valkey-io/valkey/pull/625
[#624]: https://github.com/valkey-io/valkey/pull/624
[#623]: https://github.com/valkey-io/valkey/pull/623
[#622]: https://github.com/valkey-io/valkey/pull/622
[#621]: https://github.com/valkey-io/valkey/pull/621
[#620]: https://github.com/valkey-io/valkey/pull/620
[#619]: https://github.com/valkey-io/valkey/pull/619
[#618]: https://github.com/valkey-io/valkey/pull/618
[#617]: https://github.com/valkey-io/valkey/pull/617
[#616]: https://github.com/valkey-io/valkey/pull/616
[#615]: https://github.com/valkey-io/valkey/pull/615
[#614]: https://github.com/valkey-io/valkey/pull/614
[#613]: https://github.com/valkey-io/valkey/pull/613
[#612]: https://github.com/valkey-io/valkey/pull/612
[#611]: https://github.com/valkey-io/valkey/pull/611
[#610]: https://github.com/valkey-io/valkey/pull/610
[#609]: https://github.com/valkey-io/valkey/pull/609
[#608]: https://github.com/valkey-io/valkey/pull/608
[#607]: https://github.com/valkey-io/valkey/pull/607
[#606]: https://github.com/valkey-io/valkey/pull/606
[#605]: https://github.com/valkey-io/valkey/pull/605
[#604]: https://github.com/valkey-io/valkey/pull/604
[#603]: https://github.com/valkey-io/valkey/pull/603
[#602]: https://github.com/valkey-io/valkey/pull/602
[#601]: https://github.com/valkey-io/valkey/pull/601
[#600]: https://github.com/valkey-io/valkey/pull/600
[#599]: https://github.com/valkey-io/valkey/pull/599
[#598]: https://github.com/valkey-io/valkey/pull/598
[#597]: https://github.com/valkey-io/valkey/pull/597
[#596]: https://github.com/valkey-io/valkey/pull/596
[#595]: https://github.com/valkey-io/valkey/pull/595
[#594]: https://github.com/valkey-io/valkey/pull/594
[#593]: https://github.com/valkey-io/valkey/pull/593
[#592]: https://github.com/valkey-io/valkey/pull/592
[#591]: https://github.com/valkey-io/valkey/pull/591
[#590]: https://github.com/valkey-io/valkey/pull/590
[#589]: https://github.com/valkey-io/valkey/pull/589
[#588]: https://github.com/valkey-io/valkey/pull/588
[#587]: https://github.com/valkey-io/valkey/pull/587
[#586]: https://github.com/valkey-io/valkey/pull/586
[#585]: https://github.com/valkey-io/valkey/pull/585
[#584]: https://github.com/valkey-io/valkey/pull/584
[#583]: https://github.com/valkey-io/valkey/pull/583
[#582]: https://github.com/valkey-io/valkey/pull/582
[#581]: https://github.com/valkey-io/valkey/pull/581
[#580]: https://github.com/valkey-io/valkey/pull/580
[#579]: https://github.com/valkey-io/valkey/pull/579
[#578]: https://github.com/valkey-io/valkey/pull/578
[#577]: https://github.com/valkey-io/valkey/pull/577
[#576]: https://github.com/valkey-io/valkey/pull/576
[#575]: https://github.com/valkey-io/valkey/pull/575
[#574]: https://github.com/valkey-io/valkey/pull/574
[#573]: https://github.com/valkey-io/valkey/pull/573
[#572]: https://github.com/valkey-io/valkey/pull/572
[#571]: https://github.com/valkey-io/valkey/pull/571
[#570]: https://github.com/valkey-io/valkey/pull/570
[#569]: https://github.com/valkey-io/valkey/pull/569
[#568]: https://github.com/valkey-io/valkey/pull/568
[#567]: https://github.com/valkey-io/valkey/pull/567
[#566]: https://github.com/valkey-io/valkey/pull/566
[#565]: https://github.com/valkey-io/valkey/pull/565
[#564]: https://github.com/valkey-io/valkey/pull/564
[#563]: https://github.com/valkey-io/valkey/pull/563
[#562]: https://github.com/valkey-io/valkey/pull/562
[#561]: https://github.com/valkey-io/valkey/pull/561
[#560]: https://github.com/valkey-io/valkey/pull/560
[#559]: https://github.com/valkey-io/valkey/pull/559
[#558]: https://github.com/valkey-io/valkey/pull/558
[#557]: https://github.com/valkey-io/valkey/pull/557
[#556]: https://github.com/valkey-io/valkey/pull/556
[#555]: https://github.com/valkey-io/valkey/pull/555
[#554]: https://github.com/valkey-io/valkey/pull/554
[#553]: https://github.com/valkey-io/valkey/pull/553
[#552]: https://github.com/valkey-io/valkey/pull/552
[#551]: https://github.com/valkey-io/valkey/pull/551
[#550]: https://github.com/valkey-io/valkey/pull/550
[#549]: https://github.com/valkey-io/valkey/pull/549
[#548]: https://github.com/valkey-io/valkey/pull/548
[#547]: https://github.com/valkey-io/valkey/pull/547
[#546]: https://github.com/valkey-io/valkey/pull/546
[#545]: https://github.com/valkey-io/valkey/pull/545
[#544]: https://github.com/valkey-io/valkey/pull/544
[#543]: https://github.com/valkey-io/valkey/pull/543
[#542]: https://github.com/valkey-io/valkey/pull/542
[#541]: https://github.com/valkey-io/valkey/pull/541
[#540]: https://github.com/valkey-io/valkey/pull/540
[#539]: https://github.com/valkey-io/valkey/pull/539
[#538]: https://github.com/valkey-io/valkey/pull/538
[#537]: https://github.com/valkey-io/valkey/pull/537
[#536]: https://github.com/valkey-io/valkey/pull/536
[#535]: https://github.com/valkey-io/valkey/pull/535
[#534]: https://github.com/valkey-io/valkey/pull/534
[#533]: https://github.com/valkey-io/valkey/pull/533
[#532]: https://github.com/valkey-io/valkey/pull/532
[#531]: https://github.com/valkey-io/valkey/pull/531
[#530]: https://github.com/valkey-io/valkey/pull/530
[#529]: https://github.com/valkey-io/valkey/pull/529
[#528]: https://github.com/valkey-io/valkey/pull/528
[#527]: https://github.com/valkey-io/valkey/pull/527
[#526]: https://github.com/valkey-io/valkey/pull/526
[#525]: https://github.com/valkey-io/valkey/pull/525
[#524]: https://github.com/valkey-io/valkey/pull/524
[#523]: https://github.com/valkey-io/valkey/pull/523
[#522]: https://github.com/valkey-io/valkey/pull/522
[#521]: https://github.com/valkey-io/valkey/pull/521
[#520]: https://github.com/valkey-io/valkey/pull/520
[#519]: https://github.com/valkey-io/valkey/pull/519
[#518]: https://github.com/valkey-io/valkey/pull/518
[#517]: https://github.com/valkey-io/valkey/pull/517
[#516]: https://github.com/valkey-io/valkey/pull/516
[#515]: https://github.com/valkey-io/valkey/pull/515
[#514]: https://github.com/valkey-io/valkey/pull/514
[#513]: https://github.com/valkey-io/valkey/pull/513
[#512]: https://github.com/valkey-io/valkey/pull/512
[#511]: https://github.com/valkey-io/valkey/pull/511
[#510]: https://github.com/valkey-io/valkey/pull/510
[#509]: https://github.com/valkey-io/valkey/pull/509
[#508]: https://github.com/valkey-io/valkey/pull/508
[#507]: https://github.com/valkey-io/valkey/pull/507
[#506]: https://github.com/valkey-io/valkey/pull/506
[#505]: https://github.com/valkey-io/valkey/pull/505
[#504]: https://github.com/valkey-io/valkey/pull/504
[#503]: https://github.com/valkey-io/valkey/pull/503
[#502]: https://github.com/valkey-io/valkey/pull/502
[#501]: https://github.com/valkey-io/valkey/pull/501
[#500]: https://github.com/valkey-io/valkey/pull/500
[#499]: https://github.com/valkey-io/valkey/pull/499
[#498]: https://github.com/valkey-io/valkey/pull/498
[#497]: https://github.com/valkey-io/valkey/pull/497
[#496]: https://github.com/valkey-io/valkey/pull/496
[#495]: https://github.com/valkey-io/valkey/pull/495
[#494]: https://github.com/valkey-io/valkey/pull/494
[#493]: https://github.com/valkey-io/valkey/pull/493
[#492]: https://github.com/valkey-io/valkey/pull/492
[#491]: https://github.com/valkey-io/valkey/pull/491
[#490]: https://github.com/valkey-io/valkey/pull/490
[#489]: https://github.com/valkey-io/valkey/pull/489
[#488]: https://github.com/valkey-io/valkey/pull/488
[#487]: https://github.com/valkey-io/valkey/pull/487
[#486]: https://github.com/valkey-io/valkey/pull/486
[#485]: https://github.com/valkey-io/valkey/pull/485
[#484]: https://github.com/valkey-io/valkey/pull/484
[#483]: https://github.com/valkey-io/valkey/pull/483
[#482]: https://github.com/valkey-io/valkey/pull/482
[#481]: https://github.com/valkey-io/valkey/pull/481
[#480]: https://github.com/valkey-io/valkey/pull/480
[#479]: https://github.com/valkey-io/valkey/pull/479
[#478]: https://github.com/valkey-io/valkey/pull/478
[#477]: https://github.com/valkey-io/valkey/pull/477
[#476]: https://github.com/valkey-io/valkey/pull/476
[#475]: https://github.com/valkey-io/valkey/pull/475
[#474]: https://github.com/valkey-io/valkey/pull/474
[#473]: https://github.com/valkey-io/valkey/pull/473
[#472]: https://github.com/valkey-io/valkey/pull/472
[#471]: https://github.com/valkey-io/valkey/pull/471
[#470]: https://github.com/valkey-io/valkey/pull/470
[#469]: https://github.com/valkey-io/valkey/pull/469
[#468]: https://github.com/valkey-io/valkey/pull/468
[#467]: https://github.com/valkey-io/valkey/pull/467
[#466]: https://github.com/valkey-io/valkey/pull/466
[#465]: https://github.com/valkey-io/valkey/pull/465
[#464]: https://github.com/valkey-io/valkey/pull/464
[#463]: https://github.com/valkey-io/valkey/pull/463
[#462]: https://github.com/valkey-io/valkey/pull/462
[#461]: https://github.com/valkey-io/valkey/pull/461
[#460]: https://github.com/valkey-io/valkey/pull/460
[#459]: https://github.com/valkey-io/valkey/pull/459
[#458]: https://github.com/valkey-io/valkey/pull/458
[#457]: https://github.com/valkey-io/valkey/pull/457
[#456]: https://github.com/valkey-io/valkey/pull/456
[#455]: https://github.com/valkey-io/valkey/pull/455
[#454]: https://github.com/valkey-io/valkey/pull/454
[#453]: https://github.com/valkey-io/valkey/pull/453
[#452]: https://github.com/valkey-io/valkey/pull/452
[#451]: https://github.com/valkey-io/valkey/pull/451
[#450]: https://github.com/valkey-io/valkey/pull/450
[#449]: https://github.com/valkey-io/valkey/pull/449
[#448]: https://github.com/valkey-io/valkey/pull/448
[#447]: https://github.com/valkey-io/valkey/pull/447
[#446]: https://github.com/valkey-io/valkey/pull/446
[#445]: https://github.com/valkey-io/valkey/pull/445
[#444]: https://github.com/valkey-io/valkey/pull/444
[#443]: https://github.com/valkey-io/valkey/pull/443
[#442]: https://github.com/valkey-io/valkey/pull/442
[#441]: https://github.com/valkey-io/valkey/pull/441
[#440]: https://github.com/valkey-io/valkey/pull/440
[#439]: https://github.com/valkey-io/valkey/pull/439
[#438]: https://github.com/valkey-io/valkey/pull/438
[#437]: https://github.com/valkey-io/valkey/pull/437
[#436]: https://github.com/valkey-io/valkey/pull/436
[#435]: https://github.com/valkey-io/valkey/pull/435
[#434]: https://github.com/valkey-io/valkey/pull/434
[#433]: https://github.com/valkey-io/valkey/pull/433
[#432]: https://github.com/valkey-io/valkey/pull/432
[#431]: https://github.com/valkey-io/valkey/pull/431
[#430]: https://github.com/valkey-io/valkey/pull/430
[#429]: https://github.com/valkey-io/valkey/pull/429
[#428]: https://github.com/valkey-io/valkey/pull/428
[#427]: https://github.com/valkey-io/valkey/pull/427
[#426]: https://github.com/valkey-io/valkey/pull/426
[#425]: https://github.com/valkey-io/valkey/pull/425
[#424]: https://github.com/valkey-io/valkey/pull/424
[#423]: https://github.com/valkey-io/valkey/pull/423
[#422]: https://github.com/valkey-io/valkey/pull/422
[#421]: https://github.com/valkey-io/valkey/pull/421
[#420]: https://github.com/valkey-io/valkey/pull/420
[#419]: https://github.com/valkey-io/valkey/pull/419
[#418]: https://github.com/valkey-io/valkey/pull/418
[#417]: https://github.com/valkey-io/valkey/pull/417
[#416]: https://github.com/valkey-io/valkey/pull/416
[#415]: https://github.com/valkey-io/valkey/pull/415
[#414]: https://github.com/valkey-io/valkey/pull/414
[#413]: https://github.com/valkey-io/valkey/pull/413
[#412]: https://github.com/valkey-io/valkey/pull/412
[#411]: https://github.com/valkey-io/valkey/pull/411
[#410]: https://github.com/valkey-io/valkey/pull/410
[#409]: https://github.com/valkey-io/valkey/pull/409
[#408]: https://github.com/valkey-io/valkey/pull/408
[#407]: https://github.com/valkey-io/valkey/pull/407
[#406]: https://github.com/valkey-io/valkey/pull/406
[#405]: https://github.com/valkey-io/valkey/pull/405
[#404]: https://github.com/valkey-io/valkey/pull/404
[#403]: https://github.com/valkey-io/valkey/pull/403
[#402]: https://github.com/valkey-io/valkey/pull/402
[#401]: https://github.com/valkey-io/valkey/pull/401
[#400]: https://github.com/valkey-io/valkey/pull/400
[#399]: https://github.com/valkey-io/valkey/pull/399
[#398]: https://github.com/valkey-io/valkey/pull/398
[#397]: https://github.com/valkey-io/valkey/pull/397
[#396]: https://github.com/valkey-io/valkey/pull/396
[#395]: https://github.com/valkey-io/valkey/pull/395
[#394]: https://github.com/valkey-io/valkey/pull/394
[#393]: https://github.com/valkey-io/valkey/pull/393
[#392]: https://github.com/valkey-io/valkey/pull/392
[#391]: https://github.com/valkey-io/valkey/pull/391
[#390]: https://github.com/valkey-io/valkey/pull/390
[#389]: https://github.com/valkey-io/valkey/pull/389
[#388]: https://github.com/valkey-io/valkey/pull/388
[#387]: https://github.com/valkey-io/valkey/pull/387
[#386]: https://github.com/valkey-io/valkey/pull/386
[#385]: https://github.com/valkey-io/valkey/pull/385
[#384]: https://github.com/valkey-io/valkey/pull/384
[#383]: https://github.com/valkey-io/valkey/pull/383
[#382]: https://github.com/valkey-io/valkey/pull/382
[#381]: https://github.com/valkey-io/valkey/pull/381
[#380]: https://github.com/valkey-io/valkey/pull/380
[#379]: https://github.com/valkey-io/valkey/pull/379
[#378]: https://github.com/valkey-io/valkey/pull/378
[#377]: https://github.com/valkey-io/valkey/pull/377
[#376]: https://github.com/valkey-io/valkey/pull/376
[#375]: https://github.com/valkey-io/valkey/pull/375
[#374]: https://github.com/valkey-io/valkey/pull/374
[#373]: https://github.com/valkey-io/valkey/pull/373
[#372]: https://github.com/valkey-io/valkey/pull/372
[#371]: https://github.com/valkey-io/valkey/pull/371
[#370]: https://github.com/valkey-io/valkey/pull/370
[#369]: https://github.com/valkey-io/valkey/pull/369
[#368]: https://github.com/valkey-io/valkey/pull/368
[#367]: https://github.com/valkey-io/valkey/pull/367
[#366]: https://github.com/valkey-io/valkey/pull/366
[#365]: https://github.com/valkey-io/valkey/pull/365
[#364]: https://github.com/valkey-io/valkey/pull/364
[#363]: https://github.com/valkey-io/valkey/pull/363
[#362]: https://github.com/valkey-io/valkey/pull/362
[#361]: https://github.com/valkey-io/valkey/pull/361
[#360]: https://github.com/valkey-io/valkey/pull/360
[#359]: https://github.com/valkey-io/valkey/pull/359
[#358]: https://github.com/valkey-io/valkey/pull/358
[#357]: https://github.com/valkey-io/valkey/pull/357
[#356]: https://github.com/valkey-io/valkey/pull/356
[#355]: https://github.com/valkey-io/valkey/pull/355
[#354]: https://github.com/valkey-io/valkey/pull/354
[#353]: https://github.com/valkey-io/valkey/pull/353
[#352]: https://github.com/valkey-io/valkey/pull/352
[#351]: https://github.com/valkey-io/valkey/pull/351
[#350]: https://github.com/valkey-io/valkey/pull/350
[#349]: https://github.com/valkey-io/valkey/pull/349
[#348]: https://github.com/valkey-io/valkey/pull/348
[#347]: https://github.com/valkey-io/valkey/pull/347
[#346]: https://github.com/valkey-io/valkey/pull/346
[#345]: https://github.com/valkey-io/valkey/pull/345
[#344]: https://github.com/valkey-io/valkey/pull/344
[#343]: https://github.com/valkey-io/valkey/pull/343
[#342]: https://github.com/valkey-io/valkey/pull/342
[#341]: https://github.com/valkey-io/valkey/pull/341
[#340]: https://github.com/valkey-io/valkey/pull/340
[#339]: https://github.com/valkey-io/valkey/pull/339
[#338]: https://github.com/valkey-io/valkey/pull/338
[#337]: https://github.com/valkey-io/valkey/pull/337
[#336]: https://github.com/valkey-io/valkey/pull/336
[#335]: https://github.com/valkey-io/valkey/pull/335
[#334]: https://github.com/valkey-io/valkey/pull/334
[#333]: https://github.com/valkey-io/valkey/pull/333
[#332]: https://github.com/valkey-io/valkey/pull/332
[#331]: https://github.com/valkey-io/valkey/pull/331
[#330]: https://github.com/valkey-io/valkey/pull/330
[#329]: https://github.com/valkey-io/valkey/pull/329
[#328]: https://github.com/valkey-io/valkey/pull/328
[#327]: https://github.com/valkey-io/valkey/pull/327
[#326]: https://github.com/valkey-io/valkey/pull/326
[#325]: https://github.com/valkey-io/valkey/pull/325
[#324]: https://github.com/valkey-io/valkey/pull/324
[#323]: https://github.com/valkey-io/valkey/pull/323
[#322]: https://github.com/valkey-io/valkey/pull/322
[#321]: https://github.com/valkey-io/valkey/pull/321
[#320]: https://github.com/valkey-io/valkey/pull/320
[#319]: https://github.com/valkey-io/valkey/pull/319
[#318]: https://github.com/valkey-io/valkey/pull/318
[#317]: https://github.com/valkey-io/valkey/pull/317
[#316]: https://github.com/valkey-io/valkey/pull/316
[#315]: https://github.com/valkey-io/valkey/pull/315
[#314]: https://github.com/valkey-io/valkey/pull/314
[#313]: https://github.com/valkey-io/valkey/pull/313
[#312]: https://github.com/valkey-io/valkey/pull/312
[#311]: https://github.com/valkey-io/valkey/pull/311
[#310]: https://github.com/valkey-io/valkey/pull/310
[#309]: https://github.com/valkey-io/valkey/pull/309
[#308]: https://github.com/valkey-io/valkey/pull/308
[#307]: https://github.com/valkey-io/valkey/pull/307
[#306]: https://github.com/valkey-io/valkey/pull/306
[#305]: https://github.com/valkey-io/valkey/pull/305
[#304]: https://github.com/valkey-io/valkey/pull/304
[#303]: https://github.com/valkey-io/valkey/pull/303
[#302]: https://github.com/valkey-io/valkey/pull/302
[#301]: https://github.com/valkey-io/valkey/pull/301
[#300]: https://github.com/valkey-io/valkey/pull/300
[#299]: https://github.com/valkey-io/valkey/pull/299
[#298]: https://github.com/valkey-io/valkey/pull/298
[#297]: https://github.com/valkey-io/valkey/pull/297
[#296]: https://github.com/valkey-io/valkey/pull/296
[#295]: https://github.com/valkey-io/valkey/pull/295
[#294]: https://github.com/valkey-io/valkey/pull/294
[#293]: https://github.com/valkey-io/valkey/pull/293
[#292]: https://github.com/valkey-io/valkey/pull/292
[#291]: https://github.com/valkey-io/valkey/pull/291
[#290]: https://github.com/valkey-io/valkey/pull/290
[#289]: https://github.com/valkey-io/valkey/pull/289
[#288]: https://github.com/valkey-io/valkey/pull/288
[#287]: https://github.com/valkey-io/valkey/pull/287
[#286]: https://github.com/valkey-io/valkey/pull/286
[#285]: https://github.com/valkey-io/valkey/pull/285
[#284]: https://github.com/valkey-io/valkey/pull/284
[#283]: https://github.com/valkey-io/valkey/pull/283
[#282]: https://github.com/valkey-io/valkey/pull/282
[#281]: https://github.com/valkey-io/valkey/pull/281
[#280]: https://github.com/valkey-io/valkey/pull/280
[#279]: https://github.com/valkey-io/valkey/pull/279
[#278]: https://github.com/valkey-io/valkey/pull/278
[#277]: https://github.com/valkey-io/valkey/pull/277
[#276]: https://github.com/valkey-io/valkey/pull/276
[#275]: https://github.com/valkey-io/valkey/pull/275
[#274]: https://github.com/valkey-io/valkey/pull/274
[#273]: https://github.com/valkey-io/valkey/pull/273
[#272]: https://github.com/valkey-io/valkey/pull/272
[#271]: https://github.com/valkey-io/valkey/pull/271
[#270]: https://github.com/valkey-io/valkey/pull/270
[#269]: https://github.com/valkey-io/valkey/pull/269
[#268]: https://github.com/valkey-io/valkey/pull/268
[#267]: https://github.com/valkey-io/valkey/pull/267
[#266]: https://github.com/valkey-io/valkey/pull/266
[#265]: https://github.com/valkey-io/valkey/pull/265
[#264]: https://github.com/valkey-io/valkey/pull/264
[#263]: https://github.com/valkey-io/valkey/pull/263
[#262]: https://github.com/valkey-io/valkey/pull/262
[#261]: https://github.com/valkey-io/valkey/pull/261
[#260]: https://github.com/valkey-io/valkey/pull/260
[#259]: https://github.com/valkey-io/valkey/pull/259
[#258]: https://github.com/valkey-io/valkey/pull/258
[#257]: https://github.com/valkey-io/valkey/pull/257
[#256]: https://github.com/valkey-io/valkey/pull/256
[#255]: https://github.com/valkey-io/valkey/pull/255
[#254]: https://github.com/valkey-io/valkey/pull/254
[#253]: https://github.com/valkey-io/valkey/pull/253
[#252]: https://github.com/valkey-io/valkey/pull/252
[#251]: https://github.com/valkey-io/valkey/pull/251
[#250]: https://github.com/valkey-io/valkey/pull/250
[#249]: https://github.com/valkey-io/valkey/pull/249
[#248]: https://github.com/valkey-io/valkey/pull/248
[#247]: https://github.com/valkey-io/valkey/pull/247
[#246]: https://github.com/valkey-io/valkey/pull/246
[#245]: https://github.com/valkey-io/valkey/pull/245
[#244]: https://github.com/valkey-io/valkey/pull/244
[#243]: https://github.com/valkey-io/valkey/pull/243
[#242]: https://github.com/valkey-io/valkey/pull/242
[#241]: https://github.com/valkey-io/valkey/pull/241
[#240]: https://github.com/valkey-io/valkey/pull/240
[#239]: https://github.com/valkey-io/valkey/pull/239
[#238]: https://github.com/valkey-io/valkey/pull/238
[#237]: https://github.com/valkey-io/valkey/pull/237
[#236]: https://github.com/valkey-io/valkey/pull/236
[#235]: https://github.com/valkey-io/valkey/pull/235
[#234]: https://github.com/valkey-io/valkey/pull/234
[#233]: https://github.com/valkey-io/valkey/pull/233
[#232]: https://github.com/valkey-io/valkey/pull/232
[#231]: https://github.com/valkey-io/valkey/pull/231
[#230]: https://github.com/valkey-io/valkey/pull/230
[#229]: https://github.com/valkey-io/valkey/pull/229
[#228]: https://github.com/valkey-io/valkey/pull/228
[#227]: https://github.com/valkey-io/valkey/pull/227
[#226]: https://github.com/valkey-io/valkey/pull/226
[#225]: https://github.com/valkey-io/valkey/pull/225
[#224]: https://github.com/valkey-io/valkey/pull/224
[#223]: https://github.com/valkey-io/valkey/pull/223
[#222]: https://github.com/valkey-io/valkey/pull/222
[#221]: https://github.com/valkey-io/valkey/pull/221
[#220]: https://github.com/valkey-io/valkey/pull/220
[#219]: https://github.com/valkey-io/valkey/pull/219
[#218]: https://github.com/valkey-io/valkey/pull/218
[#217]: https://github.com/valkey-io/valkey/pull/217
[#216]: https://github.com/valkey-io/valkey/pull/216
[#215]: https://github.com/valkey-io/valkey/pull/215
[#214]: https://github.com/valkey-io/valkey/pull/214
[#213]: https://github.com/valkey-io/valkey/pull/213
[#212]: https://github.com/valkey-io/valkey/pull/212
[#211]: https://github.com/valkey-io/valkey/pull/211
[#210]: https://github.com/valkey-io/valkey/pull/210
[#209]: https://github.com/valkey-io/valkey/pull/209
[#208]: https://github.com/valkey-io/valkey/pull/208
[#207]: https://github.com/valkey-io/valkey/pull/207
[#206]: https://github.com/valkey-io/valkey/pull/206
[#205]: https://github.com/valkey-io/valkey/pull/205
[#204]: https://github.com/valkey-io/valkey/pull/204
[#203]: https://github.com/valkey-io/valkey/pull/203
[#202]: https://github.com/valkey-io/valkey/pull/202
[#201]: https://github.com/valkey-io/valkey/pull/201
[#200]: https://github.com/valkey-io/valkey/pull/200
[#199]: https://github.com/valkey-io/valkey/pull/199
[#198]: https://github.com/valkey-io/valkey/pull/198
[#197]: https://github.com/valkey-io/valkey/pull/197
[#196]: https://github.com/valkey-io/valkey/pull/196
[#195]: https://github.com/valkey-io/valkey/pull/195
[#194]: https://github.com/valkey-io/valkey/pull/194
[#193]: https://github.com/valkey-io/valkey/pull/193
[#192]: https://github.com/valkey-io/valkey/pull/192
[#191]: https://github.com/valkey-io/valkey/pull/191
[#190]: https://github.com/valkey-io/valkey/pull/190
[#189]: https://github.com/valkey-io/valkey/pull/189
[#188]: https://github.com/valkey-io/valkey/pull/188
[#187]: https://github.com/valkey-io/valkey/pull/187
[#186]: https://github.com/valkey-io/valkey/pull/186
[#185]: https://github.com/valkey-io/valkey/pull/185
[#184]: https://github.com/valkey-io/valkey/pull/184
[#183]: https://github.com/valkey-io/valkey/pull/183
[#182]: https://github.com/valkey-io/valkey/pull/182
[#181]: https://github.com/valkey-io/valkey/pull/181
[#180]: https://github.com/valkey-io/valkey/pull/180
[#179]: https://github.com/valkey-io/valkey/pull/179
[#178]: https://github.com/valkey-io/valkey/pull/178
[#177]: https://github.com/valkey-io/valkey/pull/177
[#176]: https://github.com/valkey-io/valkey/pull/176
[#175]: https://github.com/valkey-io/valkey/pull/175
[#174]: https://github.com/valkey-io/valkey/pull/174
[#173]: https://github.com/valkey-io/valkey/pull/173
[#172]: https://github.com/valkey-io/valkey/pull/172
[#171]: https://github.com/valkey-io/valkey/pull/171
[#170]: https://github.com/valkey-io/valkey/pull/170
[#169]: https://github.com/valkey-io/valkey/pull/169
[#168]: https://github.com/valkey-io/valkey/pull/168
[#167]: https://github.com/valkey-io/valkey/pull/167
[#166]: https://github.com/valkey-io/valkey/pull/166
[#165]: https://github.com/valkey-io/valkey/pull/165
[#164]: https://github.com/valkey-io/valkey/pull/164
[#163]: https://github.com/valkey-io/valkey/pull/163
[#162]: https://github.com/valkey-io/valkey/pull/162
[#161]: https://github.com/valkey-io/valkey/pull/161
[#160]: https://github.com/valkey-io/valkey/pull/160
[#159]: https://github.com/valkey-io/valkey/pull/159
[#158]: https://github.com/valkey-io/valkey/pull/158
[#157]: https://github.com/valkey-io/valkey/pull/157
[#156]: https://github.com/valkey-io/valkey/pull/156
[#155]: https://github.com/valkey-io/valkey/pull/155
[#154]: https://github.com/valkey-io/valkey/pull/154
[#153]: https://github.com/valkey-io/valkey/pull/153
[#152]: https://github.com/valkey-io/valkey/pull/152
[#151]: https://github.com/valkey-io/valkey/pull/151
[#150]: https://github.com/valkey-io/valkey/pull/150
[#149]: https://github.com/valkey-io/valkey/pull/149
[#148]: https://github.com/valkey-io/valkey/pull/148
[#147]: https://github.com/valkey-io/valkey/pull/147
[#146]: https://github.com/valkey-io/valkey/pull/146
[#145]: https://github.com/valkey-io/valkey/pull/145
[#144]: https://github.com/valkey-io/valkey/pull/144
[#143]: https://github.com/valkey-io/valkey/pull/143
[#142]: https://github.com/valkey-io/valkey/pull/142
[#141]: https://github.com/valkey-io/valkey/pull/141
[#140]: https://github.com/valkey-io/valkey/pull/140
[#139]: https://github.com/valkey-io/valkey/pull/139
[#138]: https://github.com/valkey-io/valkey/pull/138
[#137]: https://github.com/valkey-io/valkey/pull/137
[#136]: https://github.com/valkey-io/valkey/pull/136
[#135]: https://github.com/valkey-io/valkey/pull/135
[#134]: https://github.com/valkey-io/valkey/pull/134
[#133]: https://github.com/valkey-io/valkey/pull/133
[#132]: https://github.com/valkey-io/valkey/pull/132
[#131]: https://github.com/valkey-io/valkey/pull/131
[#130]: https://github.com/valkey-io/valkey/pull/130
[#129]: https://github.com/valkey-io/valkey/pull/129
[#128]: https://github.com/valkey-io/valkey/pull/128
[#127]: https://github.com/valkey-io/valkey/pull/127
[#126]: https://github.com/valkey-io/valkey/pull/126
[#125]: https://github.com/valkey-io/valkey/pull/125
[#124]: https://github.com/valkey-io/valkey/pull/124
[#123]: https://github.com/valkey-io/valkey/pull/123
[#122]: https://github.com/valkey-io/valkey/pull/122
[#121]: https://github.com/valkey-io/valkey/pull/121
[#120]: https://github.com/valkey-io/valkey/pull/120
[#119]: https://github.com/valkey-io/valkey/pull/119
[#118]: https://github.com/valkey-io/valkey/pull/118
[#117]: https://github.com/valkey-io/valkey/pull/117
[#116]: https://github.com/valkey-io/valkey/pull/116
[#115]: https://github.com/valkey-io/valkey/pull/115
[#114]: https://github.com/valkey-io/valkey/pull/114
[#113]: https://github.com/valkey-io/valkey/pull/113
[#112]: https://github.com/valkey-io/valkey/pull/112
[#111]: https://github.com/valkey-io/valkey/pull/111
[#110]: https://github.com/valkey-io/valkey/pull/110
[#109]: https://github.com/valkey-io/valkey/pull/109
[#108]: https://github.com/valkey-io/valkey/pull/108
[#107]: https://github.com/valkey-io/valkey/pull/107
[#106]: https://github.com/valkey-io/valkey/pull/106
[#105]: https://github.com/valkey-io/valkey/pull/105
[#104]: https://github.com/valkey-io/valkey/pull/104
[#103]: https://github.com/valkey-io/valkey/pull/103
[#102]: https://github.com/valkey-io/valkey/pull/102
[#101]: https://github.com/valkey-io/valkey/pull/101
[#100]: https://github.com/valkey-io/valkey/pull/100
[#99]: https://github.com/valkey-io/valkey/pull/99
[#98]: https://github.com/valkey-io/valkey/pull/98
[#97]: https://github.com/valkey-io/valkey/pull/97
[#96]: https://github.com/valkey-io/valkey/pull/96
[#95]: https://github.com/valkey-io/valkey/pull/95
[#94]: https://github.com/valkey-io/valkey/pull/94
[#93]: https://github.com/valkey-io/valkey/pull/93
[#92]: https://github.com/valkey-io/valkey/pull/92
[#91]: https://github.com/valkey-io/valkey/pull/91
[#90]: https://github.com/valkey-io/valkey/pull/90
[#89]: https://github.com/valkey-io/valkey/pull/89
[#88]: https://github.com/valkey-io/valkey/pull/88
[#87]: https://github.com/valkey-io/valkey/pull/87
[#86]: https://github.com/valkey-io/valkey/pull/86
[#85]: https://github.com/valkey-io/valkey/pull/85
[#84]: https://github.com/valkey-io/valkey/pull/84
[#83]: https://github.com/valkey-io/valkey/pull/83
[#82]: https://github.com/valkey-io/valkey/pull/82
[#81]: https://github.com/valkey-io/valkey/pull/81
[#80]: https://github.com/valkey-io/valkey/pull/80
[#79]: https://github.com/valkey-io/valkey/pull/79
[#78]: https://github.com/valkey-io/valkey/pull/78
[#77]: https://github.com/valkey-io/valkey/pull/77
[#76]: https://github.com/valkey-io/valkey/pull/76
[#75]: https://github.com/valkey-io/valkey/pull/75
[#74]: https://github.com/valkey-io/valkey/pull/74
[#73]: https://github.com/valkey-io/valkey/pull/73
[#72]: https://github.com/valkey-io/valkey/pull/72
[#71]: https://github.com/valkey-io/valkey/pull/71
[#70]: https://github.com/valkey-io/valkey/pull/70
[#69]: https://github.com/valkey-io/valkey/pull/69
[#68]: https://github.com/valkey-io/valkey/pull/68
[#67]: https://github.com/valkey-io/valkey/pull/67
[#66]: https://github.com/valkey-io/valkey/pull/66
[#65]: https://github.com/valkey-io/valkey/pull/65
[#64]: https://github.com/valkey-io/valkey/pull/64
[#63]: https://github.com/valkey-io/valkey/pull/63
[#62]: https://github.com/valkey-io/valkey/pull/62
[#61]: https://github.com/valkey-io/valkey/pull/61
[#60]: https://github.com/valkey-io/valkey/pull/60
[#59]: https://github.com/valkey-io/valkey/pull/59
[#58]: https://github.com/valkey-io/valkey/pull/58
[#57]: https://github.com/valkey-io/valkey/pull/57
[#56]: https://github.com/valkey-io/valkey/pull/56
[#55]: https://github.com/valkey-io/valkey/pull/55
[#54]: https://github.com/valkey-io/valkey/pull/54
[#53]: https://github.com/valkey-io/valkey/pull/53
[#52]: https://github.com/valkey-io/valkey/pull/52
[#51]: https://github.com/valkey-io/valkey/pull/51
[#50]: https://github.com/valkey-io/valkey/pull/50
[#49]: https://github.com/valkey-io/valkey/pull/49
[#48]: https://github.com/valkey-io/valkey/pull/48
[#47]: https://github.com/valkey-io/valkey/pull/47
[#46]: https://github.com/valkey-io/valkey/pull/46
[#45]: https://github.com/valkey-io/valkey/pull/45
[#44]: https://github.com/valkey-io/valkey/pull/44
[#43]: https://github.com/valkey-io/valkey/pull/43
[#42]: https://github.com/valkey-io/valkey/pull/42
[#41]: https://github.com/valkey-io/valkey/pull/41
[#40]: https://github.com/valkey-io/valkey/pull/40
[#39]: https://github.com/valkey-io/valkey/pull/39
[#38]: https://github.com/valkey-io/valkey/pull/38
[#37]: https://github.com/valkey-io/valkey/pull/37
[#36]: https://github.com/valkey-io/valkey/pull/36
[#35]: https://github.com/valkey-io/valkey/pull/35
[#34]: https://github.com/valkey-io/valkey/pull/34
[#33]: https://github.com/valkey-io/valkey/pull/33
[#32]: https://github.com/valkey-io/valkey/pull/32
[#31]: https://github.com/valkey-io/valkey/pull/31
[#30]: https://github.com/valkey-io/valkey/pull/30
[#29]: https://github.com/valkey-io/valkey/pull/29
[#28]: https://github.com/valkey-io/valkey/pull/28
[#27]: https://github.com/valkey-io/valkey/pull/27
[#26]: https://github.com/valkey-io/valkey/pull/26
[#25]: https://github.com/valkey-io/valkey/pull/25
[#24]: https://github.com/valkey-io/valkey/pull/24
[#23]: https://github.com/valkey-io/valkey/pull/23
[#22]: https://github.com/valkey-io/valkey/pull/22
[#21]: https://github.com/valkey-io/valkey/pull/21
[#20]: https://github.com/valkey-io/valkey/pull/20
[#19]: https://github.com/valkey-io/valkey/pull/19
[#18]: https://github.com/valkey-io/valkey/pull/18
[#17]: https://github.com/valkey-io/valkey/pull/17
[#16]: https://github.com/valkey-io/valkey/pull/16
[#15]: https://github.com/valkey-io/valkey/pull/15
[#14]: https://github.com/valkey-io/valkey/pull/14
[#13]: https://github.com/valkey-io/valkey/pull/13
[#12]: https://github.com/valkey-io/valkey/pull/12
[#11]: https://github.com/valkey-io/valkey/pull/11
[#10]: https://github.com/valkey-io/valkey/pull/10
[#9]: https://github.com/valkey-io/valkey/pull/9
[#8]: https://github.com/valkey-io/valkey/pull/8
[#7]: https://github.com/valkey-io/valkey/pull/7
[#6]: https://github.com/valkey-io/valkey/pull/6
[#5]: https://github.com/valkey-io/valkey/pull/5
[#4]: https://github.com/valkey-io/valkey/pull/4
[#3]: https://github.com/valkey-io/valkey/pull/3
[#2]: https://github.com/valkey-io/valkey/pull/2
[#1]: https://github.com/valkey-io/valkey/pull/1

[Issue #784]: https://github.com/valkey-io/valkey/issues/784
[Issue #619]: https://github.com/valkey-io/valkey/issues/619
[Issue #719]: https://github.com/valkey-io/valkey/issues/719

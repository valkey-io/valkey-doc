
---
title: Upgrading Valkey

description: Step-by-step instructions for upgrading an existing Valkey instance with minimal downtime

---

# Upgrading Valkey

Valkey is designed to run as a long-running process. Many configuration options can be modified without restarting the server using the `CONFIG SET` command. However, some changes, such as upgrading the Valkey process to a newer version or modifying unsupported configuration parameters, require a restart.

You can minimise downtime during an upgrade by starting a new Valkey instance, synchronising it with the existing instance, and switching clients to the new instance.

## Upgrading a standalone Valkey instance

Follow these steps to upgrade a standalone Valkey instance with minimal downtime.

### 1. Prepare the new Valkey instance

Set up a new Valkey instance using the version you want to upgrade to.

You need either:
- A different server to run the new instance.
- A server with enough available RAM to run both the existing and new Valkey instances simultaneously.

If you are running both instances on the same server, configure the new instance to use a different port from the existing instance.

### 2. Configure the new instance as a replica

Configure the new Valkey instance to replicate from the existing instance using the `REPLICAOF` command:

```bash
valkey-cli -h <new-instance-host> -p <new-instance-port>
```

Then execute:

```text
REPLICAOF <old-primary-host> <old-primary-port>
```

The new instance will connect to the existing primary and begin synchronising its dataset.

### 3. Wait for initial synchronisation

Wait for the initial replication synchronisation to complete. Check the new instance's log file for replication progress.

You can also inspect the replication status:

```bash
valkey-cli -h <new-instance-host> -p <new-instance-port> INFO replication
```

Verify that `master_link_status` is `up` and `master_sync_in_progress` is `0`. These values indicate that the replication link is established and the initial synchronisation has completed.

### 4. Verify the dataset

Use the `INFO` command on both instances to compare their key counts.

```bash
valkey-cli -h <old-primary-host> -p <old-primary-port> INFO keyspace
```

```bash
valkey-cli -h <new-instance-host> -p <new-instance-port> INFO keyspace
```

Compare the key counts to check for obvious differences between the instances. Since replication is asynchronous, matching key counts alone do not guarantee that the replica has received all recent writes. Before switching clients, ensure that the replica has caught up with the primary. You can compare replication offsets using the `INFO replication` command on both instances.

### 5. Pause writes to the old primary

Before switching clients, pause write commands on the old primary:

```bash
valkey-cli -h <old-primary-host> -p <old-primary-port> CLIENT PAUSE <timeout-in-milliseconds> WRITE
```
The timeout is specified in milliseconds. During this period, write commands from clients are paused. Complete the promotion and client reconfiguration before the timeout expires, as clients are automatically unblocked when it expires.

### 6. Wait for the replica to catch up

Check the replication offsets using `INFO replication` on both instances.

Ensure that the replica has processed all the writes from the old primary before promoting it.

### 7. Promote the new instance to primary

Promote the new instance:

```bash
valkey-cli -h <new-instance-host> -p <new-instance-port> REPLICAOF NO ONE
```

Configure application clients to connect to the new primary.

After confirming that the new instance is serving client traffic correctly, safely shut down the old primary.

## Upgrading Valkey Sentinel or Cluster deployments

If you are using [Valkey Sentinel](sentinel.md) or [Valkey Cluster](cluster-tutorial.md), the simplest way to upgrade to newer versions is to upgrade one replica after the other. Then you can perform a manual failover to promote one of the upgraded replicas to primary, and finally promote the last replica.

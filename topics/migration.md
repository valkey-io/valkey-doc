
---
title: Migration from Redis to Valkey
description: How to migrate from Redis to Valkey
---

This is a migration guide from Redis open source versions to Valkey.
You will learn how to migrate a standalone Redis server instance and a Redis Cluster. 

This guide provides migration steps for Redis server and Valkey deployed in Docker; however, they should also apply for other deployments.
Refer to [install Valkey](installation.md) for installation options.

## Why to migrate to Valkey?

* Valkey is the vendor-neutral and open-source software
* Enhanced performance with multi-threading and dual-channel replication
* Improved memory efficiency by using one dictionary per slot in cluster mode and embedding keys in dictionaries. 

### Migration compatibility matrix

You can migrate a Redis server to Valkey.
Valkey is compatible with Redis OSS 7.2 and all earlier open source Redis versions.
Migrating from any open source Redis version to Valkey is effectively an upgrade.
Redis Community Edition (CE), versions 7.4 and later, are not open source and the data files are not compatible with Valkey.
It may be possible to migrate the data to Valkey from proprietary Redis versions and other Redis-like software, but it requires another method and is not covered by this document.

The following table provides migration options depending on the Redis version you run:

| Redis                 | Valkey |
|-----------------------|--------|
| OSS 2.x - 7.2.x       | 7.2.x  |
| OSS 2.x - 7.2.x       | 8.0    |
| CE 7.4                | n/a    |

## Migrate a standalone instance

To migrate a standalone Redis server to Valkey, you have the following options:

* [Physical migration](#physical-migration) by copying the most recent on-disk snapshot from the Redis server to Valkey and starting Valkey server with it
* [Setting up replication](#repication) between Redis and Valkey 
* [Migrating specific keys](#migrate-specific-keys) 

The example migration steps are provided for Redis 7.2.5 and Valkey version 7.2.6. 

Note that Redis and Valkey Docker containers are considered stand-alone servers, if they are not part of a cluster.

### Physical migration

This is the easiest and fastest migration method. You make a fresh snapshot of your Redis instance and copy it over to Valkey. Valkey reads the data from the snapshot on startup and restores its contents into memory. The tradeoffs for this method are:

* The downtime to shutdown Redis and wait for Valkey to load the data. 
* Potential risk of data loss on instances with heavy writes. To prevent it, you must disconnect all active connections before starting the migration.

To perform a physical migration:

1. Disconnect all active connections to the Redis instance.

2. In your Redis container, connect to `redis-cli` and check the number of keys, using the `INFO KEYSPACE` command. This will be used later to verify that the entire database has been successfully migrated. In this example, `keys=6286` indicates that there are 6.286 keys in the database.

      ```
      $ redis-cli -h 127.0.0.1 -p 6379
      redis 127.0.0.1:6379> INFO KEYSPACE
      # Keyspace
      db0:keys=6286,expires=0,avg_ttl=0
      ```
    
3. Check the configuration for the directory (`dir`) where Redis stores its database files and the name of the database file (`dbfilename`). In this example, Redis saves the backup into the `/data/dump.rdb` file

	> NOTE: If your Redis Docker container `/data` directory is mounted to a directory on your host, the RDB file is also written to that host directory.

    ```
    redis 127.0.0.1:6379> CONFIG GET dir dbfilename
    1) "dir"
    2) "/data"
    3) "dbfilename"
    4) "dump.rdb"
    ```
4. Create the backup file. You can either use the `redis-cli` [SAVE](https://redis.io/docs/latest/commands/save/) command or the [BGSAVE](https://redis.io/docs/latest/commands/bgsave/) command to create the backup file. The `SAVE` command performs a synchronous save, blocking all the other clients. However, the `BGSAVE` does the save in the background, forking a child to save the DB, allowing the parent to continue serving the clients. 

	> NOTE: BGSAVE is usually used for production environments.

	- Using `BGSAVE`
	
		a.  Check the timestamp of the last save operation, using the [LASTSAVE](https://redis.io/docs/latest/commands/lastsave/) comamnd.

      ```
      redis 127.0.0.1:6379> LASTSAVE
      (integer) 1724764878
      ```

		b. Start the save operation.

	   ```
      redis 127.0.0.1:6379> BGSAVE
      Background saving started
      ```

		c. Rerun `LASTSAVE` periodically until the timestamp changes, indicating the backup is complete.

	- Using `SAVE`

		Start the save operation. 

      ```
		redis 127.0.0.1:6379> SAVE
		OK
      ```

5. Exit  `redis-cli` by pressing `CTRL-D` or typing `exit`.
6. Create a directory on your host to which you will mount the `/data` directory of the Valkey container.
7. Copy the RDB file from Redis to Valkey, using one of the following:

	- Redis container mounted to host directory: 

        Copy the RDB file from the host directory mounted to the Redis container to the host directory being mounted to the Valkey container.


	- Redis container not mounted to host directory:
	
		Use `docker cp` to copy the RDB file from within the Redis container to the host directory that will be mounted to your Valkey container.

		> NOTE: You may also want to copy the RDB file to a second location as a backup.

      ```
	   docker cp <Redis_container_name>:/<dir>/<dbfilename> <path/on/host>:<dir>/<dbfilename>
      ```

8. Stop the Redis server.
9. Start Valkey:

   > NOTE: If you enabled AOF in your Valkey configuration, disable it on the first start. Otherwise, the copied RDB file will not be imported into Valkey.

   Run the following command:

   ```
	docker run -d --name <Valkey_container_name> -v <path/on/host>:<path/in/Valkey/container> <image_name>
   
   ```
   In this example, the container is named, `somevalkey` and the image name is `valkey/valkey`. It is mounting whatever is set as the directory path on the host to the Docker container `/data` directory.    

   ```
   $ docker run -d --name somevalkey -v <path/on/host>:/data valkey/valkey
   ```

10. To verify that the data has been successfully migrated, determine the number of keys in the Valkey database. If the migration is successful, then the number of keys in the Valkey database match the number of keys in the Redis database that you obtained in step 2:

      ```
      $ docker exec -it somevalkey valkey-cli
      valkey 127.0.0.1:6379> INFO KEYSPACE
      # Keyspace
      db0:keys=6286,expires=0,avg_ttl=0
      ```

11. To exit `valkey-cli`, press `Ctrl-D` or type `exit`.

### Replication

To minimize the downtime during migration, you can use replication. Both Redis and Valkey allow replaying data on another server to handle the workload.

In this scenario we will configure Valkey to be the replica of Redis. For illustrative purposes, both Redis and Valkey are running in separate Docker containers connected to the same network. 

1. Retrieve the IP address of the Redis container. Replace the `myredis` placeholder with the name of your container. In this example, `172.17.0.2` is returned as the IP address of the `myredis` container.

    ```
    $ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myredis
    172.17.0.2
    ```
2. Determine the port on which your Redis container is exposed. Note that for clarity, not all of the fields are shown in the response. In this example, the `myredis` container is exposed on port `6379`.

   ```
   docker container ls
   CONTAINER ID   ...     PORTS      NAMES
   bffc575f261a   ...     6379/tcp   myvalkey
   ab18318ce820   ...     6379/tcp   myredis
   ```
   
3. Connect to your Valkey container and start the `valkey-cli` to configure replication using the [REPLICAOF](https://valkey.io/commands/replicaof/) command. In this example, the Redis IP address is `172.17.0.2` and the port is `6379`. Replace with the IP address and port of your Redis container obtained in steps 1 and 2.

   ```
   docker exec -it myvalkey valkey-cli
   valkey 127.0.0.1:6379> REPLICAOF 172.17.0.2 6379
   OK
   ```
   
4. Check the replication status in Valkey using the `INFO REPLICATION` command. If `master_link_status:up` is present, then the Redis and Valkey servers are synchronized. [INFO Command](https://valkey.io/commands/info/) desribes the different output fields.

    ```
    valkey 127.0.0.1:6379> INFO REPLICATION
    # Replication
    role:slave
    master_host:172.17.0.2
    master_port:6379
    master_link_status:up
    master_last_io_seconds_ago:4
    master_sync_in_progress:0
    ....
    ```

5. Once Redis and Valkey are synchronized, verify that your applications connect to Valkey and shut down your Redis instance. 

   You can shut down Redis in one of the following ways:

   * Using `redis-cli`:

      ```
      $ redis-cli shutdown
      ```

   * If Redis was started directly in the foreground (using redis-server), you can simply stop it by pressing `Ctrl-C` in the terminal where it is running.

6. In your Valkey container, stop the Valkey replication using the `REPLICAOF` command with `NO ONE` as the options:
 
    ```
    valkey 127.0.0.1:6379> REPLICAOF NO ONE
    OK
    ```
7. You can verify that replication has stopped by running the `valkey-cli` command, `INFO REPLICATION`. If you see `role:master` and `connected_slaves:0`, then the Valkey container is now the master and is no longer connected to the Redis server. [INFO Command](https://valkey.io/commands/info/) desribes the different output fields.

   ```
   127.0.0.1:6379> INFO REPLICATION
   # Replication
   role:master
   connected_slaves:0
   master_failover_state:no-failover
   master_replid:8d48c4667129cdb5933f9a12a1d5e6a24899602b
   master_replid2:602b7046ada6d2d6f0e89657e646d5932cc42791
   master_repl_offset:1336
   second_repl_offset:1337
   repl_backlog_active:1
   repl_backlog_size:1048576
   repl_backlog_first_byte_offset:1
   repl_backlog_histlen:1336
   ```

> NOTE: If not for backward compatibility, the Valkey project no longer uses the words "master" and "slave". Unfortunately in this command these words are part of the protocol, so we’ll be able to remove such occurrences only when this API is naturally deprecated.

### Migrate specific keys

Both physical migration and replication migrate the entire keyspace over to Valkey. 

There may be cases when you need to migrate only a specific set of critical keys. 
The `redis-cli` command, [MIGRATE](https://redis.io/docs/latest/commands/migrate/) is used to migrate one or more keys.

Requirements for this example:

- The Redis and Valkey Docker containers are on the same network and can communicate with each other.

- The Redis and Valkey containers are running without authentication.

Perform the following steps:

1. Determine the keys you wish to migrate. In this example, the `message` and  `mydata` keys are being migrated from the `myredis` container, and the `redis-cli` is used to view their current values.
   
    ```
    $ docker exec -it myredis redis-cli
    redis 127.0.0.1:6379> GET message
    "Hello Valkey"
    redis 127.0.0.1:6379> HGETALL  mydata
    1) "name"
    2) "Alice"
    3) "age"
    4) "33"
    5) "country"
    6) "Brazil"
    7) "favorite food"
    8) "beans"
    ```

2. Retrieve the IP address of your Valkey container. Replace `myvalkey` with the name of your Valkey container.
    
    ```
    $ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myvalkey
    172.21.0.3
    ```

3. Start the `valkey-cli` in your Valkey container and get the database number using the `INFO KEYSPACE` command. In this example, the database number is `0` (db0).
   
   ```
   valkey 127.0.0.1:6379> INFO KEYSPACE
   # Keyspace
   db0:keys=3,expires=0,avg_ttl=0
   ```
    > NOTE: If you haven't migrated or added any data to your Valkey database, then the `INFO KEYSPACE` command will not return any database number. You can use `0` for the `MIGRATE` command in step 4.
   
4. From the Redis server, run the `MIGRATE` command:
     ```
     MIGRATE <Valkey_IP> <Valkey_port> <key | ""> <Valkey-db-number> <timeout> [COPY] [REPLACE] [AUTH password | AUTH2 username password] [KEYS key [key ...]]
     ```
    For example, to migrate the `message` and `mydata` keys to the Valkey instance with the IP address 172.21.0.3 and port 6379, the command would look similar to:

    ```
    redis 127.0.0.1:6379> MIGRATE 172.21.0.3 6379 "" 0 10 COPY REPLACE KEYS message mydata
    ```
    
   where:
   - `""` = Indicates that we are migrating multiple keys. You would use `key` if you were only migrating a single key.
   - `0` = The database number.
   - `10`= The maximum idle time, in milliseconds, allowed when communicating with the destination server.
   - `COPY` = Do not remove the key from the Redis database.
   - `REPLACE` = Replace existing key on the Valkey database.
   - `KEYS` = We are migrating multiple keys and it is followed by the key names.

    

7. Exit `redis-cli` by pressing `Ctrl-D` or typing `exit`.

4. Connect to Valkey and check the migrated keys. replace `myvalkey` with the name of your Valkey container.
   
    ```
    $ docker exec -it myvalkey valkey-cli
    valkey 127.0.0.1:6379> GET message
    "Hello Valkey"
    valkey 127.0.0.1:6379> HGETALL mydata
    1) "name"
    2) "Alice"
    3) "age"
    4) "33"
    5) "country"
    6) "Brazil"
    7) "favorite food"
    8) "beans"
    ```

## Migrate a Cluster

This section demonstrates how to migrate a cluster. The first step is to add the required number of Valkey nodes to the existing cluster as replicas. Once the new Valkey nodes replicate the data, one Valkey replica is promoted to be a new primary for each Redis primary. After the migration, the Redis nodes are removed from the cluster.

> NOTE: You can also use data migration tools such as [RIOT](https://redis.github.io/riot/#_introduction), [RedisShake](https://github.com/tair-opensource/RedisShake), and [Redis-Migrate-Tool](https://github.com/vipshop/redis-migrate-tool) but that is beyond the scope of this document.

Requirements for this exmaple:

- The Redis and Valkey cluster nodes are on the same network and can communicate with each other.

For this scenario, there is a Redis Cluster consisting of 3 primary and 3 replica nodes up and running. Refer to [Create a Redis cluster](https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/#create-a-redis-cluster) documentation for steps how to create a Cluster. 

To perform the migraiton:

1.  Use the `redis-cli` on one of the cluster nodes to check the current state of the cluster and to ensure all nodes are connected and active. In this cluster, there are three primary (master) and three replica (slave) nodes.

    ```
    $ redis-cli -h 127.0.0.1 -p 6379 -c cluster nodes
    70beedebe43e422b275ee1a7bac0d3819dedca98 172.22.0.3:6379@16379 master - 0 1725450849000 1 connected 0-5460
    8bbe836c59644f7395bbab09c6f8b36bc277e902 172.22.0.5:6379@16379 slave 58061fb2836bdb2f5a0973e1ccfd74a66166f329 0 1725450849510 3 connected
    65061b94da5b481dc35c2df7dae13c233d4b3ad2 172.22.0.4:6379@16379 master - 0 1725450848000 2 connected 5461-10922
    a242941d0e3edad27a954bc14ac3a3413f3040aa 172.22.0.7:6379@16379 slave 65061b94da5b481dc35c2df7dae13c233d4b3ad2 0 1725450849000 2 connected
    3499854656f085ebb77b5b921389a91b7ae9d703 172.22.0.6:6379@16379 slave 70beedebe43e422b275ee1a7bac0d3819dedca98 0 1725450849829 1 connected
    58061fb2836bdb2f5a0973e1ccfd74a66166f329 172.22.0.2:6379@16379 myself,master - 0 1725450846000 3 connected 10923-16383
    ```

2. Create a valkey.conf configuration file and specify the following parameters. Note that this configuration file enables clustering. [Valkey configuration file example](https://raw.githubusercontent.com/valkey-io/valkey/7.2/valkey.conf) provides a description of the various configuration arguments:

    ```
    # valkey.conf file
    port 6379
    cluster-enabled yes
    cluster-config-file nodes.conf
    cluster-node-timeout 5000
    appendonly yes
    ```

3. Start a Valkey instance with your custom configuration file. The following command starts Valkey in Docker: 

    ```
    $ docker run  -d -v myvalkey/conf:/usr/local/etc/valkey --name valkey-1 --net mynetwork valkey/valkey valkey-server /usr/local/etc/valkey/valkey.conf
    ```

   where:
   * `myvalkey/conf` is a local directory containing your `valkey.conf` configuration file that is being mapped to the `/usr/local/etc/valkey` directory within the Docker Valkey container.
   * `valkey-1` is the name of your container
   * `mynetwork` is the name of the network where Redis cluster is running.
   * `valkey/valkey` is the name of the Valkey image

4. Retrieve the IP address of the Valkey instance; replacing `valkey-1` with the name of your container.

    ```
    $ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' valkey-1    
    ```

5. Add your new Valkey node to the Redis Cluster as a replica. Replace placeholders in angle brackets (`<>`) with your values:

    ``` 
    $ docker exec -it <redis-1> bash
    $ redis-cli --cluster add-node <valkey-node-IP>:6379 <existing-node-IP>:6379 --cluster-replica
    ```

6. Check the cluster status. The output of the cluster nodes command is described in [CLUSTER NODES](https://redis.io/docs/latest/commands/cluster-nodes/).

    ```
    $ redis-cli -c cluster nodes
    ```

    In the output you will see the newly added node as a replica (slave). For example, we have added a Valkey node with the IP address `172.22.0.8:6379`. The cluster nodes list now includes a new entry as follows:

    ```
    a98d5bac59672597b8509f24970e413002f896b6 172.22.0.8:6379@16379 slave 58061fb2836bdb2f5a0973e1ccfd74a66166f329 0 1725451086000 3 connected
    ```
    
7. Verify that the your newly added Valkey node is recognized as a replica by running the `INFO REPLICATION` command. The output displays information about the node's primary.

8. Start the `valkey-cli` in your new Valkey container and enter the following command to promote it to be primary. [Cluster Failover](https://valkey.io/commands/cluster-failover/) provides additional information.

   ```
   docker exec -it <valkey_container_name> valkey-cli
   valkey 127.0.0.1:6379> cluster failover
   OK
   ```

9. Use the `cluster nodes` command to display the cluster state and verify that your new Valkey node is now a new primary.

10. Repeat steps 3-9 to add 2 more Valkey nodes and replace the Redis primary nodes. 
11. Repeat steps 3-7 to add 3 Valkey replica nodes. 

    To add a replica to a specific primary, do the following:

    a. Filter primary nodes. Connect to any node in the Cluster and run the following command:

       ```
       $ docker exec -it valkey-1 bash
       $ valkey-cli -c cluster nodes | grep master
       70beedebe43e422b275ee1a7bac0d3819dedca98 172.22.0.3:6379@16379 master - 0 1725451135799 1 connected 0-5460
       65061b94da5b481dc35c2df7dae13c233d4b3ad2 172.22.0.4:6379@16379 master - 0 1725451136000 2 connected 5461-10922
       58061fb2836bdb2f5a0973e1ccfd74a66166f329 172.22.0.2:6379@16379 myself,master - 0 1725451136000 3 connected 10923-16383
       ```
    > NOTE: The node ID is the 40-character globally unique string that is generated when the node is created. In this example, `70beedebe43e422b275ee1a7bac0d3819dedca98` is the ID of the primary (master) node with the IP address `172.22.0.3:6379`. The ID of a node is required when adding a new Valkey replica to a specific primary in step b.
    
    b. Add a new node to a specific primary:

      ```
      $ valkey-cli --cluster add-node 172.22.0.10:6379 172.22.0.2:6379 --cluster-replica --cluster-master-id <node-ID>
      ```
    
12. Remove Redis nodes:

     ```
     redis-cli --cluster del-node 127.0.0.1:6379 `<node-id>`
     ```

     The first argument is just a random node in the cluster, the second argument is the ID of the node you want to remove.

> NOTE: If not for backward compatibility, the Valkey project no longer uses the words "master" and "slave". Unfortunately in the given commands these words are part of the protocol, so we'll be able to remove such occurrences only when this API is naturally deprecated.

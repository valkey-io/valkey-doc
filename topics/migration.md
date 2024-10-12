---
title: Migration from Redis to Valkey
linkTitle: Migration
description: How to migrate from Redis to Valkey
---

This is a migration guide from Redis Community Edition to Valkey. 
You will learn how to migrate a standalone Redis server instance and a Redis Cluster. 

This guide provides migration steps for Redis server and Valkey deployed in Docker; however, they should also apply for on-premises deployments. 
Refer to [install Valkey](installation.md) for installation options.

## Why to migrate to Valkey?

* Valkey is the vendor-neutral and open-source software
* Enhanced performance with multi-threading and dual-channel replication
* Improved memory efficiency by using one dictionary per slot in cluster mode and embedding keys in dictionaries. 

### Migration compatibility matrix

You can migrate Redis server to Valkey. 
The following table provides migration options depending on the Redis version you run:

| Redis | Valkey |
|-------|--------|
| 6.x   | 7.2.x  |
| 7.2.x | 7.2.x  |
| 7.2.x | 8.0.x  |
| 7.4   | n/a    |

## Migrate a standalone instance

To migrate a standalone Redis server to Valkey, you have the following options:

* [Physical migration](#physical-migration) by copying the most recent on-disk snapshot from the Redis server to Valkey and starting Valkey server with it
* [Setting up replication](#repication) between Redis and Valkey 
* [Migrating specific keys](#migrate-specific-keys) 

The example migration steps are provided for Redis 7.2.5 and Valkey version 7.2.6. 

### Physical migration

This is the easiest and fastest migration method. You make a fresh snapshot of your Redis instance and copy it over to Valkey. Valkey reads the data from the snapshot on startup and restores its contents into memory. The tradeoffs for this method are:

* The downtime to shutdown Redis and wait for Valkey to load the data. 
* Potential risk of data loss on instances with heavy writes. To prevent it, you must disconnect all active connections before the migration start.

1. Disconnect all active connections to the Redis instance.

2. Make a backup of your Redis instance. 

   a. Connect to Redis and check the number of keys:

      ```
      $ redis-cli -h 127.0.0.1 -p 6379
      redis 127.0.0.1:6379> INFO KEYSPACE
      # Keyspace
      db0:keys=6286,expires=0,avg_ttl=0
      ```
    
   b. Check the configuration for the directory (`dir`) where Redis stores its database files and the name of the database file (`dbfilename`):
       ```
       redis 127.0.0.1:6379> CONFIG GET dir dbfilename
       1) "dir"
       2) "/data"
       3) "dbfilename"
       4) "dump.rdb"
       ```
    
   c. Check the timestamp of the last save operation

      ```
      redis 127.0.0.1:6379> LASTSAVE
      (integer) 1724764878
      ```

   d. Start a backup

      ```
      redis 127.0.0.1:6379> BGSAVE
      Background saving started
      ```

   e. Check if the backup succeeded by running `LASTSAVE` periodically. The backup ended when the timestamp changes.

   f. Exit the `redis-cli` by pressing `Ctrl-D`. 

2. Stop the Redis server. 
3. Copy the RDB file to the Valkey's data directory and start Valkey. 

   >NOTE: If you enabled AOF in your Valkey configuration, disable it on the first start. Otherwise, the copied RDB file will not be imported into Valkey.

   For Docker deployments, copy the RDB file to your host and start a Valkey container mounting this file to the container's data directory. Replace the `<container-name>` and `<path/on/host>` placeholders with your values.

   ```
   $ docker cp <container-name>:/data/dump.rdb <path/on/host>
   ```

   Start Valkey:

   ```
   $ docker run -d --name somevalkey -v <path/on/host>:/data valkey/valkey
   ```

4. Check the keyspace on Valkey to verify that the data is migrated:

   ```
   $ docker exec -it somevalkey valkey-cli
   valkey 127.0.0.1:6379> INFO KEYSPACE
   # Keyspace
   db0:keys=6286,expires=0,avg_ttl=0
   ```

5. To exit `valkey-cli`, press `Ctrl-D`.

### Replication

To minimize the downtime during migration, you can use replication. Both Redis and Valkey allow replaying data on another server to handle the workload.

In this scenario we will configure Valkey to be the replica of Redis. For illustrative purposes, both Redis and Valkey are running in separate Docker containers connected to the same network. 

1. Retrieve the IP address of Redis container. Replace the `myredis` placeholder with the name of your container.

    ```
    $ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myredis
    ```

2. Connect to Valkey and configure replication. Replace the IP address and port with the ones of your Redis container, retrieved at the previous step:

    ```
    $ docker exec -it myvalkey valkey-cli
    valkey 127.0.0.1:6379> REPLICAOF 172.17.0.2 6379
    ```

3. Check the replication status in Valkey. 

    ```
    valkey 127.0.0.1:6379> INFO REPLICATION
    # Replication
    role:slave
    master_host:172.21.0.4
    master_port:6379
    master_link_status:up
    master_last_io_seconds_ago:-1
    master_sync_in_progress:0
    ....
    ```

4. Now that the two are in sync, check that your applications connect to Valkey and shut down your Redis instance. 

   You can shut down Redis in one of the following ways:

   * Using `redis-cli`:

      ```
      $ redis-cli shutdown
      ```

   * If Redis was started directly in the foreground (using redis-server), you can simply stop it by pressing `Ctrl-C` in the terminal where it is running.

5. Halt Valkey replication:
 
    ```
    valkey 127.0.0.1:6379> REPLICAOF NO ONE
    OK
    ```

> NOTE: If not for backward compatibility, the Valkey project no longer uses the words "master" and "slave". Unfortunately in this command these words are part of the protocol, so we’ll be able to remove such occurrences only when this API will be naturally deprecated.

### Migrate specific keys

Both physical migration and replication migrate the entire keyspace over to Valkey. 

There may be cases when you need to migrate only specific set of critical keys. 
To do that, use the `MIGRATE` command.

For the following steps, we assume that both Redis and Valkey Docker containers are connected to the same network and can communicate with each other. 
For simplicity, we are running both instances without authentication.

1. Connect to Redis and set the keys you wish to migrate over. Replace `myredis` with the name of your container. 
   For example, let's use the keys `message` and  `mydata`.

    ```
    $ docker exec -it myredis redis-cli
    redis 127.0.0.1:6379> SET message "Hello Valkey!"
    redis 127.0.0.1:6379> HSET  mydata name Alice age 33 country Brazil "favorite food" beans
    (integer) 4
    ```

2. Retrieve the IP address of your Valkey container
    
    ```
    $ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myvalkey
    ```

3. From the Redis server, run the `MIGRATE` command and specify the following information:

     * The IP address and post of the Valkey instance
     * Authentication password. For no authentication, set the empty value 
     * The database number. To get the number, run the `INFO keyspace` command
     * Timeout for the operation, in milliseconds
     * The `COPY` option ensures that the key is not removed from the source instance after the migration.
     * The `REPLACE` option allows the key on the destination instance to be replaced if it already exists.
     * `KEYS`. Specify the key(s) to migrate

     For example, to migrate the `message` and `mydata` keys to the Valkey instance with the IP address 172.21.0.3, the command looks as follows:

    ```
    redis 127.0.0.1:6379> MIGRATE 172.21.0.3 6379 "" 0 10 COPY REPLACE KEYS message mydata
    ```

4. Exit `redis-cli` by pressing `Ctrl-D`

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

To migrate a Redis Cluster to Valkey, you have the following options:

* Add the required number of Valkey nodes to the existing cluster as replicas, wait till they replicate the data and promote one Valkey replica for each Redis primary to be a new primary. After the migration, you can remove Redis nodes.
* Use data migration tools like [RIOT](https://redis.github.io/riot/#_introduction), [RedisShake](https://github.com/tair-opensource/RedisShake), [Redis-Migrate-Tool](https://github.com/vipshop/redis-migrate-tool) and the like.

This section demonstrates migration via adding Valkey nodes and replacing Redis ones.

For this scenario, we assume that you have Redis Cluster consisting of 3 primary and 3 replica nodes up and running. Refer to [Create a Redis cluster](https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/#create-a-redis-cluster) documentation for steps how to create a Cluster. Also, make sure that both Redis Cluster nodes and Valkey nodes are connected to the same network and can communicate with each other.

1. Check the cluster state

    ```
    $ redis-cli -h 127.0.0.1 -p 6379 -c cluster nodes
    70beedebe43e422b275ee1a7bac0d3819dedca98 172.22.0.3:6379@16379 master - 0 1725450849000 1 connected 0-5460
    8bbe836c59644f7395bbab09c6f8b36bc277e902 172.22.0.5:6379@16379 slave 58061fb2836bdb2f5a0973e1ccfd74a66166f329 0 1725450849510 3 connected
    65061b94da5b481dc35c2df7dae13c233d4b3ad2 172.22.0.4:6379@16379 master - 0 1725450848000 2 connected 5461-10922
    a242941d0e3edad27a954bc14ac3a3413f3040aa 172.22.0.7:6379@16379 slave 65061b94da5b481dc35c2df7dae13c233d4b3ad2 0 1725450849000 2 connected
    3499854656f085ebb77b5b921389a91b7ae9d703 172.22.0.6:6379@16379 slave 70beedebe43e422b275ee1a7bac0d3819dedca98 0 1725450849829 1 connected
    58061fb2836bdb2f5a0973e1ccfd74a66166f329 172.22.0.2:6379@16379 myself,master - 0 1725450846000 3 connected 10923-16383
    ```

2. Enable cluster mode in Valkey configuration. Create a `valkey.conf` configuration file and specify the following directives as the starting point:

    ```
    # valkey.conf file
    port 6379
    cluster-enabled yes
    cluster-config-file nodes.conf
    cluster-node-timeout 5000
    appendonly yes
    ```

    Read more about Valkey configuration parameters in [the self documented Valkey.conf for 7.2](https://raw.githubusercontent.com/valkey-io/valkey/7.2/valkey.conf)

3. Start a Valkey instance with your custom configuration file. The following command starts Valkey in Docker: 

    ```
    $ docker run  -d -v myvalkey/conf:/usr/local/etc/valkey --name valkey-1 --net mynetwork valkey/valkey valkey-server /usr/local/etc/valkey/valkey.conf
    ```

    where `myvalkey/conf` is a local directory containing your `valkey.conf` configuration file, `valkey-1` is the name of your container and `mynetwork` is the name of the network where Redis cluster is running.

4. Retrieve the IP address of the Valkey instance; replace `valkey-1` with the name of your container.

    ```
    $ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' valkey-1
    ```

5. Add a Valkey node to the Redis Cluster as a replica. Replace placeholders in angle brackets (`<>`) with your values:

    ``` 
    $ docker exec -it <redis-1> bash
    $ redis-cli --cluster add-node <valkey-node-IP>:6379 <existing-node-IP>:6379 --cluster-replica
    ```

6. Check the cluster status

    ```
    $ redis-cli -c cluster nodes
    ```

    In the output you will see the newly added nodes. For example, we have added a Valkey node with the IP address `172.22.0.8:6379`. The cluster nodes list now includes a new entry as follows:

    ```
    a98d5bac59672597b8509f24970e413002f896b6 172.22.0.8:6379@16379 slave 58061fb2836bdb2f5a0973e1ccfd74a66166f329 0 1725451086000 3 connected
    ``` 

7. Check that the newly added node is recognized as a replica by running the `INFO REPLICATION` command. The output shows the information about the node's primary.

8. Promote it to be a new primary. Run the following command **from the node you wish to promote**:

   ```
   valkey 127.0.0.1:6379> cluster failover
   OK
   ```

9. Check the cluster state. You should now see the previous replica to be a new primary.

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

    b. Add a new node to a specific primary:

      ```
      $ valkey-cli --cluster add-node 172.22.0.10:6379 172.22.0.2:6379 --cluster-replica --cluster-master-id <node-ID>
      ```
    
12. Remove Redis nodes:

     ```
     redis-cli --cluster del-node 127.0.0.1:6379 `<node-id>`
     ```

     The first argument is just a random node in the cluster, the second argument is the ID of the node you want to remove.

> NOTE: If not for backward compatibility, the Valkey project no longer uses the words "master" and "slave". Unfortunately in the given commands these words are part of the protocol, so we’ll be able to remove such occurrences only when this API will be naturally deprecated.


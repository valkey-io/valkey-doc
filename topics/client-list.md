---
title: "Client list"
description: Overview of Valkey clients and features
---

Selecting the right client is a complex task, given that there are over 200 clients compatible with Valkey across different programming languages. This document offers an overview of recommended Valkey clients for various programming languages. To be included in this list, a client must support a mandatory set of features, such as TLS support and cluster mode. Additionally, a table of advanced features supported by the respective clients is provided, highlighting the unique advantages of one client over another.

Mandatory Features Overview
----
1. **Cluster Support** - The ability to operate in a clustered environment, where the data is distributed across multiple shards. Cluster support is essential for applications that require high scalability.

2. **TLS/SSL Support** - The capability to establish secure connections using TLS/SSL, which encrypts the data transmitted between the client and the server. This is a critical feature for applications that require data privacy and protection against eavesdropping.

Advanced Features Overview
-----

1. **Read from Replica** - The ability to read data from a replica node, which can be useful for load balancing and reducing the load on the primary node. This feature is particularly important in read-heavy applications.

2. **Smart Backoff to Prevent Connection Storm** - A strategy used to prevent connection storms by progressively updating the wait time between retries when attempting to reconnect to a Valkey server. This helps to reduce the load on the server during topology updates, periods of high demand or network instability.

3. **Valkey Version Compatibility** - Indicates which versions of Valkey the client is compatible with. This is crucial for ensuring that the client can leverage the latest features and improvements in the Valkey server.

4. **PubSub State Restoration** - The ability to restore the state of Pub/Sub (publish/subscribe) channels after a client reconnects. This feature ensures that clients can continue receiving messages after disconnections or topology updates such as adding or removing shards, for both legacy Pub/Sub and sharded Pub/Sub. The client will automatically resubscribe the connections to the new node. The advantage is that the application code is simplified, and doesn’t have to take care of resubscribing to new nodes during reconnects.

5. **Cluster Scan** - This feature ensures that the user experience and guarantees for scanning a cluster are identical to those for scanning a single node. The SCAN function operates as a cursor-based iterator. With each command, the server provides an updated cursor, which must be used as the cursor argument in subsequent calls. A complete iteration with SCAN retrieves all elements present in the collection from start to finish. If an element exists in the collection at the beginning and remains until the end of the iteration, SCAN will return it. Conversely, any element removed before the iteration begins and not re-added during the process will not be returned by SCAN. A client supporting this feature ensures the scan iterator remains valid even during failovers or cluster scaling (in or out) during the SCAN operation. 

6. **Latency-Based Read from Replica** - This feature enables reading data from the nearest replica, i.e., the replica that offers the best latency. It supports complex deployments where replicas are distributed across various distances, including different geographical regions, to ensure data is read from the closest replica, thereby minimizing latency.
   
7. **AZ-Based Read from Replica** - This feature enables reading data from replicas within the same Availability Zone (AZ). When running Valkey in a cloud environment across multiple AZs, it is preferable to keep traffic localized within an AZ to reduce costs and latency. By reading from replicas in the same AZ as the client, you can optimize performance and minimize cross-AZ data transfer charges. For more detailed information about this feature and its implementation, please refer to the following link: https://github.com/valkey-io/valkey/pull/700

8. **Client Side Caching** - Valkey client-side caching is a feature that allows clients to cache the results of Valkey queries on the client-side, reducing the need for frequent communication with the Valkey server. This can significantly improve application performance by lowering latency, reducing the network usage and cost and reducing the load on the Valkey server. 
   
9. **`CLIENT CAPA redirect` Support** - The `CLIENT CAPA redirect` feature was introduced in Valkey 8 to facilitate seamless upgrades without causing errors in standalone mode. When enabled, this feature allows the replica to redirect data access commands (both read and write operations) to the primary instance. This ensures uninterrupted service during the upgrade process. For more detailed information about this feature, please refer to the following link: https://github.com/valkey-io/valkey/pull/325

10. **Persistent Connection Pool** - This feature enables the Valkey client to maintain a pool of persistent connections to the Valkey server, improving performance and reducing overhead. Instead of establishing a new connection for each request, the client can reuse existing connections from the pool, minimizing the time and resources required for connection setup.

Table of Contents
----
- [Table of Contents](#table-of-contents)
- [Python](#python)
- [JavaScript/Node.js](#javascriptnodejs)
- [Java](#java)
- [Go](#go)
- [PHP](#php)
  

Python
-----
- **valkey-glide**
  - GitHub: [valkey-glide](https://github.com/valkey-io/valkey-glide/tree/main/python)
  - Installation: `pip install valkey-glide`
  - Description: Valkey GLIDE is designed for reliability, optimized performance, and high-availability, for Valkey and Redis OSS based applications. GLIDE is a multi language client library, written in Rust with programming language bindings, such as Java, node.js and Python.

- **valkey-py**
  - GitHub: [valkey-py](https://github.com/valkey-io/valkey-py)
  - Installation: `pip install valkey`
  - Description: The Python interface to the Valkey key-value store.


JavaScript/Node.js
----
- **valkey-glide**
  - GitHub: [valkey-glide](https://github.com/valkey-io/valkey-glide/tree/main/node)
  - Installation: `npm install valkey-glide`
  - Description: Valkey GLIDE is designed for reliability, optimized performance, and high-availability, for Valkey and Redis OSS based applications. GLIDE is a multi language client library, written in Rust with programming language bindings, such as Java, node.js and Python.

- **iovalkey**
  - GitHub: [iovalkey](https://github.com/valkey-io/iovalkey)
  - Installation: `npm install iovalkey`
  - Description: A robust, performance-focused and full-featured Redis client for Node.js. This is a friendly fork of ioredis after this commit.

Java
----

- **valkey-glide**
  - GitHub: [valkey-glide](https://github.com/valkey-io/valkey-glide/tree/main/java)
  - Installation:

    Maven - 
    ```
    <dependency>
        <groupId>io.valkey</groupId>
        <artifactId>valkey-glide</artifactId>
        <version>1.2.0</version>
    </dependency>
    ```
    Gradle - 
    `implementation 'io.valkey:valkey-glide:1.2.0'`


  - Description: Valkey GLIDE is designed for reliability, optimized performance, and high-availability, for Valkey and Redis OSS based applications. GLIDE is a multi language client library, written in Rust with programming language bindings, such as Java, node.js and Python.

- **Valkey-Java**
  - GitHub: [valkey-java](https://github.com/valkey-io/valkey-java)
  - Installation: 
  
    Maven - 
    ```
    <dependency>
        <groupId>io.valkey</groupId>
        <artifactId>valkey-java</artifactId>
        <version>5.3.0</version>
    </dependency>
    ```
    Gradle - 
    `implementation 'io.valkey:valkey-java:5.3.0'`
  - Description: valkey-java is Valkey's Java client, dedicated to maintaining simplicity and high performance.


Go
-----
- **valkey-go**
  - GitHub: [go-valkey-go](https://github.com/valkey-io/valkey-go)
  - Installation: `go get github.com/valkey-io/valkey-go`
  - Description: A fast Golang Valkey client that does auto pipelining and supports server-assisted client-side caching.


PHP
----
- **Predis**
  - GitHub: [Predis](https://github.com/predis/predis)
  - Installation: `composer require predis/predis`
  - Description: A flexible and feature-rich Valkey client for PHP.

- **phpredis**
  - GitHub: [phpredis](https://github.com/phpredis/phpredis)
  - Installation: Install via PECL or compile from source
  - Description: A PHP extension for Redis, offering high performance and a native API.

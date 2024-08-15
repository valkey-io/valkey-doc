---
# Valkey Clients

Selecting the right client is a complex task, given that there are over 200 clients compatible with Valkey across different programming languages. This document offers an overview of recommended Valkey clients for various programming languages. To be included in this list, a client must support a mandatory set of features, such as TLS support and cluster mode. Additionally, for each language, we have provided a list of advanced features supported by the respective clients, highlighting the unique advantages of one client over another.

## Mandatory Features Overview

1. **Cluster Support** - The ability to operate in a clustered environment, where the data is distributed across multiple shards. Cluster support is essential for applications that require high  scalability.

2. **TLS/SSL Support** - The capability to establish secure connections using TLS/SSL, which encrypts the data transmitted between the client and the server. This is a critical feature for applications that require data privacy and protection against eavesdropping.

## Advanced Features Overview

1. **Read from Replica** - The ability to read data from a replica node, which can be useful for load balancing and reducing the load on the primary node. This feature is particularly important in read-heavy applications.

2. **Exponential Backoff to Prevent Storm** - A strategy used to prevent connection storms by progressively increasing the wait time between retries when attempting to reconnect to a Valkey server. This helps to reduce the load on the server during topology updates, periods of high demand or network instability.

3. **Valkey Version Compatibility** - Indicates which versions of Valkey the client is compatible with. This is crucial for ensuring that the client can leverage the latest features and improvements in the Valkey server.

4. **PubSub State Restoration** - The ability to restore the state of Pub/Sub (publish/subscribe) channels after a client reconnects. This feature ensures that clients can continue receiving messages after disconnections or topology updates such as adding or removing shards, for both legacy Pub/Sub and sharded Pub/Sub. The client will automatically resubscribe the connections to the new node. The advantage is that the application code is simplified, and doesn’t have to take care of resubscribing to new nodes during reconnects.

5. **Cluster Scan** - This feature ensures that the user experience and guarantees for scanning a cluster are identical to those for scanning a single node. The SCAN function operates as a cursor-based iterator. With each command, the server provides an updated cursor, which must be used as the cursor argument in subsequent calls. A complete iteration with SCAN retrieves all elements present in the collection from start to finish. If an element exists in the collection at the beginning and remains until the end of the iteration, SCAN will return it. Conversely, any element removed before the iteration begins and not re-added during the process will not be returned by SCAN. A client supporting this feature ensures the scan iterator remains valid even during failovers or cluster scaling (in or out) during the SCAN operation. This is achieved by storing metadata of the scanned slots and nodes within the GLIDE SCAN cursor and continuously updating the cluster topology.

6. **Latency-Based Read from Replica** - This feature enables reading data from the nearest replica, i.e., the replica that offers the best latency. It supports complex deployments where replicas are distributed across various distances, including different geographical regions, to ensure data is read from the closest replica, thereby minimizing latency.

7. **Client Side Caching** - Valkey client-side caching is a feature that allows clients to cache the results of Redis queries on the client-side, reducing the need for frequent communication with the Valkey server. This can significantly improve application performance by lowering latency, reducing the network usage and cost and reducing the load on the Valkey server. 



---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Python](#python)
  - [Feature Comparison Table](#feature-comparison-table)
- [JavaScript/Node.js](#javascriptnodejs)
  - [Feature Comparison Table](#feature-comparison-table-1)
- [Java](#java)
  - [Feature Comparison Table](#feature-comparison-table-2)
- [Go](#go)
  - [Feature Comparison Table](#feature-comparison-table-3)
- [Ruby](#ruby)
- [PHP](#php)
  - [Feature Comparison Table](#feature-comparison-table-4)
- [C#](#c)
  - [Feature Comparison Table](#feature-comparison-table-5)
- [Other Languages](#other-languages)
- [References](#references)

## Python

- **valkey-glide**
  - GitHub: [valkey-glide](https://github.com/valkey-io/valkey-glide/tree/main/python)
  - Installation: `pip install valkey-glide`
  - Description: An open source Valkey client library that supports Valkey and Redis open source 6.2, 7.0 and 7.2. Valkey GLIDE is designed for reliability, optimized performance, and high-availability, for Valkey and Redis OSS based applications. GLIDE is a multi language client library, written in Rust with programming language bindings, such as Java, node.js and Python.

- **valkey-py**
  - GitHub: [valkey-py](https://github.com/valkey-io/valkey-py)
  - Installation: `pip install valkey`
  - Description: The Python interface to the Valkey key-value store.

<!--- This heading should not be included in the TOC --->
### Feature Comparison Table
{: .no_toc }

| Feature                                      | valkey-glide | valkey-py |
|----------------------------------------------|:------------:|:---------:|
| **Read from replica**                        |     Yes      |    Yes    |
| **Exponential backoff to prevent storm**     |     Yes      |    Yes    |
| **Valkey version compatibility**             |     7.2      |   7.2     |
| **PubSub state restoration**                 |     Yes      |    No     |
| **Cluster Scan**                             |     Yes      |    No     |
| **Latency-Based Read from Replica**          |     No       |    No     |
| **Client Side Caching**                      |     No       |    No     |

## JavaScript/Node.js

- **valkey-glide**
  - GitHub: [valkey-glide](https://github.com/valkey-io/valkey-glide/tree/main/node)
  - Installation: `npm install valkey-glide`
  - Description: An open source Valkey client library that supports Valkey and Redis open source 6.2, 7.0 and 7.2. Valkey GLIDE is designed for reliability, optimized performance, and high-availability, for Valkey and Redis OSS based applications. GLIDE is a multi language client library, written in Rust with programming language bindings, such as Java, node.js and Python.

- **iovalkey**
  - GitHub: [iovalkey](https://github.com/valkey-io/iovalkey)
  - Installation: `npm install iovalkey`
  - Description: A robust, performance-focused and full-featured Redis client for Node.js. This is a friendly fork of ioredis after this commit.

<!--- This heading should not be included in the TOC --->
### Feature Comparison Table
{: .no_toc }

| Feature                                      | valkey-glide | iovalkey  |
|----------------------------------------------|:------------:|:---------:|
| **Read from replica**                        |     Yes      |    Yes    |
| **Exponential backoff to prevent storm**     |     Yes      |    Yes    |
| **Valkey version compatibility**             |     7.2      |    7.2    |
| **PubSub state restoration**                 |     Yes      |    No     |
| **Cluster Scan**                             |     Yes      |    No     |
| **Latency-Based Read from Replica**          |     No       |    No     |
| **Client Side Caching**                      |     No       |    No     |

## Java

- **valkey-glide**
  - GitHub: [valkey-glide](https://github.com/valkey-io/valkey-glide/tree/main/java)
  - Installation: Available via Maven and Gradle
  - Description: An open source Valkey client library that supports Valkey and Redis open source 6.2, 7.0 and 7.2. Valkey GLIDE is designed for reliability, optimized performance, and high-availability, for Valkey and Redis OSS based applications. GLIDE is a multi language client library, written in Rust with programming language bindings, such as Java, node.js and Python.

- **Valkey-Java**
  - GitHub: [valkey-java](https://github.com/valkey-io/valkey-java)
  - Installation: Available via Maven and Gradle
  - Description: valkey-java is Valkey's Java client, derived from Jedis fork, dedicated to maintaining simplicity and high performance.

<!--- This heading should not be included in the TOC --->
### Feature Comparison Table
{: .no_toc }

| Feature                                      | valkey-glide | valkey-java |
|----------------------------------------------|:------------:|:-----------:|
| **Read from replica**                        |     Yes      |     No      |
| **Exponential backoff to prevent storm**     |     Yes      |     Yes     |
| **Valkey version compatibility**             |     7.2      |     7.2     |
| **Cluster support**                          |     Yes      |     Yes     |
| **TLS/SSL support**                          |     Yes      |     Yes     |
| **PubSub state restoration**                 |     Yes      |     No      |
| **Cluster Scan**                             |     Yes      |     No      |
| **Latency-Based Read from Replica**          |     No       |     No      |
| **Client Side Caching**                      |     No       |     No      |


## Go

- **valkey-go**
  - GitHub: [go-valkey-go](https://github.com/valkey-io/valkey-go)
  - Installation: TBD
  - Description: A fast Golang Valkey client that does auto pipelining and supports server-assisted client-side caching.

<!--- This heading should not be included in the TOC --->
### Feature Comparison Table
{: .no_toc }

| Feature                                      | valkey-go  |
|----------------------------------------------|:----------:|
| **Read from replica**                        |     Yes    |
| **Exponential backoff to prevent storm**     |     Yes    |
| **Valkey version compatibility**             |     7.2    |
| **Cluster support**                          |     Yes    |
| **TLS/SSL support**                          |     Yes    |
| **PubSub state restoration**                 |     No     |
| **Cluster Scan**                             |     No     |
| **Latency-Based Read from Replica**          |     No     |
| **Client Side Caching**                      |     No     |



## Ruby

TODO

## PHP

- **Predis**
  - GitHub: [Predis](https://github.com/predis/predis)
  - Installation: `composer require predis/predis`
  - Description: A flexible and feature-rich Valkey client for PHP.

- **phpvalkey**
  - GitHub: [phpredis](https://github.com/phpredis/phpredis)
  - Installation: Install via PECL or compile from source
  - Description: A PHP extension for Redis, offering high performance and a native API.

<!--- This heading should not be included in the TOC --->
### Feature Comparison Table
{: .no_toc }

| Feature                                      | Predis  | phpredis |
|----------------------------------------------|:-------:|:--------:|
| **Read from replica**                        |   Yes   |    Yes   |
| **Exponential backoff to prevent storm**     |   No    |    Yes   |
| **Valkey version compatibility**             |   7.2   |    7.2   |
| **Cluster support**                          |   Yes   |    Yes   |
| **TLS/SSL support**                          |   Yes   |    Yes   |
| **PubSub state restoration**                 |   No    |    No    |
| **Cluster Scan**                             |   No    |    No    |
| **Latency-Based Read from Replica**          |   No    |    No    |
| **Client Side Caching**                      |   No    |    No    |

## C#

- **StackExchange.Redis**
  - GitHub: [StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis)
  - Installation: Available via NuGet
  - Description: A high-performance Valkey client for .NET, maintained by StackExchange.

<!--- This heading should not be included in the TOC --->
### Feature Comparison Table
{: .no_toc }

| Feature                                      | StackExchange.Valkey |
|----------------------------------------------|:--------------------:|
| **Read from replica**                        |         Yes          |
| **Exponential backoff to prevent storm**     |         Yes          |
| **Valkey version compatibility**             |         7.2          |
| **Cluster support**                          |         Yes          |
| **TLS/SSL support**                          |         Yes          |
| **PubSub state restoration**                 |         No           |
| **Cluster Scan**                             |         No           |
| **Latency-Based Read from Replica**          |         No           |
| **Client Side Caching**                      |         No           |

## Other Languages

TBD

## References

- [Valkey Official Documentation](https://valkey.io/docs/)
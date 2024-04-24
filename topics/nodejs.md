---
title: "Node.js guide"
linkTitle: "Node.js"
description: Connect your Node.js application to a Valkey database
weight: 4
aliases:
  - /docs/clients/nodejs/
  - /docs/redis-clients/nodejs/
---

Install Valkey and the client, then connect your Node.js application to a Valkey database. 

## node-redis

[node-redis](https://github.com/redis/node-redis) is a modern, high-performance Valkey and Redis client for Node.js.
`node-redis` requires a running Valkey server. See [Getting started](get-started.md) for Valkey installation instructions.

### Install

To install node-redis, run:

```
npm install redis
```

### Connect

Connect to localhost on port 6379. 

```js
import { createClient } from 'redis';

const client = createClient();

client.on('error', err => console.log('Valkey Client Error', err));

await client.connect();
```

Store and retrieve a simple string.

```js
await client.set('key', 'value');
const value = await client.get('key');
```

Store and retrieve a map.

```js
await client.hSet('user-session:123', {
    name: 'John',
    surname: 'Smith',
    company: 'Garantia',
    age: 29
})
 */
```

To connect to a different host or port, use a connection string in the format `redis[s]://[[username][:password]@][host][:port][/db-number]`:

```js
createClient({
  url: 'redis://alice:foobared@awesome.redis.server:6380'
});
```
To check if the client is connected and ready to send commands, use `client.isReady`, which returns a Boolean. `client.isOpen` is also available. This returns `true` when the client's underlying socket is open, and `false` when it isn't (for example, when the client is still connecting or reconnecting after a network error).

#### Connect to a Valkey cluster

To connect to a Valkey cluster, use `createCluster`.

```js
import { createCluster } from 'redis';

const cluster = createCluster({
    rootNodes: [
        {
            url: 'redis://127.0.0.1:16379'
        },
        {
            url: 'redis://127.0.0.1:16380'
        },
        // ...
    ]
});

cluster.on('error', (err) => console.log('Valkey Cluster Error', err));

await cluster.connect();

await cluster.set('foo', 'bar');
const value = await cluster.get('foo');
console.log(value); // returns 'bar'

await cluster.quit();
```

#### Connect to your production Valkey with TLS

When you deploy your application, use TLS and follow the [security](/docs/management/security/) guidelines.

```js
const client = createClient({
    username: 'default', // use your Valkey user. More info https://valkey.io/topics/acl
    password: 'secret', // use your password here
    socket: {
        host: 'my-valkey.example.com',
        port: 6379,
        tls: true,
        key: readFileSync('./valkey_user_private.key'),
        cert: readFileSync('./valkey_user.crt'),
        ca: [readFileSync('./valkey_ca.pem')]
    }
});

client.on('error', (err) => console.log('Valkey Client Error', err));

await client.connect();

await client.set('foo', 'bar');
const value = await client.get('foo');
console.log(value) // returns 'bar'

await client.disconnect();
```

You can also use discrete parameters and UNIX sockets. Details can be found in the [client configuration guide](https://github.com/redis/node-redis/blob/master/docs/client-configuration.md).

### Learn more

* [Commands](https://redis.js.org/#node-redis-usage-redis-commands)
* [Programmability](https://redis.js.org/#node-redis-usage-programmability)
* [Clustering](https://redis.js.org/#node-redis-usage-clustering)
* [GitHub](https://github.com/redis/node-redis)

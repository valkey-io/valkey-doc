---
title: "Python guide"
linkTitle: "Python"
description: Connect your Python application to a Redis database
weight: 5
aliases:
  - /docs/clients/python/
  - /docs/redis-clients/python/
---

Install Redis and the Redis client, then connect your Python application to a Redis database. 

## redis-py

Get started with the [redis-py](https://github.com/redis/redis-py) client for Redis. 

`redis-py` requires a running Redis. See [Getting started](/docs/getting-started/) for Redis installation instructions.

### Install

To install `redis-py`, enter:

```bash
pip install redis
```

For faster performance, install Redis with [`hiredis`](https://github.com/redis/hiredis) support. This provides a compiled response parser, and for most cases requires zero code changes. By default, if `hiredis` >= 1.0 is available, `redis-py` attempts to use it for response parsing.

{{% alert title="Note" %}}
The Python `distutils` packaging scheme is no longer part of Python 3.12 and greater. If you're having difficulties getting `redis-py` installed in a Python 3.12 environment, consider updating to a recent release of `redis-py`.
{{% /alert %}}

```bash
pip install redis[hiredis]
```

### Connect

Connect to localhost on port 6379, set a value in Redis, and retrieve it. All responses are returned as bytes in Python. To receive decoded strings, set `decode_responses=True`. For more connection options, see [these examples](https://redis.readthedocs.io/en/stable/examples.html).

```python
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
```

Store and retrieve a simple string.

```python
r.set('foo', 'bar')
# True
r.get('foo')
# bar
```

Store and retrieve a dict.

```python
r.hset('user-session:123', mapping={
    'name': 'John',
    "surname": 'Smith',
    "company": 'Redis',
    "age": 29
})
# True

r.hgetall('user-session:123')
# {'surname': 'Smith', 'name': 'John', 'company': 'Redis', 'age': '29'}
```

#### Connect to a Redis cluster

To connect to a Redis cluster, use `RedisCluster`.

```python
from redis.cluster import RedisCluster

rc = RedisCluster(host='localhost', port=16379)

print(rc.get_nodes())
# [[host=127.0.0.1,port=16379,name=127.0.0.1:16379,server_type=primary,redis_connection=Redis<ConnectionPool<Connection<host=127.0.0.1,port=16379,db=0>>>], ...

rc.set('foo', 'bar')
# True

rc.get('foo')
# b'bar'
```
For more information, see [redis-py Clustering](https://redis-py.readthedocs.io/en/stable/clustering.html).

#### Connect to your production Redis with TLS

When you deploy your application, use TLS and follow the [Redis security](/docs/management/security/) guidelines.

```python
import redis

r = redis.Redis(
    host="my-redis.cloud.redislabs.com", port=6379,
    username="default", # use your Redis user. More info https://redis.io/docs/management/security/acl/
    password="secret", # use your Redis password
    ssl=True,
    ssl_certfile="./redis_user.crt",
    ssl_keyfile="./redis_user_private.key",
    ssl_ca_certs="./redis_ca.pem",
)
r.set('foo', 'bar')
# True

r.get('foo')
# b'bar'
```
For more information, see [redis-py TLS examples](https://redis-py.readthedocs.io/en/stable/examples/ssl_connection_examples.html).


### Learn more

* [Command reference](https://redis-py.readthedocs.io/en/stable/commands.html)
* [Tutorials](https://redis.readthedocs.io/en/stable/examples.html)
* [GitHub](https://github.com/redis/redis-py)

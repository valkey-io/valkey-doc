Establishes an RDMA session for the current connection.
A client must send this command once on a connection before it can use [`BLOB.RDMA_SET`](blob.rdma_set.md) or [`BLOB.RDMA_GET`](blob.rdma_get.md) on that connection.

`client-rdma-address` is the fabric address of the client endpoint, encoded as hexadecimal text.
The client gets this address from its libfabric endpoint.
When `largeobj.fabric-provider` is `EfaDirect`, the address must be exactly 32 bytes (64 hexadecimal characters).
When `largeobj.fabric-provider` is `Emulated`, the address must be a socket address: 16 bytes for IPv4 (`sockaddr_in`) or 28 bytes for IPv6 (`sockaddr_in6`).
The command takes exactly one argument.
With no argument or more than one argument, it returns an error.

The server adds the client address to each of its fabric services.
The reply is an array with one hexadecimal fabric address for each server fabric service.
The client must add all the returned addresses to its own address vector before the first transfer.

The session belongs to the connection.
The server removes the session when the connection closes.
A connection can have only one session: a second `BLOB.RDMA_HELLO` on the same connection returns an error.
To use a new client endpoint, open a new connection.

If the RDMA fabric did not start on the server, the command returns an error.
In that case, only the TCP commands, [`BLOB.TCP_SET`](blob.tcp_set.md) and [`BLOB.TCP_GET`](blob.tcp_get.md), are available.

For the full RDMA flow and the fabric configuration, see [Valkey Large Object - RDMA Transfers](../topics/large-object-rdma.md).

## Reply

Array of strings: one string for each server fabric service, with the hexadecimal fabric address of that service.

An error occurs if RDMA is not available on the server, if the client address is not valid for the fabric provider, or if the connection already has an RDMA session. See [Errors](../topics/large-object-rdma.md#errors) for all errors.

## Examples

A useful `BLOB.RDMA_HELLO` needs a client that has a libfabric endpoint.
`valkey-cli` can send the command, but it cannot do the RDMA transfers that follow.
The example shows the command shape and the reply, with example addresses.

```
127.0.0.1:6379> BLOB.RDMA_HELLO 0a1b2c3d4e5f60718293a4b5c6d7e8f900112233445566778899aabbccddeeff
1) "fe80000000000000049a1ffffe2b3c4d0b000000c5a3d1e20000000000000000"
2) "fe80000000000000049a1ffffe2b3c4e0c000000d7b4e2f30000000000000000"
127.0.0.1:6379> BLOB.RDMA_HELLO 0a1b2c3d4e5f60718293a4b5c6d7e8f900112233445566778899aabbccddeeff
(error) ERR RDMA session already established
```

These errors do not need an RDMA client.
The server in this example uses the `EfaDirect` fabric provider:

```
127.0.0.1:6379> BLOB.RDMA_HELLO zz
(error) ERR invalid rdma address hex
127.0.0.1:6379> BLOB.RDMA_HELLO 0a1b
(error) ERR rdma address must be 32 bytes
127.0.0.1:6379> BLOB.RDMA_HELLO 0a1b extra
(error) ERR wrong number of arguments for 'BLOB.RDMA_HELLO' command
```

With the `Emulated` fabric provider, `valkey-cli` can open a session.
The reply has one address for each server fabric service, here one:

```
127.0.0.1:6379> BLOB.RDMA_HELLO 0a1b
(error) ERR rdma address is not a valid sockaddr
127.0.0.1:6379> BLOB.RDMA_HELLO 02001f907f0000010000000000000000
1) "020098ff7f0000010000000000000000"
127.0.0.1:6379> BLOB.RDMA_HELLO 02001f907f0000010000000000000000
(error) ERR RDMA session already established
```

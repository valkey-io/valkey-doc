---
title: "C#/.NET guide"
linkTitle: "C#/.NET"
description: Connect your .NET application to a Valkey database
weight: 1
aliases:
  - /docs/clients/dotnet/
  - /docs/redis-clients/dotnet/
---

Install Valkey and the Valkey client, then connect your .NET application to a Valkey database.

## NRedisStack

[NRedisStack](https://github.com/redis/NRedisStack) is a .NET client for Valkey and Redis.
`NredisStack` requires a running Valkey or Redis server. See [Getting started](get-started.md) for Valkey installation instructions.

### Install

Using the `dotnet` CLI, run:

```
dotnet add package NRedisStack
```

### Connect

Connect to localhost on port 6379.

```
using NRedisStack;
using StackExchange.Redis;
//...
ConnectionMultiplexer redis = ConnectionMultiplexer.Connect("localhost");
IDatabase db = redis.GetDatabase();
```

Store and retrieve a simple string.

```csharp
db.StringSet("foo", "bar");
Console.WriteLine(db.StringGet("foo")); // prints bar
```

Store and retrieve a HashMap.

```csharp
var hash = new HashEntry[] { 
    new HashEntry("name", "John"), 
    new HashEntry("surname", "Smith"),
    new HashEntry("company", "Garantia"),
    new HashEntry("age", "29"),
    };
db.HashSet("user-session:123", hash);

var hashFields = db.HashGetAll("user-session:123");
Console.WriteLine(String.Join("; ", hashFields));
// Prints: 
// name: John; surname: Smith; company: Garantia; age: 29
```

#### Connect to a Valkey cluster

To connect to a Valkey cluster, you just need to specify one or all cluster endpoints in the client configuration:

```csharp
ConfigurationOptions options = new ConfigurationOptions
{
    //list of available nodes of the cluster along with the endpoint port.
    EndPoints = {
        { "localhost", 16379 },
        { "localhost", 16380 },
        // ...
    },            
};

ConnectionMultiplexer cluster = ConnectionMultiplexer.Connect(options);
IDatabase db = cluster.GetDatabase();

db.StringSet("foo", "bar");
Console.WriteLine(db.StringGet("foo")); // prints bar
```

#### Connect to Valkey with TLS

When you deploy your application, use TLS and follow the [security](/docs/management/security/) guidelines.

Before connecting your application to the TLS-enabled Valkey server, ensure that your certificates and private keys are in the correct format.

To convert user certificate and private key from the PEM format to `pfx`, use this command:

```bash
openssl pkcs12 -inkey valkey_user_private.key -in valkey_user.crt -export -out valkey.pfx
```

Enter password to protect your `pfx` file.

Establish a secure connection with your Valkey database using this snippet.

```csharp
ConfigurationOptions options = new ConfigurationOptions
{
    EndPoints = { { "my-valkey.example.com", 6379 } },
    User = "default",  // use your Valkey user. More info https://valkey.io/topics/acl
    Password = "secret", // use your Valkey password
    Ssl = true,
    SslProtocols = System.Security.Authentication.SslProtocols.Tls12                
};

options.CertificateSelection += delegate
{
    return new X509Certificate2("valkey.pfx", "secret"); // use the password you specified for pfx file
};
options.CertificateValidation += ValidateServerCertificate;

bool ValidateServerCertificate(
        object sender,
        X509Certificate? certificate,
        X509Chain? chain,
        SslPolicyErrors sslPolicyErrors)
{
    if (certificate == null) {
        return false;       
    }

    var ca = new X509Certificate2("valkey_ca.pem");
    bool verdict = (certificate.Issuer == ca.Subject);
    if (verdict) {
        return true;
    }
    Console.WriteLine("Certificate error: {0}", sslPolicyErrors);
    return false;
}

ConnectionMultiplexer muxer = ConnectionMultiplexer.Connect(options);   
            
//Creation of the connection to the DB
IDatabase conn = muxer.GetDatabase();

//send SET command
conn.StringSet("foo", "bar");

//send GET command and print the value
Console.WriteLine(conn.StringGet("foo"));   
```

### Learn more

* [GitHub](https://github.com/redis/NRedisStack)

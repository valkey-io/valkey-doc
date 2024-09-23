Return the username the current connection is authenticated with.
New connections are authenticated with the "default" user. They
can change user using `AUTH`.

## Examples

```
127.0.0.1:6379> ACL WHOAMI
"default"
```

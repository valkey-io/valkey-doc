## Syntax

```bash
JSON.DEBUG <subcommand & arguments>
```

## Return

Depends on the subcommand:

* MEMORY
    * If the path is enhanced syntax:
        * returns an array of integers, representing memory size (in bytes) of JSON value at each path.
        * returns an empty array if the Redis key does not exist.
    * If the path is restricted syntax:
        * returns an integer, memory size the JSON value in bytes.
        * returns null if the Redis key does not exist.
* DEPTH
    * returns an integer, the maximum path depth of the JSON document.
    * returns null if the Redis key does not exist.
* FIELDS
    * If the path is enhanced syntax:
        * returns an array of integers, representing number of fields of JSON value at each path.
        * returns an empty array if the Redis key does not exist.
    * If the path is restricted syntax:
        * returns an integer, number of fields of the JSON value.
        * returns null if the Redis key does not exist.
* HELP
    * returns an array of help messages

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '[1, 2.3, "foo", true, null, {}, [], {"a":1, "b":2}, [1,2,3]]'
OK
127.0.0.1:6379> JSON.DEBUG MEMORY k1 $[*]
1) (integer) 16
2) (integer) 16
3) (integer) 19
4) (integer) 16
5) (integer) 16
6) (integer) 16
7) (integer) 16
8) (integer) 50
9) (integer) 64
127.0.0.1:6379> JSON.DEBUG FIELDS k1 $[*]
1) (integer) 1
2) (integer) 1
3) (integer) 1
4) (integer) 1
5) (integer) 1
6) (integer) 0
7) (integer) 0
8) (integer) 2
9) (integer) 3
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"firstName":"John","lastName":"Smith","age":27,"weight":135.25,"isAlive":true,"address":{"street":"21 2nd Street","city":"New York","state":"NY","zipcode":"10021-3100"},"phoneNumbers":[{"type":"home","number":"212 555-1234"},{"type":"office","number":"646 555-4567"}],"children":[],"spouse":null}'
OK
127.0.0.1:6379> JSON.DEBUG MEMORY k1
(integer) 632
127.0.0.1:6379> JSON.DEBUG MEMORY k1 .phoneNumbers
(integer) 166

127.0.0.1:6379> JSON.DEBUG FIELDS k1
(integer) 19
127.0.0.1:6379> JSON.DEBUG FIELDS k1 .address
(integer) 4
```

```bash
127.0.0.1:6379> JSON.DEBUG HELP
1) JSON.DEBUG MEMORY <key> [path] - report memory size (bytes) of the JSON element. Path defaults to root if not provided.
2) JSON.DEBUG FIELDS <key> [path] - report number of fields in the JSON element. Path defaults to root if not provided.
3) JSON.DEBUG DEPTH <key> - report depth of JSON doc.
3) JSON.DEBUG HELP - print help message.
```
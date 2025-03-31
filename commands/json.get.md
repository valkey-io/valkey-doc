Get the serialized JSON at one or multiple paths.

## Syntax

```bash
JSON.GET <key>
         [INDENT indentation-string]
         [NEWLINE newline-string]
         [SPACE space-string]
         [NOESCAPE]
         [path ...]
```

* key - required, Redis key of document type
* INDENT/NEWLINE/SPACE - optional, controls the format of the returned JSON string, i.e., "pretty print". The default
  value of each one is empty string. They can be overidden in any combination. They can be specified in any order.
* NOESCAPE - optional, allowed to be present for legacy compatibility and has no other effect.
* path - optional, zero or more JSON paths, defaults to the root path if none is given. The path arguments must be
  placed at the end.

## Return

* Enhanced path syntax:
    * If one path is given:
        * Return serialized string of an array of values.
        * If no value is selected, the command returns an empty array.
    * If multiple paths are given:
        * Return a stringified JSON object, in which each path is a key.
        * If there are mixed enhanced and restricted path syntax, the result conforms to the enhanced syntax.
        * If a path does not exist, its corresponding value is an empty array.

* Restricted path syntax:
    * If one path is given:
        * Return serialized string of the value at the path.
        * If multiple values are selected, the command returns the first value.
        * If the path does not exist, the command returns NONEXISTENT error.
    * If multiple paths are given:
        * Return a stringified JSON object, in which each path is a key.
        * The result conforms to the restricted path syntax if and only if all paths are restricted paths.
        * If a path does not exist, the command returns NONEXISTENT error

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"firstName":"John","lastName":"Smith","age":27,"weight":135.25,"isAlive":true,"address":{"street":"21 2nd Street","city":"New York","state":"NY","zipcode":"10021-3100"},"phoneNumbers":[{"type":"home","number":"212 555-1234"},{"type":"office","number":"646 555-4567"}],"children":[],"spouse":null}'
OK
127.0.0.1:6379> JSON.GET k1 $.address.*
"[\"21 2nd Street\",\"New York\",\"NY\",\"10021-3100\"]"
127.0.0.1:6379> JSON.GET k1 indent "\t" space " " NEWLINE "\n" $.address.*
"[\n\t\"21 2nd Street\",\n\t\"New York\",\n\t\"NY\",\n\t\"10021-3100\"\n]"
127.0.0.1:6379> JSON.GET k1 $.firstName $.lastName $.age
"{\"$.firstName\":[\"John\"],\"$.lastName\":[\"Smith\"],\"$.age\":[27]}"

127.0.0.1:6379> JSON.SET k2 . '{"a":{}, "b":{"a":1}, "c":{"a":1, "b":2}}'
OK
127.0.0.1:6379> json.get k2 $..*
"[{},{\"a\":1},{\"a\":1,\"b\":2},1,1,2]"
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"firstName":"John","lastName":"Smith","age":27,"weight":135.25,"isAlive":true,"address":{"street":"21 2nd Street","city":"New York","state":"NY","zipcode":"10021-3100"},"phoneNumbers":[{"type":"home","number":"212 555-1234"},{"type":"office","number":"646 555-4567"}],"children":[],"spouse":null}'
OK
127.0.0.1:6379> JSON.GET k1 .address
"{\"street\":\"21 2nd Street\",\"city\":\"New York\",\"state\":\"NY\",\"zipcode\":\"10021-3100\"}"
127.0.0.1:6379> JSON.GET k1 indent "\t" space " " NEWLINE "\n" .address
"{\n\t\"street\": \"21 2nd Street\",\n\t\"city\": \"New York\",\n\t\"state\": \"NY\",\n\t\"zipcode\": \"10021-3100\"\n}"
127.0.0.1:6379> JSON.GET k1 .firstName .lastName .age
"{\".firstName\":\"John\",\".lastName\":\"Smith\",\".age\":27}"
```

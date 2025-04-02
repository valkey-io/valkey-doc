Return the JSON value at the given path in Valkey Serialization Protocol (RESP).\nIf the value is container, the response is RESP array or nested array.\n\n* JSON null is mapped to the RESP Null Bulk String.\n* JSON boolean values are mapped to the respective RESP Simple Strings.\n* Integer numbers are mapped to RESP Integers.\n* Floating point numbers are mapped to RESP Bulk Strings.\n* JSON Strings are mapped to RESP Bulk Strings.\n* JSON Arrays are represented as RESP Arrays, where the first element is the simple string [,\n  followed by the array's elements.\n* JSON Objects are represented as RESP Arrays, where the first element is the simple string {,\n  followed by key-value pairs, each of which is a RESP bulk string.

## Syntax

```bash
JSON.RESP <key> [path]
```
* key - required, Redis key of document type
* path - optional, a JSON path. Defaults to the root path if not provided

## Return

* If the path is enhanced syntax:
    * Array of arrays. Each array element represents the RESP form of the value at one path.
    * Empty array if the document key does not exist.

* If the path is restricted syntax:
    * Array, representing the RESP form of the value at the path.
    * Null if the document key does not exist.

## Examples

Enhanced path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"firstName":"John","lastName":"Smith","age":27,"weight":135.25,"isAlive":true,"address":{"street":"21 2nd Street","city":"New York","state":"NY","zipcode":"10021-3100"},"phoneNumbers":[{"type":"home","number":"212 555-1234"},{"type":"office","number":"646 555-4567"}],"children":[],"spouse":null}'
OK

127.0.0.1:6379> JSON.RESP k1 $.address
1) 1) {
   2) 1) "street"
      2) "21 2nd Street"
   3) 1) "city"
      2) "New York"
   4) 1) "state"
      2) "NY"
   5) 1) "zipcode"
      2) "10021-3100"

127.0.0.1:6379> JSON.RESP k1 $.address.*
1) "21 2nd Street"
2) "New York"
3) "NY"
4) "10021-3100"

127.0.0.1:6379> JSON.RESP k1 $.phoneNumbers
1) 1) [
   2) 1) {
      2) 1) "type"
         2) "home"
      3) 1) "number"
         2) "212 555-1234"
   3) 1) {
      2) 1) "type"
         2) "office"
      3) 1) "number"
         2) "646 555-4567"

127.0.0.1:6379> JSON.RESP k1 $.phoneNumbers[*]
1) 1) {
   2) 1) "type"
      2) "home"
   3) 1) "number"
      2) "212 555-1234"
2) 1) {
   2) 1) "type"
      2) "office"
   3) 1) "number"
      2) "646 555-4567"
```

Restricted path syntax:

```bash
127.0.0.1:6379> JSON.SET k1 . '{"firstName":"John","lastName":"Smith","age":27,"weight":135.25,"isAlive":true,"address":{"street":"21 2nd Street","city":"New York","state":"NY","zipcode":"10021-3100"},"phoneNumbers":[{"type":"home","number":"212 555-1234"},{"type":"office","number":"646 555-4567"}],"children":[],"spouse":null}'
OK

127.0.0.1:6379> JSON.RESP k1 .address
1) {
2) 1) "street"
   2) "21 2nd Street"
3) 1) "city"
   2) "New York"
4) 1) "state"
   2) "NY"
5) 1) "zipcode"
   2) "10021-3100"

127.0.0.1:6379> JSON.RESP k1
 1) {
 2) 1) "firstName"
    2) "John"
 3) 1) "lastName"
    2) "Smith"
 4) 1) "age"
    2) (integer) 27
 5) 1) "weight"
    2) "135.25"
 6) 1) "isAlive"
    2) true
 7) 1) "address"
    2) 1) {
       2) 1) "street"
          2) "21 2nd Street"
       3) 1) "city"
          2) "New York"
       4) 1) "state"
          2) "NY"
       5) 1) "zipcode"
          2) "10021-3100"
 8) 1) "phoneNumbers"
    2) 1) [
       2) 1) {
          2) 1) "type"
             2) "home"
          3) 1) "number"
             2) "212 555-1234"
       3) 1) {
          2) 1) "type"
             2) "office"
          3) 1) "number"
             2) "646 555-4567"
 9) 1) "children"
    2) 1) [
10) 1) "spouse"
    2) (nil)
```

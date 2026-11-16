By default, the command pops a single element from the end of the list.
When provided with the optional `count` argument, the reply will consist of up
to `count` elements, depending on the list's length.
Deletes the list if the last element was popped.

## Reply

One of the following:

* Null: if the key does not exist.
* String: when called without the _count_ argument, the value of the last element.
* Array: when called with the _count_ argument, a list of popped elements.

## Examples

```
127.0.0.1:6379> RPUSH mylist "one" "two" "three" "four" "five"
(integer) 5
127.0.0.1:6379> RPOP mylist
"five"
127.0.0.1:6379> RPOP mylist 2
1) "four"
2) "three"
127.0.0.1:6379> LRANGE mylist 0 -1
1) "one"
2) "two"
```

The `SADDEX` command adds one or more members to the set stored at `key` and optionally sets their expiration time.
If `key` doesn't exist, a new set is created.

Without an expiration option set or `KEEPTTL`, `SADDEX` adds the members without an expiration time.
Any existing member named in the command loses its expiration time and becomes persistent.
This is different from [`SADD`](sadd.md), which leaves the expiration time of an existing member unchanged.

## Options

The `SADDEX` command supports a set of options that modify its behavior:

* NX, only perform the operation if `key` does not exist.
* XX, only perform the operation if `key` already exists.
* MNX, only perform the operation if none of the specified members exist in the set.
* MXX, only perform the operation if all of the specified members exist in the set.
* EX `seconds`, sets the specified expiration time in seconds.
* PX `milliseconds`, sets the specified expiration time in milliseconds.
* EXAT `unix-time-seconds`, sets the specified Unix time in seconds at which the members expire.
* PXAT `unix-time-milliseconds`, sets the specified Unix time in milliseconds at which the members expire.
* KEEPTTL, keeps the existing expiration time of members that already exist.
New members are added without an expiration time.

Note the following:

1. `NX` and `XX` are mutually exclusive.
`MNX` and `MXX` are mutually exclusive.
A key condition and a member condition can be combined.
2. `EX`, `PX`, `EXAT`, `PXAT`, and `KEEPTTL` are mutually exclusive.
3. Member conditions apply to the whole call: if any specified member fails the condition, no member is added or changed.
4. A member that has logically expired, but has not been removed yet, is treated as nonexistent by `MNX` and `MXX`.
5. An expiration time of `0` with `EX` or `PX`, or a time in the past with `EXAT` or `PXAT`, removes the specified members from the set immediately.
If the set becomes empty, the key is deleted.

## Reply

The reply is one of the following:

* Integer: `0` if the operation was skipped because an `NX`, `XX`, `MNX`, or `MXX` condition was not met.
* Integer: `1` if the conditions were met and all the specified members were processed, even if the set did not change.

## Examples

1. Add three members without an expiration time:

```
127.0.0.1:6379> SADDEX myset MEMBERS 3 a b c
(integer) 1
```

2. The `MNX` condition fails because `a` and `b` already exist, so nothing changes:

```
127.0.0.1:6379> SADDEX myset MNX EX 100 MEMBERS 2 a b
(integer) 0
```

3. Set an expiration time on existing members:

```
127.0.0.1:6379> SADDEX myset MXX EX 100 MEMBERS 2 a b
(integer) 1
127.0.0.1:6379> STTL myset MEMBERS 3 a b c
1) (integer) 100
2) (integer) 100
3) (integer) -1
```

4. Add a new member and keep the expiration time of an existing one:

```
127.0.0.1:6379> SADDEX myset KEEPTTL MEMBERS 2 a d
(integer) 1
127.0.0.1:6379> STTL myset MEMBERS 2 a d
1) (integer) 98
2) (integer) -1
```

5. Without `KEEPTTL`, the expiration time of an existing member is removed:

```
127.0.0.1:6379> SADDEX myset MEMBERS 1 a
(integer) 1
127.0.0.1:6379> STTL myset MEMBERS 1 a
1) (integer) -1
```

6. An expiration time of `0` removes the members:

```
127.0.0.1:6379> SADDEX myset EX 0 MEMBERS 4 a b c d
(integer) 1
127.0.0.1:6379> EXISTS myset
(integer) 0
```

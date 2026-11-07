Increments the numeric value stored at `key`, optionally setting or updating its expiration in the same atomic operation.
If the key does not exist, it is set to `0` before performing the operation.
An error is returned if the key contains a value of the wrong type or contains a
string that can not be represented as a number.

By default the increment is `1`. Use `BYINT` to increment by a 64 bit signed
integer, or `BYFLOAT` to increment by a floating-point number.

`INCREX` combines what is usually done with `INCR`/`INCRBY`/`INCRBYFLOAT` plus
`EXPIRE` (or a `MULTI`/`EXEC` block or Lua script) into a single command, and
adds optional lower and upper bounds on the resulting value.

## Options

### Condition

* `NX` -- Only perform the operation if the key does not already exist.
* `XX` -- Only perform the operation if the key already exists.

### Expiration

* `EX seconds` -- Set the expire time, in seconds.
* `PX milliseconds` -- Set the expire time, in milliseconds.
* `EXAT unix-time-seconds` -- Set the expire time to a Unix timestamp, in seconds.
* `PXAT unix-time-milliseconds` -- Set the expire time to a Unix timestamp, in milliseconds.
* `PERSIST` -- Remove the existing expiration from the key.
* `ENX` -- Only set the expiration if the key currently has no TTL.
  Requires one of `EX`, `PX`, `EXAT` or `PXAT`, and cannot be combined with `PERSIST`.

### Increment

* `BYINT increment` -- Increment by a 64 bit signed integer.
* `BYFLOAT increment` -- Increment by a floating-point number.

### Bounds

* `LBOUND lowerbound` -- The minimum allowed value of the result.
* `UBOUND upperbound` -- The maximum allowed value of the result.
* `SATURATE` -- If the result would be out of bounds, clamp it to `LBOUND`/`UBOUND`
  (or to the limits of the numeric type when no explicit bound is given) instead
  of rejecting the operation.

The bound values are integers when used with `BYINT` and floating-point numbers
when used with `BYFLOAT`.

Without `SATURATE`, an operation that would take the value out of bounds is
rejected: the value is left unchanged and the reply is `[current_value, 0]`.

## Reply

Array: a two-element array.

1. The value of the key after the operation. If the increment was not applied,
   this is the current value of the key.
2. The increment that was actually applied. This is `0` if the operation was
   skipped (for example because of `NX`/`XX`) or rejected because it was out of
   bounds, and may differ from the requested increment when `SATURATE` clamps
   the result.

## Examples

```
127.0.0.1:6379> SET mykey "10"
OK
127.0.0.1:6379> INCREX mykey
1) (integer) 11
2) (integer) 1
127.0.0.1:6379> INCREX mykey BYINT 5 EX 60
1) (integer) 16
2) (integer) 5
127.0.0.1:6379> INCREX mykey BYINT 100 UBOUND 20
1) (integer) 16
2) (integer) 0
127.0.0.1:6379> INCREX mykey BYINT 100 UBOUND 20 SATURATE
1) (integer) 20
2) (integer) 4
```

## Pattern: Fixed-window rate limiter

A rate limiter built with `INCR` needs a `MULTI`/`EXEC` block or a Lua script
to make sure the counter always gets an expiration, otherwise the key can be
leaked if the client fails between the two commands.
`INCREX` does this in one atomic command.
With `ENX`, the expiration is set only when the counter is created, so the
window is not extended by later requests:

```
FUNCTION LIMIT_API_CALL(ip)
current, applied = INCREX(ip, EX 1, ENX, BYINT 1, UBOUND 10)
IF applied == 0 THEN
    ERROR "too many requests per second"
ELSE
    PERFORM_API_CALL()
END
```

The counter lives for one second from the first request in the window. Once it
reaches the upper bound of `10`, further calls are rejected (the reply is
`[10, 0]`) without modifying the counter.

## Pattern: Bounded counter

Use `LBOUND`, `UBOUND` and `SATURATE` to keep a value inside a range, for example
an inventory level or a score that must never go below zero:

```
SET stock:item42 2
INCREX stock:item42 BYINT -3 LBOUND 0 SATURATE
```

If only 2 units remain, the key is set to `0` and the second element of the
reply is `-2`, telling the caller how much was actually applied.

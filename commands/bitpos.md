Return the position of the first bit set to 1 or 0 in a string.

The position is returned, thinking of the string as an array of bits from left to
right, where the first byte's most significant bit is at position 0, the second
byte's most significant bit is at position 8, and so forth.

The same bit position convention is followed by [`GETBIT`](getbit.md) and [`SETBIT`](setbit.md).

By default, all the bytes contained in the string are examined.
It is possible to look for bits only in a specified interval by passing the additional arguments `start` and `end`. You can also just pass `start`, the operation will assume that the end is the last byte of the string. However there are semantic differences as explained later.
By default, the range is interpreted as a range of bytes and not a range of bits, so `start=0` and `end=2` means to look at the first three bytes.

You can use the optional `BIT` modifier to specify that the range should be interpreted as a range of bits.
So `start=0` and `end=2` means to look at the first three bits.

Note that bit positions are returned always as absolute values starting from bit zero even when `start` and `end` are used to specify a range.

Similar to the [`GETRANGE`](getrange.md) command, `start` and `end` can contain negative values in
order to index bytes starting from the end of the string, where -1 is the last
byte, -2 is the penultimate, and so forth. When `BIT` is specified, -1 is the last
bit, -2 is the penultimate, and so forth.

Non-existent keys are treated as empty strings.

## Reply

One of the following:

* Integer: the position of the first bit set to 1 or 0 according to the request
* Integer: `-1`. In case the `bit` argument is 1 and the string is empty or composed of just zero bytes

If we look for set bits (the bit argument is 1) and the string is empty or composed of just zero bytes, -1 is returned.

If we look for clear bits (the bit argument is 0) and the string only contains bits set to 1, the function returns the first bit not part of the string on the right. So if the string is three bytes set to the value `0xff` the command `BITPOS key 0` will return 24, since up to bit 23 all the bits are 1.

The function considers the right of the string as padded with zeros if you look for clear bits and specify no range or the _start_ argument **only**.

However, this behavior changes if you are looking for clear bits and specify a range with both _start_ and _end_.

If a clear bit isn't found in the specified range, the function returns -1 as the user specified a clear range and there are no 0 bits in that range.

## Examples

```
127.0.0.1:6379> SET mykey "\xff\xf0\x00"
OK
127.0.0.1:6379> BITPOS mykey 0
(integer) 12
127.0.0.1:6379> SET mykey "\x00\xff\xf0"
OK
127.0.0.1:6379> BITPOS mykey 1 0
(integer) 8
127.0.0.1:6379> BITPOS mykey 1 2
(integer) 16
127.0.0.1:6379> BITPOS mykey 1 2 -1 BYTE
(integer) 16
127.0.0.1:6379> BITPOS mykey 1 7 15 BIT
(integer) 8
127.0.0.1:6379> set mykey "\x00\x00\x00"
OK
127.0.0.1:6379> BITPOS mykey 1
(integer) -1
127.0.0.1:6379> BITPOS mykey 1 7 -3 BIT
(integer) -1
```

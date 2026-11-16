Read-only variant of the `GEORADIUSBYMEMBER` command.

This command is identical to the `GEORADIUSBYMEMBER` command, except that it doesn't support the optional `STORE` and `STOREDIST` parameters.

## Alternative

`GEOSEARCH` with the `BYRADIUS` and `FROMMEMBER` arguments.

## Reply

One of the following:

* If no `WITH*` option is specified, an array of matched member names
* If `WITHCOORD`, `WITHDIST`, or `WITHHASH` options are specified, the command returns an array of arrays, where each sub-array represents a single item:
    * The distance from the center as a floating point number, in the same unit specified in the radius.
    * The Geohash integer.
    * The coordinates as a two items x,y array (longitude,latitude).

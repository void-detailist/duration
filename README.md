# duration: Operations with ISO 8601 durations.

## What is this.

ISO 8601 is most commonly known as a way to exchange datetimes in textual format. A
lesser known aspect of the standard is the representation of durations. They have a
shape similar to this:

```
P3Y6M4DT12H30M5S80m90u120n
```

which symbols defined as blow:<br />

```
"H" -> "hours"
"M" -> "minutes"
"S" -> "seconds"
"m" -> "miliseconds"
"u" -> "microseconds"
"n" -> "nanoseconds"
```

As this module maps ISO 8601 dates/times to standard Python data type.

parse:
```
parses an ISO 8601 duration string into Duration object.
```

generate:
```
generate a duration object into ISO 8601 duration string 
```
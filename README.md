# frozendict
Implementation of immutable dictionary in python using a left leaning red black tree on top of named tuples. Requires Python 3.5.

I created this project after playing with immutable types in Clojure and wanting something similar in python. Instances are  immutable so long as the values are immutable.  The keys must be immutable and comparable.

```python
d = FrozenDict({"foo": "bar"})
e = FrozenDict(d, baz=42)
```

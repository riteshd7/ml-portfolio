"""
Exercise 1 — Number Stats Calculator
=====================================

Goal
----
Build 7 small functions that each compute one statistic over a list of numbers.
Then build one wrapper function `summary()` that calls all of them and returns
a dict.

Why this exercise
-----------------
This is your warm-up. It's deliberately easy. The point is to:
- Type code from a blank file (no copy-paste)
- Get used to writing assertions to test your own code
- Build the muscle of "function takes input, returns output, no side effects"

You should finish in 25–40 minutes. If you take longer than 60, you're
overthinking; ship what you have and move on.

Specification
-------------
Implement each function below. Each takes a list of numbers (ints or floats)
and returns a single number (or, for `mode`, a list).

    count(nums)   -> int      number of elements
    total(nums)   -> float    sum of elements
    mean(nums)    -> float    arithmetic mean
    median(nums)  -> float    middle value (average of two middles if even count)
    mode(nums)    -> list     most-frequent value(s); return ALL ties as a list
    variance(nums)-> float    population variance: mean of squared deviations
    stddev(nums)  -> float    square root of variance

Then implement:

    summary(nums) -> dict     keys: "count","sum","mean","median","mode","var","stddev"

Edge cases your code must handle
--------------------------------
1. Empty list: every function should raise ValueError("empty list")
2. Single-element list: median == mean == that element; variance == 0
3. Even-length list: median is mean of the two middle values
4. Mode with multiple ties: return ALL tied values (sorted ascending)

Forbidden today
---------------
- `statistics` module (write the math yourself; you have the math background)
- `numpy`, `pandas` (Day 8+)
- LLMs / Stack Overflow on first pass

Allowed
-------
- Built-in functions: `sum`, `len`, `sorted`, `min`, `max`
- `collections.Counter` for `mode` (this is the right tool)
- `math.sqrt`
"""

from collections import Counter
import math


def count(nums):
    # TODO: return number of elements; raise ValueError if empty
    pass


def total(nums):
    # TODO
    pass


def mean(nums):
    # TODO
    pass


def median(nums):
    # TODO: handle odd vs even length
    pass


def mode(nums):
    # TODO: return list of all values with max frequency, sorted ascending
    pass


def variance(nums):
    # TODO: population variance = mean of (x - mean)^2
    pass


def stddev(nums):
    # TODO: sqrt of variance
    pass


def summary(nums):
    # TODO: return dict with keys: count, sum, mean, median, mode, var, stddev
    pass


# ---------------------------------------------------------------------------
# Tests — DO NOT MODIFY. Run this file directly: `python 01_number_stats.py`
# Every assertion must pass.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Basic case
    assert count([1, 2, 3, 4, 5]) == 5
    assert total([1, 2, 3, 4, 5]) == 15
    assert mean([1, 2, 3, 4, 5]) == 3.0
    assert median([1, 2, 3, 4, 5]) == 3.0
    assert median([1, 2, 3, 4]) == 2.5  # even length
    assert mode([1, 2, 2, 3]) == [2]
    assert mode([1, 1, 2, 2, 3]) == [1, 2]  # tie — return both
    assert variance([2, 4, 4, 4, 5, 5, 7, 9]) == 4.0
    assert abs(stddev([2, 4, 4, 4, 5, 5, 7, 9]) - 2.0) < 1e-9

    # Single element
    assert median([7]) == 7
    assert variance([7]) == 0.0
    assert stddev([7]) == 0.0

    # Floats
    assert abs(mean([1.5, 2.5, 3.5]) - 2.5) < 1e-9

    # summary() dict
    s = summary([1, 2, 3, 4, 5])
    assert s["count"] == 5
    assert s["sum"] == 15
    assert s["mean"] == 3.0
    assert s["median"] == 3.0
    assert s["mode"] == [1, 2, 3, 4, 5]  # all unique → all tie
    assert s["var"] == 2.0
    assert abs(s["stddev"] - math.sqrt(2.0)) < 1e-9

    # Empty list raises
    for fn in (count, total, mean, median, mode, variance, stddev, summary):
        try:
            fn([])
        except ValueError:
            pass
        else:
            raise AssertionError(f"{fn.__name__}([]) should raise ValueError")

    print("All tests passed.")

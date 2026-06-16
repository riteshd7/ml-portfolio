# Day 1 — Refactor Notes

Your code already works — all four exercises pass. These aren't bug fixes. They're
"same result, cleaner code" tweaks. Each one is a habit that pays off all month.

## 1. `count()` — delete code that does nothing

Your version:

```python
def count(nums):
    i = 0                    # ALTLOGIC
    for element in nums:
        i += 1
    length = len(nums)       # LOGIC
    if not nums:
        raise ValueError("Cannot process an empty list")
    return len(nums)
```

The loop counts into `i`, and `length` gets set — but you never use either. You return
`len(nums)` anyway. Two fixes: **delete the dead lines**, and **check for empty first**
(do the guard before any work):

```python
def count(nums):
    if not nums:
        raise ValueError("Cannot process an empty list")
    return len(nums)
```

Habit: if a variable is never read again, it shouldn't exist.

## 2. `variance()` — don't recompute the same thing in a loop

Your version calls `mean(nums)` *inside* the loop:

```python
    for element in nums:
        diff = element - mean(nums)   # mean() runs again every single time
```

If the list has 1,000 numbers, you compute the mean 1,000 times — same answer each time.
Compute it **once, before the loop**:

```python
def variance(nums):
    if not nums:
        raise ValueError("Cannot process an empty list")
    m = mean(nums)                      # once
    return mean([(x - m) ** 2 for x in nums])
```

Habit: if a value doesn't change inside a loop, calculate it above the loop.

## 3. `summary()` — be consistent, and fill the dict the simple way

Two small things. First, you wrote a `total()` function but then used Python's built-in
`sum()` here instead — pick one (use your own `total()` so the file is consistent).
Second, `dict.update({...})` seven times is the long way round; just assign keys directly:

```python
def summary(nums):
    if not nums:
        raise ValueError("Cannot process an empty list")
    return {
        "count":  count(nums),
        "sum":    total(nums),     # your own function, not built-in sum()
        "mean":   mean(nums),
        "median": median(nums),
        "mode":   mode(nums),
        "var":    variance(nums),
        "stddev": stddev(nums),
    }
```

Habit: `d["key"] = value` (or a dict literal) is the normal way; reach for `.update()`
only when merging two dicts.

## 4. `check_password()` — you don't need the special empty-string block

You added a whole separate branch for `password == ""`. But walk through it: an empty
string already fails all 5 rules in your normal code (no length, no lowercase, etc.), so
it *already* returns score 0, "weak", and all 5 issues. The special case just repeats
what the main logic does. **Delete the `if password == "":` block** and let the normal
path handle it — fewer lines, one less place for the two versions to drift apart.

Habit: before writing a special case, check whether your general code already handles it.

---

One general note: clear out leftover scratch markers (`# ALTLOGIC`, `# LOGIC`, `# HINT`)
before you commit — they're notes-to-self, not part of the solution.

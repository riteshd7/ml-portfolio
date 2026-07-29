# Day 3b — Building a package from an empty directory

> Week 1 · Python fluency, blank-editor reps · **Day 3b of 30** · Second half of Day 3

---

## Why today exists

Yesterday you split an existing file into modules. That's the easy direction — the code already worked, and you were reorganizing it. Today you start from an empty directory and design the split *before* the code exists. That's harder and much more common: every project you ever start begins here.

Two things are being trained today:

1. **Package design under uncertainty.** You'll build three modules that convert units. Two of them share an interface naturally. The third can't, and you'll have to decide what the common contract actually is. That decision is the whole exercise — the arithmetic is trivial.
2. **Writing the test before the implementation.** Day 3a's debrief noted that your Day 2 practice tests came from an LLM after the fact, and in `strip_comments.py` the generated assertion was right while the code was wrong. Today the tests come first, from you. If you can't state what "correct" means before writing the function, you don't understand the problem yet.

---

## What you'll be able to do by EOD

- Design a package layout before writing implementation code
- Explain why `length` and `weight` share an interface but `temperature` can't
- Diagnose `ImportError`, `ModuleNotFoundError`, and circular imports from the traceback alone
- Predict what `sys.path` contains and how it changes with `-m` vs direct execution
- Write assertions that encode a spec, chosen for the bugs they'd catch
- Expose a clean public API from `__init__.py` using `__all__`

---

## Today's schedule (target: 6.5 hours)

| Block | Time | What |
|-------|------|------|
| Warm-up | 30 min | Re-read the Day 3a primer sections 2–4. No new reading today. |
| Practice | 90 min | Six import-mechanics drills — break things deliberately |
| Build | 3.5 hrs | `unit_converter` package from an empty directory |
| Wrap up | 30 min | Self-assessment, PR with pasted output, merge |

Note there's no lecture block. Day 1–3a were 60–90 minutes of reading each. From here the ratio shifts toward building — by week 3 the curriculum is 80% build, and this is the transition.

### Pre-flight

```bash
cd ~/Projects/ml-portfolio
source .venv/bin/activate
git checkout main && git pull          # 3a must be merged before you start
git checkout -b day-03b-unit-converter
python -m cli.notes list               # 3a's work still runs. Confirm before building on it.
```

---

## Practice (90 min) — Six import drills

Create `week1/practice/day03/` and work through these. Each one is: **predict the outcome in writing, then run it, then explain any gap.** Keep your predictions in `week1/practice/day03/PREDICTIONS.md` — including the ones you got wrong. Especially those.

The point isn't to memorize import rules. It's that when you hit an `ImportError` in month four on a real codebase, you diagnose it from the traceback in thirty seconds instead of randomly adding `__init__.py` files until something works.

### Drill 1 — `sys.path` under three invocations (15 min)

```python
# week1/practice/day03/drill1/show_path.py
import sys
print("argv[0]:", sys.argv[0])
print("sys.path[0]:", sys.path[0])
```

Predict `sys.path[0]` for each, then run all three from the repo root:

```bash
python week1/practice/day03/drill1/show_path.py
cd week1/practice/day03/drill1 && python show_path.py; cd -
python -m week1.practice.day03.drill1.show_path     # will this even work?
```

The third one may fail. If it does, the error message is the lesson — write down what it tells you about what `-m` requires.

### Drill 2 — Relative import, both ways (10 min)

```
drill2/
├── __init__.py
├── helper.py        # def greet(): return "hi from helper"
└── main.py          # from .helper import greet; print(greet())
```

```bash
python week1/practice/day03/drill2/main.py               # predict
python -m week1.practice.day03.drill2.main               # predict
```

One works, one doesn't. Explain *why* in one sentence, using the phrase "parent package."

### Drill 3 — Build a circular import on purpose (15 min)

```python
# drill3/a.py
from .b import b_thing
def a_thing(): return "A"

# drill3/b.py
from .a import a_thing
def b_thing(): return "B"
```

Run `python -m week1.practice.day03.drill3.a`. Read the traceback carefully — it names the *partially initialized* module. Then fix it three ways and note the trade-off of each in `PREDICTIONS.md`:

1. Move the shared thing into a third module `c.py`
2. Move one import inside the function body (lazy import)
3. Restructure so the dependency only points one direction

Option 3 is usually right in real code. Say why.

### Drill 4 — `__init__.py` vs `__main__.py` (10 min)

```python
# drill4/__init__.py
print("__init__ ran")

# drill4/__main__.py
print("__main__ ran")
```

Predict the output of each, then run:

```bash
python -m week1.practice.day03.drill4
python -c "import week1.practice.day03.drill4"
```

One prints one line, one prints two. Which, and why?

### Drill 5 — Module-level code runs once (10 min)

```python
# drill5/expensive.py
print("expensive.py is being executed")
VALUE = 42

# drill5/main.py
from .expensive import VALUE
from .expensive import VALUE          # again
import week1.practice.day03.drill5.expensive    # and again, absolute this time
print("done")
```

How many times does "expensive.py is being executed" print? Predict, run, then name the mechanism (one word — it's in the Day 3a primer, section 2, step 1).

### Drill 6 — LEGB, the Day 2 bug in miniature (30 min)

Write `drill6/scope.py` from a blank editor — no copying from the primer:

1. A function that shadows a global and proves the global is unchanged after
2. A closure where an inner function reads an enclosing local
3. A function that raises `UnboundLocalError`, plus a one-line comment on why it isn't `NameError`
4. **A two-function reproduction of your Day 2 bug:** `f()` defines a local, `g()` tries to read it, `f()` calls `g()`. Assert that `NameError` is raised.

```python
def test_day2_bug():
    def g():
        return args.text        # NameError — args is f's local
    def f():
        args = "whatever"       # noqa — deliberately unused
        return g()
    try:
        f()
    except NameError as e:
        print(f"Reproduced: {e}")
    else:
        raise AssertionError("expected NameError")
```

Type it yourself, run it, and confirm the message matches the one from Day 2. That's the whole point — you should be able to produce that bug on demand now, which means you can also see it coming.

```bash
git add week1/practice/day03/
git commit -m "day-03b: import mechanics drills with predictions"
```

---

## Build (3.5 hours) — `unit_converter`

### What you're building

A package converting between length, weight, and temperature units. Usable both as a library (`from unit_converter import convert`) and as a CLI (`python -m unit_converter 100 miles km`). At the repo root, next to `cli/`.

```
unit_converter/
├── __init__.py              # public API
├── __main__.py              # CLI: argparse, dispatch to convert()
├── length.py
├── weight.py
├── temperature.py
├── core.py                  # cross-category convert()
└── tests.py                 # smoke tests
```

### Order of work — tests first

**Write `tests.py` before any implementation.** It will fail with `ImportError` for the first hour. That's correct and expected; it's how you know the tests are real. Do not write the tests after the code and do not generate them.

### Step 1 — `tests.py` (30 min, first)

```python
"""Smoke tests for unit_converter — run with: python -m unit_converter.tests"""

from .core import convert, detect_category


def run():
    assert abs(convert(1, "mi", "km") - 1.609344) < 1e-9
    assert abs(convert(100, "c", "f") - 212.0) < 1e-9
    assert abs(convert(0, "c", "k") - 273.15) < 1e-9
    assert abs(convert(1, "kg", "g") - 1000.0) < 1e-9
    assert abs(convert(-40, "c", "f") - (-40.0)) < 1e-9
    assert detect_category("lb") == "weight"

    # Round-trip: value → other unit → back should be identity
    for a, b in [("mi", "ft"), ("cm", "in"), ("kg", "oz"), ("c", "f"), ("c", "k")]:
        assert abs(convert(convert(7, a, b), b, a) - 7) < 1e-9, f"round-trip failed: {a}/{b}"

    for bad in [("m", "kg"), ("c", "km"), ("m", "furlong")]:
        try:
            convert(1, *bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print("All conversion tests passed.")


if __name__ == "__main__":
    run()
```

Two of these are chosen for specific bugs. Work out which bug each catches before you continue — you'll be asked in the self-assessment:

- **`-40 c → f`.** Almost every other value passes even if you swap the C→F and F→C formulas, or use `9/5` where you meant `5/9`. −40 is the fixed point where the two scales agree, so it pins the formula down. Actually — think harder about that claim. Does −40 catch a swapped formula, or does it *fail* to? Test it both ways and write down what you find. The reasoning matters more than the answer.
- **Round-trip.** Catches a factor that's wrong *consistently* in both directions — where `to_meters` and `from_meters` share the same bad constant, so they cancel out. Ask yourself what round-trip *can't* catch, then add a test that covers that gap.

**Add two more cases of your own** and justify each in the PR description: what specific wrong implementation does it catch that nothing else here would?

```bash
git commit -m "day-03b: add unit_converter smoke tests (failing, no implementation yet)"
```

A commit of failing tests is a legitimate commit. It's a statement of intent.

### Step 2 — `length.py` (30 min)

```python
"""Length conversions. Internal representation: meters."""

# Conversion factors: how many meters is 1 of this unit?
FACTORS = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "mi": 1609.344,
    "miles": 1609.344,
    "yd": 0.9144,
    "ft": 0.3048,
    "in": 0.0254,
}

UNITS = set(FACTORS.keys())


def to_meters(value: float, unit: str) -> float:
    """Convert from `unit` to meters. Raise ValueError on unknown unit."""

def from_meters(value: float, unit: str) -> float:
    """Convert from meters to `unit`. Raise ValueError on unknown unit."""

def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between any two length units."""
```

`convert` should be two lines: to base, then from base. If it's longer, you're special-casing something you don't need to.

### Step 3 — `weight.py` (15 min)

Same shape, base unit grams. This should be fast — that's the point of a shared interface.

```python
FACTORS = {
    "g": 1.0,
    "kg": 1000.0,
    "mg": 0.001,
    "lb": 453.592,
    "oz": 28.3495,
    "tonne": 1_000_000.0,
}
```

### Step 4 — `temperature.py` (30 min)

Here's the interesting one. Temperatures don't scale, they translate — there's an offset, so a multiplication table can't express them.

```python
UNITS = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}

def to_celsius(value: float, unit: str) -> float: ...
def from_celsius(value: float, unit: str) -> float: ...
def convert(value: float, from_unit: str, to_unit: str) -> float: ...
```

- C → F: `(c * 9/5) + 32`
- F → C: `(f - 32) * 5/9`
- C → K: `c + 273.15`
- K → C: `k - 273.15`

**Notice what just happened to your design.** `length` and `weight` both expose `FACTORS`, `to_<base>`, `from_<base>`. `temperature` can't expose `FACTORS` at all. So `FACTORS` is *not* part of the contract — the only thing all three share is `UNITS` and `convert()`. That's the interface `core.py` gets to depend on, and nothing more.

This is the actual lesson of the day: **the shared interface is the intersection of what all implementations can provide, not the union of what's convenient.** Getting this wrong is how codebases end up with `if isinstance(x, Temperature)` scattered through them.

### Step 5 — `core.py` (45 min)

```python
from . import length, weight, temperature

CATEGORIES = {
    "length": length,
    "weight": weight,
    "temperature": temperature,
}


def detect_category(unit: str) -> str:
    """Return 'length', 'weight', or 'temperature' for a given unit.
    Raise ValueError if the unit is unknown."""

def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Detect the category, dispatch to that module's convert.
    Raise ValueError if from_unit and to_unit are different categories."""
```

`convert` must not know anything about meters, grams, or Celsius. It looks up two categories, compares them, and delegates. If `core.py` contains a single conversion constant, the abstraction leaked.

Error messages are part of the spec — `tests.py` only checks that `ValueError` is raised, but a user reads the text:
- `cannot convert length to weight`
- `unknown unit 'furlong'`

### Step 6 — `__main__.py` and `__init__.py` (30 min)

```python
import argparse
import sys

from .core import convert


def main():
    parser = argparse.ArgumentParser(prog="unit_converter")
    parser.add_argument("value", type=float)
    parser.add_argument("from_unit")
    parser.add_argument("to_unit")
    args = parser.parse_args()
    try:
        result = convert(args.value, args.from_unit, args.to_unit)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"{args.value} {args.from_unit} = {result:.4f} {args.to_unit}")


if __name__ == "__main__":
    main()
```

Compare that `print(..., file=sys.stderr)` against Day 2 defect #2 one more time. Type it correctly here.

```python
# __init__.py
from .core import convert, detect_category

__all__ = ["convert", "detect_category"]
```

`__all__` declares the public API: what `from unit_converter import *` exports, and a signal to readers that `length.FACTORS` is an internal detail they shouldn't reach into.

### Manual test sequence

```bash
$ python -m unit_converter 100 miles km
100.0 miles = 160.9344 km

$ python -m unit_converter 100 c f
100.0 c = 212.0000 f

$ python -m unit_converter 5 kg lb
5.0 kg = 11.0231 lb

$ python -m unit_converter 1 m kg
Error: cannot convert length to weight
$ echo $?
1

$ python -m unit_converter 1 m furlong
Error: unknown unit 'furlong'

$ python -m unit_converter.tests
All conversion tests passed.

$ python -c "from unit_converter import convert; print(convert(1, 'mi', 'km'))"
1.609344
```

Run every line. Paste the output into the PR.

### Commit cadence

```bash
git commit -m "day-03b: add length conversions to unit_converter"
git commit -m "day-03b: add weight conversions"
git commit -m "day-03b: add temperature with formula-based conversion"
git commit -m "day-03b: add core.detect_category and convert dispatcher"
git commit -m "day-03b: add CLI entry point and public API via __all__"
```

---

## Common pitfalls today

1. **Writing `tests.py` last.** If the tests never failed, they never tested anything. You'd be encoding the behavior you happened to implement, not the behavior you meant.
2. **Putting conversion logic in `core.py`.** If `core.py` mentions `1609.344`, the category modules aren't doing their job.
3. **`temperature.FACTORS`.** If you find yourself inventing one to make `core.py` uniform, stop — you're forcing an interface onto something that can't hold it. The uniform thing is `convert()`.
4. **Circular import between `core.py` and the category modules.** Categories must not import `core`. Dependencies point one direction: `__main__` → `core` → categories. Drill 3 was practice for exactly this.
5. **Float equality.** `assert convert(1, "mi", "km") == 1.609344` will bite you. Compare with a tolerance, which is why every assertion above uses `abs(a - b) < 1e-9`.
6. **Silent unit aliases.** `"mi"` and `"miles"` both map to the same factor. Make sure `detect_category` handles both, and decide whether unit names are case-sensitive — then make the code match the decision.

---

## Self-assessment

Answers in `week1/day-03b-answers.md`, committed.

1. Why can `length.py` and `weight.py` share an interface that `temperature.py` cannot? What *is* the shared interface, precisely?
2. In `core.convert`, why does the category check have to happen before dispatch rather than inside each module's `convert`?
3. What does `__all__` do? What breaks if you omit it?
4. Drill 5: how many times did the module body execute, and what mechanism causes that?
5. Drill 3: you fixed the circular import three ways. Which is right for real code, and why are the other two workarounds?
6. Does the `-40 c → f` assertion catch a swapped C↔F formula? Show your working — you tested this in step 1.
7. What can a round-trip test *not* catch? What did you add to cover it?

---

## Stretch (only if everything above is green)

- **Fourth category: currency.** Static FX table for INR/USD/EUR/GBP. Note in the README that rates are stale — a converter that silently returns stale money is worse than one that refuses.
- **`--help` examples.** argparse's `epilog` parameter puts usage examples below the help text.
- **Publish to TestPyPI.** `pyproject.toml`, `python -m build`, `twine upload --repository testpypi dist/*`, then `pip install` it into a fresh venv and import it. Seeing your own code arrive via `pip` is worth the hour.

---

## Anti-stall guardrails

**Failure mode #1: designing `core.py` before writing any category module.**
You can't design the shared interface until you've seen the one that doesn't fit. Write `length.py` and `temperature.py` first, *then* look at what they have in common. Bottom-up, not top-down, when the abstraction isn't obvious yet.

**Failure mode #2: the tests fail for an hour and it feels like failure.**
It isn't. Red tests with no implementation is the correct state at 11am. The failure mode to worry about is green tests you never saw fail.

**Failure mode #3: perfecting unit coverage.**
Nine length units is plenty. Adding nautical miles and furlongs is not learning, it's typing.

**Failure mode #4: the last edit, again.**
Day 2's bug was in the final change before commit. Before every `git commit` today: `python -m unit_converter.tests`. It takes half a second.

---

## Deliverable checklist

Practice:
- [ ] `week1/practice/day03/` with all six drills
- [ ] `PREDICTIONS.md` with a written prediction *and* actual outcome for each — including the misses
- [ ] Drill 6 reproduces the Day 2 `NameError` and asserts on it

Build:
- [ ] `unit_converter/` with 6 modules + `tests.py` at the repo root
- [ ] `tests.py` committed **before** any implementation module
- [ ] Two extra test cases of your own, each justified in the PR
- [ ] `python -m unit_converter 100 miles km` works
- [ ] `python -m unit_converter 1 m kg` → clean stderr message, exit 1
- [ ] `python -m unit_converter 1 m furlong` → unknown-unit message
- [ ] `python -m unit_converter.tests` prints "All conversion tests passed."
- [ ] `python -c "from unit_converter import convert; print(convert(1,'mi','km'))"` works
- [ ] `core.py` contains zero conversion constants

Process:
- [ ] `week1/day-03b-answers.md` with all 7 answers
- [ ] ≥8 commits on `day-03b-unit-converter`, all prefixed `day-03b:`
- [ ] **PR with the manual test sequence output pasted into the description**, merged to `main`
- [ ] Day 3a's CLI still works after the merge — `python -m cli.notes list`

---

## Done when

```bash
python -m unit_converter 100 miles km
python -m unit_converter 1 m kg; echo "exit: $?"
python -m unit_converter.tests
python -c "from unit_converter import convert; print(convert(100, 'c', 'f'))"
python -m cli.notes list                 # 3a still green
```

All clean, and you ran them. You've gone from "writes scripts" to "writes packages," and — more to the point — from "writes code" to "verifies code." Tomorrow: classes, and Day 1's inventory exercise becomes something you can defend.

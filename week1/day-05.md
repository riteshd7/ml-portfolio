# Day 5 — pytest, debugging with pdb, reading tracebacks

> Week 1 · Python fluency, blank-editor reps · **Day 5 of 30**

---

## Why today exists

So far you've used `assert` statements inside `if __name__ == "__main__":` blocks to test your code. That works for small files but breaks down for real projects: assertions run sequentially, the first failure halts the rest, and you lose visibility into which scenarios pass.

Today you graduate to `pytest`, the de facto testing framework for Python. You'll also learn `pdb`, the standard library debugger. Together these are the difference between hoping your code is right and *knowing* it is.

The deeper skill today is **reading tracebacks** — the multi-line error messages Python prints when something fails. 80% of beginner debugging time is spent because they didn't read the traceback. By tonight you'll diagnose most bugs in 30 seconds from the traceback alone.

---

## What you'll be able to do by EOD

- Write `pytest` tests with proper naming and discovery
- Use fixtures, parametrize, and `pytest.raises` to write idiomatic tests
- Run a coverage report and interpret it
- Drop into `pdb` to inspect a running program's state
- Set breakpoints with `breakpoint()` and navigate with `n`, `s`, `c`, `p`, `l`
- Read a multi-frame traceback and identify the exact line where the bug originated
- Stop using `print()` as a debugging tool

---

## Today's schedule (target: 6.5 hours)

| Block | Time | What |
|-------|------|------|
| Morning concept | 60 min | Read the concept primer below |
| Practice | 2 hrs | Convert previous days' tests to pytest |
| Build | 3 hrs | Plant 3 deliberate bugs, find them with pdb |
| Wrap up | 30 min | DEBUG_LOG.md + commit + push |

---

## Concept primer (60 min)

### 1. Why `assert` blocks aren't enough (5 min)

```python
if __name__ == "__main__":
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(1.5, 2.5) == 4.0
```

Problems with this style:
- First failure halts execution — you don't learn what else broke
- No isolation — tests share module state
- No structured output — you can't see "5 passed, 2 failed"
- No fixtures — setup/teardown has to be manual
- No parameterization — repetitive cases are copy-paste

`pytest` solves all of these.

### 2. pytest discovery rules (5 min)

`pytest` finds tests by convention:

- Files named `test_*.py` or `*_test.py`
- Inside those files, functions named `test_*`
- Classes named `Test*` containing `test_*` methods (you'll rarely use this — favor functions)

Recommended layout:
```
ml-portfolio/
├── cli/
│   └── notes/
│       ├── storage.py
│       └── commands.py
├── tests/
│   ├── __init__.py            # often empty; signals "package"
│   ├── test_storage.py
│   └── test_commands.py
└── pyproject.toml             # or pytest.ini for config
```

Run all tests:
```bash
pytest
pytest -v               # verbose: show each test name
pytest tests/test_storage.py    # one file
pytest tests/test_storage.py::test_load_returns_empty_when_missing   # one test
pytest -k "storage"     # all tests matching pattern
pytest -x               # stop after first failure
```

### 3. Anatomy of a pytest test (10 min)

```python
# tests/test_storage.py

from cli.notes.storage import load_notes, save_notes


def test_load_returns_empty_list_when_file_missing(tmp_path):
    """Loading from a non-existent file yields []."""
    fake = tmp_path / "no_such_file.json"
    assert load_notes(fake) == []


def test_save_and_load_roundtrip(tmp_path):
    """What we save is what we load."""
    notes = [{"id": 1, "text": "hi", "done": False, "created": "2026-05-02"}]
    path = tmp_path / "notes.json"
    save_notes(path, notes)
    assert load_notes(path) == notes
```

Notes:
- Test names should describe the *behavior being verified*, not the function being tested. `test_load_returns_empty_list_when_file_missing` >> `test_load_notes`.
- One assertion per test is the ideal but not a rule — group closely-related assertions.
- `tmp_path` is a built-in fixture giving you a unique temp directory per test, auto-cleaned.

### 4. Fixtures (10 min)

A fixture is a function that produces data or sets up state for tests. Other tests can request it by including its name as a parameter.

```python
import pytest

@pytest.fixture
def sample_notes():
    return [
        {"id": 1, "text": "buy milk", "done": False, "created": "2026-05-02"},
        {"id": 2, "text": "call dentist", "done": True, "created": "2026-05-02"},
    ]


def test_count_done(sample_notes):
    done_count = sum(1 for n in sample_notes if n["done"])
    assert done_count == 1


def test_extract_texts(sample_notes):
    texts = [n["text"] for n in sample_notes]
    assert "buy milk" in texts
```

Built-in fixtures you'll use:
- `tmp_path` — a `Path` to a unique temp directory (cleaned up automatically)
- `monkeypatch` — set environment variables, patch attributes for one test
- `capsys` — capture stdout/stderr from the code under test

### 5. `pytest.raises` — testing for exceptions (5 min)

To verify code raises an expected exception:

```python
import pytest
from cli.notes.exceptions import NoteNotFoundError


def test_done_on_missing_id_raises():
    with pytest.raises(NoteNotFoundError):
        cmd_done(99)


def test_error_message_contains_id():
    with pytest.raises(NoteNotFoundError, match="99"):
        cmd_done(99)
```

`match=` accepts a regex; the exception message is checked against it.

### 6. Parametrize — one test, many cases (10 min)

```python
import pytest

@pytest.mark.parametrize("password,expected_score", [
    ("",            0),
    ("hello",       2),
    ("Hello123",    4),
    ("Hello123!",   5),
    ("Ab1!",        4),
])
def test_password_score(password, expected_score):
    assert check_password(password)["score"] == expected_score
```

Output:
```
test_password_score[-0]   PASSED
test_password_score[hello-2]   PASSED
test_password_score[Hello123-4]  PASSED
...
```

You get one test per row. If row 3 fails, the others still run. **Parametrize liberally** — it's the highest-leverage pytest feature.

### 7. Coverage (5 min)

`pytest --cov` reports what fraction of your code was actually executed during tests. Install the plugin:

```bash
pip install pytest-cov
```

Run:
```bash
pytest --cov=cli/notes --cov-report=term-missing
```

Output:
```
Name                       Stmts   Miss  Cover   Missing
-----------------------------------------------------------
cli/notes/commands.py         40      4    90%   23-26
cli/notes/storage.py          22      0   100%
```

The "Missing" column shows the lines that never ran. Those are your gaps.

**Coverage caveat:** 100% coverage doesn't mean correct. It means every line ran at least once. A test that calls a buggy function but doesn't check the result will give 100% coverage and miss the bug. **Coverage is a floor, not a ceiling.**

For today, target **70% on `cli/notes/`**. Don't chase 100% — diminishing returns.

### 8. The `pdb` debugger (10 min)

`pdb` is Python's standard library debugger. It pauses execution wherever you tell it to and gives you a REPL with full access to local variables and the call stack.

#### Setting a breakpoint

```python
def cmd_done(notes_file, note_id):
    notes = load_notes(notes_file)
    breakpoint()                    # execution pauses here
    for note in notes:
        if note["id"] == note_id:
            note["done"] = True
            ...
```

`breakpoint()` is a Python builtin (since 3.7). It drops you into pdb. (You can also use `import pdb; pdb.set_trace()` — same effect, older syntax.)

When pdb is active, your terminal becomes interactive:

```
(Pdb)
```

#### Essential pdb commands

| Command | Meaning |
|---------|---------|
| `n` | Next line (step over function calls) |
| `s` | Step into function call |
| `c` | Continue until next breakpoint or end |
| `q` | Quit (kills the program) |
| `l` | List source around current line |
| `ll` | List the entire current function |
| `p <expr>` | Print the value of an expression |
| `pp <expr>` | Pretty-print |
| `b 42` | Set a breakpoint at line 42 of current file |
| `b somefile.py:42` | Set breakpoint in another file |
| `cl` | Clear all breakpoints |
| `w` | Where (show stack trace and current frame) |
| `u` | Up one frame (move toward caller) |
| `d` | Down one frame |
| `<Enter>` | Repeat last command |

#### A typical session

```
$ python -m cli.notes done 99
> /path/to/commands.py(40)cmd_done()
-> for note in notes:
(Pdb) p notes
[{'id': 1, 'text': 'hi', 'done': False, ...}]
(Pdb) p note_id
99
(Pdb) p type(note_id)
<class 'int'>
(Pdb) c
... rest of program runs
```

#### When NOT to use `print()`

Replacing `print(x)` with `breakpoint()` + `p x` is almost always better:
- `print` requires editing the code, running, reading output, editing the code again to remove the print
- `pdb` lets you *also* inspect every other variable in scope, not just the one you predicted you'd want
- `pdb` lets you climb the call stack to see *who called this function*

`print()` for debugging is a code smell. The exception is when the code runs in a context where pdb can't be used (like a server in production, or a worker process).

### 9. Reading a traceback (10 min)

A traceback is the multi-line error output Python prints when an unhandled exception bubbles up. **Read it bottom-up.**

```
Traceback (most recent call last):
  File "/Users/foo/cli/notes/__main__.py", line 12, in <module>
    main()
  File "/Users/foo/cli/notes/cli.py", line 45, in main
    cmd_done(NOTES_FILE, args.note_id)
  File "/Users/foo/cli/notes/commands.py", line 38, in cmd_done
    note["dnoe"] = True
KeyError: 'dnoe'
```

How to read:
1. **Bottom line** is the actual error: `KeyError: 'dnoe'`
2. **Line above** is *where* it happened: `commands.py:38`, the assignment `note["dnoe"] = True`
3. **Above that** is the call stack, showing how we got there

In this example, the bug is a typo: `dnoe` instead of `done`. The fix is one character.

Many beginners panic at the long output and miss the obvious answer at the bottom. **Read bottom-up. The bottom line names the problem.**

#### Common error types

- `NameError: name 'x' is not defined` — typo or missing import
- `TypeError: 'NoneType' object is not subscriptable` — you're indexing `None`; some function returned `None` when you expected a value
- `KeyError: 'foo'` — dict access for a missing key; use `.get()` or check
- `IndexError: list index out of range` — off-by-one or empty list
- `AttributeError: 'X' object has no attribute 'y'` — typo, OR object isn't what you think (often `None`)
- `ValueError` — value of right type but wrong content (e.g. `int("hello")`)

---

## Pre-flight check

```bash
cd ~/Projects/ml-portfolio
source .venv/bin/activate
git status                    # clean
git checkout main && git pull
git checkout -b day-05-testing

# Install pytest + coverage
pip install pytest pytest-cov
pip freeze | grep -E "pytest|coverage" >> requirements.txt
# (Or manually edit requirements.txt to add: pytest>=8.0 and pytest-cov>=5.0)
```

Verify:
```bash
pytest --version
pytest --collect-only       # should find no tests yet (folder doesn't exist)
```

---

## Practice (2 hours) — Real pytest tests for prior code

### Setup

```bash
mkdir -p tests
touch tests/__init__.py
```

Add to `pyproject.toml` at the repo root (create if missing):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

This tells pytest where to look.

### Task 1 — Write `tests/test_notes_storage.py` (40 min)

Write at least 6 test functions covering:

- [ ] `test_load_returns_empty_list_when_file_missing` (use `tmp_path`)
- [ ] `test_load_returns_empty_list_when_file_is_empty` — **this one will fail first, and
      that's the point.** An empty file isn't valid JSON, so `json.load` raises. Decide what
      the right behaviour is (an empty file and a missing file mean the same thing to a user)
      and change `load_notes` to match. Then the test passes. Expect to edit the code here.
- [ ] `test_load_raises_on_corrupt_json` (write `"{{not json"`) — **expect whichever exception
      your `storage.py` actually raises.** If you took the Day 3a review note and replaced the
      `sys.exit(1)` with a `CorruptNotesError`, expect that. If `storage.py` still calls
      `sys.exit`, this test can't be written at all: `sys.exit` raises `SystemExit` and kills
      the test run. That's the concrete cost of exiting from a library, and fixing it is part
      of today.
- [ ] `test_save_and_load_roundtrip`
- [ ] `test_save_creates_parent_directory_if_needed` (only if your impl supports it; otherwise mark `@pytest.mark.xfail`)
- [ ] `test_next_id_returns_one_when_empty`
- [ ] `test_next_id_returns_max_plus_one`

Two of these force changes to `storage.py`. That's normal and good: **writing tests is how
you find out your error handling was designed for one caller only.**

Run:
```bash
pytest tests/test_notes_storage.py -v
```

All green? Commit:
```bash
git add tests/test_notes_storage.py pyproject.toml
git commit -m "day-05: add pytest tests for notes storage"
```

### Task 2 — Write `tests/test_unit_converter.py` (40 min)

Use parametrize for multiple conversion cases:

```python
import pytest
from unit_converter import convert


@pytest.mark.parametrize("value,from_unit,to_unit,expected", [
    (1, "mi", "km", 1.609344),
    (1000, "m", "km", 1.0),
    (100, "c", "f", 212.0),
    (32, "f", "c", 0.0),
    (0, "c", "k", 273.15),
    (1, "kg", "g", 1000.0),
    (1, "lb", "kg", 0.453592),
])
def test_convert_known_values(value, from_unit, to_unit, expected):
    assert abs(convert(value, from_unit, to_unit) - expected) < 1e-3


def test_unknown_unit_raises():
    with pytest.raises(ValueError):
        convert(1, "stones", "kg")


def test_cross_category_raises():
    with pytest.raises(ValueError):
        convert(1, "m", "kg")
```

Aim for at least 12 test cases (parametrize counts toward this — each row is a test).

### Task 3 — Run coverage (20 min)

```bash
pytest --cov=cli/notes --cov=unit_converter --cov-report=term-missing
```

Look at the "Missing" column. Pick the function with the worst coverage and add 2–3 tests to bring it up.

Target: **>70% on `cli/notes/`**.

Commit:
```bash
git commit -m "day-05: add unit_converter tests, raise coverage to 70%+"
```

### Task 4 — Convert one Day 1 exercise to pytest (20 min)

Pick `04_inventory_manager.py` (functional version). Create `tests/test_inventory_functional.py` and migrate 5 of the assertions in its `if __name__ == "__main__":` block to pytest tests. **Don't delete the original file's assertions** — keep both. Production code often has both quick smoke tests in `__main__` AND proper test files.

Commit:
```bash
git commit -m "day-05: migrate inventory assertions to pytest"
```

---

## Build session — Plant and find 3 deliberate bugs (3 hours)

This is the day's main exercise. You'll learn pdb by *needing* it, not by reading about it.

### Setup

Copy `week1/python/04b_inventory_class.py` to `week1/python/04b_inventory_class_buggy.py`.

```bash
cp week1/python/04b_inventory_class.py week1/python/04b_inventory_class_buggy.py
```

### Plant 3 bugs

In the buggy file, introduce these three changes WITHOUT looking at the original after you do:

**Bug 1 — Off-by-one or wrong comparison.** Change a `<=` to `<`, or a `+1` to `-1`, somewhere in `low_stock` or `update_qty`.

**Bug 2 — Wrong operator.** Change a `+` to `-`, or `*` to `/`, somewhere in `total_value`.

**Bug 3 — Missing return.** Pick one method that should return `self` and remove the `return self` line.

Save the file. **Don't write down what you changed.** Try to forget. Get coffee, walk around for 5 minutes.

### Find the bugs using ONLY pdb

1. **Run the file's existing tests:**
   ```bash
   python week1/python/04b_inventory_class_buggy.py
   ```
   You'll see an `AssertionError` — the first failed test points you somewhere in the spec.

2. **Reproduce the failure with `breakpoint()`.** Add `breakpoint()` ONE line before the failing assertion. Re-run.

3. **Inspect:** When pdb pauses, use `p`, `pp`, `l` to see what's happening. Look at intermediate values.

4. **Walk up the stack with `u`** to see where the wrong value originated.

5. **Form a hypothesis.** ("I think `total_value` is wrong.") Test it: `(Pdb) p inv.total_value` and compare to expected.

6. **Fix the bug.** Re-run tests. Repeat.

**The hard rule today: NO `print()` STATEMENTS.** Banned. Use `pdb` exclusively. If you find yourself adding `print(x)`, delete it and use `breakpoint()` instead.

### Document your debugging in `DEBUG_LOG.md`

Create `DEBUG_LOG.md` at the repo root. For each of the 3 bugs:

```markdown
## Bug 1

**Symptom:** `assert qtys == sorted(qtys)` failed.

**Hypothesis:** Maybe low_stock isn't sorting.

**pdb session:**
```
(Pdb) l
... showed me the function
(Pdb) p sorted(items, key=lambda x: x["qty"])
[correct order]
(Pdb) p items
[wrong order — same as input]
```

**Diagnosis:** I had `return items` instead of `return sorted(...)`.

**Fix:** added the sort.

**Time to find:** 4 minutes.
```

Each bug gets a similar entry. The goal is to **demonstrate** real pdb usage in writing — recruiters who see this in your repo will understand you can debug.

### Commit

```bash
git add week1/python/04b_inventory_class_buggy.py DEBUG_LOG.md
git commit -m "day-05: add buggy version of inventory + DEBUG_LOG documenting pdb sessions"
```

(The buggy file should be committed FIXED — i.e. the same as the working version, plus your DEBUG_LOG describing what was wrong before. Don't commit broken code.)

---

## Common pitfalls today

1. **`pytest` not finding your tests.** Causes:
   - File not named `test_*.py`
   - Function not prefixed with `test_`
   - Running pytest from the wrong directory (run from repo root)
   - Missing `__init__.py` in `tests/` (sometimes needed, sometimes not — try with first)

2. **Import errors when pytest runs but the script works.** pytest manipulates `sys.path` slightly differently. Add this to `pyproject.toml`:
   ```toml
   [tool.pytest.ini_options]
   pythonpath = ["."]
   ```

3. **`breakpoint()` doesn't pause.** You're running in an environment that overrides `PYTHONBREAKPOINT`. Try `import pdb; pdb.set_trace()` instead.

4. **You're stuck in pdb and can't get out.** Press `q` then Enter.

5. **Coverage shows 0% even though tests pass.** You're measuring the wrong path. `--cov=cli/notes` measures the package; `--cov=cli` measures more; `--cov=.` measures everything. Match it to your actual code path.

6. **Test passes locally but you "feel" it should fail.** Maybe it's testing the wrong thing. Read the assertion carefully. Add a `breakpoint()` before the assertion and inspect.

7. **Unintentionally testing implementation details.** A good test verifies behavior, not internals. `test_balance_after_deposit` is good. `test_history_attribute_is_a_list` is over-specified.

---

## Self-assessment

1. What's the difference between `n` and `s` in pdb?
2. What does `tmp_path` give you, and why is it better than hardcoding `/tmp/test.json`?
3. When would you use `@pytest.mark.parametrize` instead of writing 5 separate test functions?
4. Why is `print()` debugging worse than `pdb`?
5. In a traceback, where do you look first — top or bottom?
6. What does it mean if your coverage is 100% but you still have bugs?

---

## Stretch (only if you finish before 6 hours)

- Add a GitHub Actions workflow at `.github/workflows/test.yml` that runs `pytest` on every push and PR. (You'll do this on Day 12 anyway, but doing it today is great practice.)
- Pick one piece of your code that's currently untested and add a parametrized test with at least 6 cases.
- Read the pytest docs section on **fixtures with scope** (`scope="session"`, `scope="module"`). Try writing one.

---

## Anti-stall guardrails for today

**Failure mode #1: pytest config rabbit hole.**

You'll spend 90 minutes trying to make pytest discover tests. Stop. The minimal config in `pyproject.toml` shown above works. If pytest STILL can't find tests after that, it's almost certainly a `__init__.py` issue or you're running from the wrong directory.

**Failure mode #2: not actually using pdb.**

The instinct will be to add `print()` statements to debug the planted bugs. **Resist.** The whole point of the bug-planting exercise is to internalize that pdb is faster. The first 10 minutes will feel slower than print. By minute 30 it's faster. Push through.

**Failure mode #3: chasing 100% coverage.**

Coverage past ~75% has dramatically diminishing returns and starts encouraging brittle tests of implementation details. Stop at 70-80% on the most important modules. Move on.

---

## Deliverable checklist

- [ ] `tests/` folder with `__init__.py` and at least 3 test files
- [ ] At least 20 test functions total (parametrize rows count)
- [ ] All pass: `pytest -v` shows green
- [ ] Coverage on `cli/notes/` is >70%
- [ ] `pyproject.toml` with `[tool.pytest.ini_options]`
- [ ] `requirements.txt` includes `pytest` and `pytest-cov`
- [ ] `DEBUG_LOG.md` at repo root with 3 entries (one per planted bug)
- [ ] No `print()` statements added during debugging
- [ ] At least 7 commits today on `day-05-testing`
- [ ] Branch merged to `main`

---

## Done when

```bash
pytest --cov=cli/notes --cov=unit_converter --cov-report=term-missing
# all green; cli/notes coverage >= 70%

cat DEBUG_LOG.md       # 3 entries, each with real pdb commands
```

If yes: you've stepped from "code that seems to work" to "code I can prove works." Tomorrow is the standard library tour.

If not: commit partial work, note in DEBUG_LOG.md what's incomplete, and continue tomorrow morning.

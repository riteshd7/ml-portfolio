# Day 3a — Fix, then split: modules, imports, scope

> Week 1 · Python fluency, blank-editor reps · **Day 3a of 30** · Day 3 is split across 3a and 3b

---

## Day 2 debrief — read this first

Day 2 was not actually complete.

```
$ python3 -m cli.notes add "test"
Traceback (most recent call last):
  File ".../cli/notes/__main__.py", line 97, in build_parser
    if not args.text.strip():
           ^^^^
NameError: name 'args' is not defined
```

Line 97 sits in `build_parser()` and reads `args`, which is a local of `main()`. It is **unconditional** — not inside any `if args.command == ...` branch — so it fires during parser construction, before argparse has parsed anything. Every subcommand (`add`, `list`, `done`, `rm`) dies there. No input or environment makes it not fire.

Second case, same root cause: `week1/practice/day02/strip_comments.py` fails the assertion inside its own file.

### The precise diagnosis

Look at lines 97–98 next to lines 114–115. They're near-duplicates. The check in `main()` is correct and works. The copy in `build_parser()` is the broken one. That reads as: you wrote the validation correctly, tested it, then pasted it into a second place as a final edit and committed without re-running.

So this isn't "you never test your code." It's narrower and more common: **you don't re-run after the last edit.** The last edit is the one nobody tests, because it's small and it's obviously fine. That's exactly the edit that breaks things.

The fix is mechanical, not moral: **the last thing you do before `git commit` is run the acceptance sequence.** Not before the last edit. After it.

### The Day 2 defect list

| # | Issue | Where |
|---|-------|-------|
| 1 | `NameError` on every command | `__main__.py:97` |
| 2 | `print(f"Error: {e}, file = sys.stderr")` — `file=sys.stderr` is *inside* the f-string. Errors go to stdout, and the literal text `, file = sys.stderr` is shown to the user. | `__main__.py:128` |
| 3 | Empty-text validation duplicated: broken copy in `build_parser`, working one in `main`. Delete the broken one. | `__main__.py:97`, `114` |
| 4 | `status_char = "x" if note["done"] else ""` renders `[]`. Spec says `[ ]` — a space, so columns align. | `__main__.py:61` |
| 5 | `print(f"Removed note{note_id}")` — missing space. | `__main__.py:84` |
| 6 | Corrupt/empty JSON unhandled. Day 2 spec required "print error, exit code 1, don't lose user data." Currently raises a raw `JSONDecodeError` traceback at the user. | `__main__.py:15` |
| 7 | `json.dump(notes, f)` with no `indent=2` — unreadable when you open it to debug. | `__main__.py:26` |
| 8 | Two different error messages for the same failure class (`done` vs `rm`), one missing a space. Pick one format. | `__main__.py:74`, `87` |

### Process gaps

- Day 2 required **7 commits on a `day-02-notes-cli` branch, merged via PR**. Actual: **2 commits, no branch, straight to `main`.** Day 1 *did* use a branch and PR #1. This is a regression from your own established practice.
- `##CHECKING AND ASSERTIONS FROM CLAUDE` / `#ASSERTIONS FROM GEMINI` appear in the practice files. Generating tests as a check on your work is fine. Note what happened in `strip_comments.py` though: the generated assertion was **correct**, your implementation was **wrong**, and the file was committed anyway. The tool caught the bug. Nobody read the output.
- The package sits at `week1/cli/`, so `python -m cli.notes` only works from inside `week1/`. Both day specs show it running from the repo root. Fixed in Block 0.

**Day 2 was not wasted.** Nine of ten practice problems pass; `caesar.py` and `merge_alternating.py` are clean. The CLI's *design* is right — custom exception, subparsers, `next_id`, `pathlib`. The structure is sound and the verification habit is missing. That's the easier of the two problems to fix.

---

## Why today exists

Yesterday you *wrote* the `notes` CLI as one ~135-line file. Today you make it run, then learn what professionals do with that file: **split it into pieces with clear responsibilities**, each testable in isolation, importable, replaceable without rewriting everything.

That's the difference between a script and software. You'll also learn Python's package system — the rules that decide what `import x` actually does, and the source of most beginner `ImportError` panic.

---

## What you'll be able to do by EOD

- Get a broken CLI to green by reading a traceback, not by guessing
- Split a 135-line script into 4 focused modules without changing behavior
- Explain the difference between a module, a package, and a script
- Choose correctly between absolute and relative imports
- Write functions with no global state — every dependency passed in, every result returned
- Explain a `NameError` in terms of Python's LEGB scope rules

---

## Today's schedule (target: 6.5 hours)

| Block | Time | What |
|-------|------|------|
| Block 0 — remediation | 75 min | Fix Day 2. Non-negotiable, first thing. |
| Concept primer | 75 min | Read below |
| Practice | 2 hrs | Refactor the working CLI into 4 modules |
| Build | 1 hr | Add `--file` — prove the refactor was real |
| Wrap up | 45 min | Self-assessment, PR with pasted output, merge |

---

## Block 0 — Fix Day 2 (75 min)

### Pre-flight

```bash
cd ~/Projects/ml-portfolio
source .venv/bin/activate        # `python` isn't on PATH outside the venv
git checkout main && git pull
git checkout -b day-03a-fix-and-split
```

### Step 1 — Move the package to the repo root (10 min)

`cli/` is shipped software, not a daily exercise. Exercises live in `week1/`; packages live at the root, where `python -m` finds them from the project root.

```bash
git mv week1/cli cli
python -m cli.notes list          # run from the repo root now
```

It still crashes — you haven't fixed anything yet. But the crash should be the `NameError`, not `ModuleNotFoundError`. If you get `ModuleNotFoundError: No module named 'cli'`, you're in the wrong directory.

### Step 2 — Fix the 8 defects (35 min)

Work down the table. **Run the CLI after each fix.** Not after all eight — after each one. Building that loop is the actual assignment.

For defect #6 (corrupt JSON):

```python
def load_notes():
    if not NOTES_FILE.exists():
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {NOTES_FILE} is corrupt. Fix or delete it.", file=sys.stderr)
        sys.exit(1)
```

Note where `file=sys.stderr` goes — an argument to `print`, outside the f-string. Put that next to your line 128 until the difference is obvious.

Verify it:

```bash
echo "not json" > ~/.notes.json
python -m cli.notes list          # friendly error, exit 1, file untouched
rm ~/.notes.json
```

### Step 3 — Run the full Day 2 acceptance sequence (20 min)

Run it. Read every line. Compare character by character against the Day 2 spec.

```bash
rm -f ~/.notes.json
python -m cli.notes add "buy milk"          # Added note 1: buy milk
python -m cli.notes add "call dentist"      # Added note 2: call dentist
python -m cli.notes list                    # both, with [ ] — a space, not empty
python -m cli.notes done 1
python -m cli.notes list                    # note 1 shows [x]
python -m cli.notes rm 1                    # Removed note 1.
python -m cli.notes done 99; echo "exit: $?"   # error + exit: 1
python -m cli.notes add ""                  # rejected
python -m cli.notes done 2                  # run twice — both succeed (idempotent)
```

Then the check people fake:

```bash
python -m cli.notes done 99 2>/dev/null     # must print NOTHING
```

Anything printed means defect #2 isn't fixed.

### Step 4 — Fix `strip_comments.py` (10 min)

The assertion expects trailing whitespace stripped; your implementation doesn't strip it. Add `.rstrip()`, re-run. Then run all ten:

```bash
cd week1/practice/day02
for f in *.py; do python "$f" >/dev/null 2>&1 && echo "PASS $f" || echo "FAIL $f"; done
cd -
```

Ten PASS lines, or Block 0 isn't done.

```bash
git add -A
git commit -m "day-03a: move cli package to repo root"
git commit -m "day-03a: fix NameError in build_parser and stderr routing"
git commit -m "day-03a: handle corrupt notes.json, align list output with spec"
git commit -m "day-03a: fix strip_comments trailing whitespace"
```

---

## Concept primer (75 min)

### 1. Module vs package vs script (10 min)

- **Module**: a single `.py` file. `notes.py` is a module.
- **Package**: a folder containing `__init__.py`. The folder name is the package name; `.py` files inside are submodules.
- **Script**: a module you run directly. The same file can be both — that's what `if __name__ == "__main__":` is for.

```
my_project/                    # not a package (no __init__.py)
├── helpers.py                 # module (importable as `helpers`)
└── notes/                     # package (has __init__.py)
    ├── __init__.py
    ├── storage.py             # submodule (importable as `notes.storage`)
    └── commands.py
```

`__init__.py` can be empty. Its presence is what makes the folder a package.

### 2. Imports — what actually happens (15 min)

When Python sees `import x`:
1. Check `sys.modules` (in-memory cache). Already imported? Return that.
2. Search the directories in `sys.path` for `x.py` or `x/` (a folder with `__init__.py`).
3. Found? Execute the file top to bottom. Names defined become attributes of the module.
4. Cache the result in `sys.modules`.

`sys.path` is a list containing:
- the directory of the script you ran (or cwd in the REPL)
- your venv's `site-packages/`
- the standard library

Inspect it: `python -c "import sys; print(sys.path)"`. **This is exactly why moving `cli/` to the repo root changed which directory you can run from.** Connect those two facts before moving on — it's self-assessment question 7.

#### Three ways to import

```python
import json                    # json.dumps(...)
from json import dumps         # dumps(...)
from json import dumps as d    # d(...)
```

No functional difference, just style. Pick what makes the call site clearest. **Avoid `from json import *`** — pollutes the namespace, hides where names came from.

### 3. Absolute vs relative imports (15 min)

**Absolute** — full path from the top:
```python
# In cli/notes/commands.py:
from cli.notes.storage import load_notes
```

**Relative** — relative to the current package:
```python
from .storage import load_notes        # same package
from ..other_pkg import thing          # parent package
```

`.` means "the package this file is in." `..` means "the parent package."

Which to use:
- **Inside your own package**: relative. They survive renaming or moving the package.
- **Third-party code**: absolute.
- **Top-level scripts**: doesn't matter much; absolute is conventional.

#### The classic gotcha

Relative imports only work when the code runs as part of a package. `python cli/notes/commands.py` runs the file as a script with no parent package:

```
ImportError: attempted relative import with no known parent package
```

Fix: `python -m cli.notes.commands`. The `-m` flag sets up the package machinery.

### 4. Scope rules — LEGB (20 min)

Python resolves names in this order:

1. **L**ocal — defined in the current function
2. **E**nclosing — defined in an enclosing function (closures)
3. **G**lobal — defined at module top level
4. **B**uilt-in — `len`, `print`, `range`

```python
x = 10                          # global

def outer():
    x = 20                      # enclosing (relative to inner)
    def inner():
        x = 30                  # local
        print(x)                # 30 — local
    inner()
    print(x)                    # 20 — enclosing's local, NOT global

outer()
print(x)                        # 10 — global unchanged
```

**This is what your Day 2 `NameError` was.** `build_parser()` referenced `args`, a *local of `main()`*. Locals of one function are invisible inside another: not local (never assigned in `build_parser`), not enclosing (`build_parser` isn't nested inside `main`), not global (never assigned at module level), not built-in. All four scopes miss → `NameError`.

Spend the full 20 minutes here. When LEGB is genuinely internalized, that bug becomes unwriteable rather than merely fixed.

#### Modifying globals from a function

```python
counter = 0

def increment():
    counter += 1                # ERROR — Python treats `counter` as local

def increment_correct():
    global counter
    counter += 1                # works, but bad design
```

`global` works and is almost always a smell. **Pass the state in, return the new state.**

### 5. Function design — the "no global state" rule (15 min)

Bad — depends on a global:
```python
NOTES_FILE = "notes.json"

def add_note(text):
    with open(NOTES_FILE) as f: ...
```

Good — dependency explicit:
```python
def add_note(notes_file, text):
    with open(notes_file) as f: ...
```

Two reasons:
1. **Testability.** The good version takes a temp file: `add_note("/tmp/test.json", "hi")`. The bad version needs the global monkey-patched. Day 5 writes pytest tests against this CLI — skip this refactor and Day 5 doubles in difficulty.
2. **Reusability.** The good version serves many files; the bad version serves one. You'll prove this concretely in today's build block.

Limits: some things are genuinely global (logger, DB connection). Rule of thumb — if it's *data the function operates on*, pass it. If it's a *cross-cutting tool*, a global is fine.

---

## Practice (2 hours) — Refactor the `notes` CLI

### Target structure

```
cli/
├── __init__.py
└── notes/
    ├── __init__.py
    ├── __main__.py          # 3 lines + guard
    ├── cli.py               # build_parser, main
    ├── commands.py          # cmd_add, cmd_list, cmd_done, cmd_rm
    ├── storage.py           # load_notes, save_notes, next_id, NOTES_FILE
    └── exceptions.py        # NoteNotFoundError
```

### Rules

1. **No new functionality.** Behavior identical before and after. Features are the build block, an hour from now.
2. **No global state.** Every function takes its dependencies as arguments. `NOTES_FILE` lives in `storage.py` but is *passed into* commands, never read from a global inside one.
3. **Relative imports** inside the package: `from .storage import ...`.
4. **`__main__.py` is tiny:**
   ```python
   from .cli import main

   if __name__ == "__main__":
       main()
   ```

### Step-by-step

1. **Create the empty files:** `touch cli/notes/{cli,commands,storage,exceptions}.py`
2. **Move `NoteNotFoundError` → `exceptions.py`.** Import it back. **Run the CLI.**
3. **Move `load_notes`, `save_notes`, `next_id`, `NOTES_FILE` → `storage.py`,** taking `path` first:
   ```python
   def load_notes(path): ...
   def save_notes(path, notes): ...
   ```
   Update callers. **Run the CLI.**
4. **Move `cmd_*` → `commands.py`,** each taking `notes_file` first:
   ```python
   def cmd_add(notes_file, text):
       notes = load_notes(notes_file)
   ```
   **Run the CLI.**
5. **Move `build_parser` and `main` → `cli.py`.** `main` dispatches on `args.command`, passing `NOTES_FILE`. **Run the CLI.**
6. **Reduce `__main__.py` to the 3-line shim. Run the CLI.**
7. **Re-run the full Block 0 acceptance sequence.** Identical output.

That's six "run the CLI" instructions. They *are* the assignment. Running once at the end is how Day 2 happened.

```bash
git commit -m "day-03a: extract NoteNotFoundError to exceptions module"
git commit -m "day-03a: extract storage layer with path as explicit parameter"
git commit -m "day-03a: extract command functions, remove global NOTES_FILE access"
git commit -m "day-03a: extract parser and main into cli module"
```

### Acceptance test

```bash
rm -f ~/.notes.json
python -m cli.notes add "test"
python -m cli.notes list
python -m cli.notes done 1
python -m cli.notes rm 1
python -m cli.notes done 99 2>/dev/null; echo "exit: $?"
```

Byte-identical to Block 0, and the last line prints `exit: 1` with nothing before it. Any difference means the refactor is incomplete — `git diff` against your Block 0 commit.

---

## Build (1 hour) — Add `--file`, and prove the refactor was real

A refactor with no observable benefit is indistinguishable from moving code around. Here's the payoff, and it should take fifteen minutes now where it would have taken an hour yesterday.

Add a global `--file` option that overrides the notes file:

```bash
python -m cli.notes --file /tmp/work.json add "ship the PR"
python -m cli.notes --file /tmp/work.json list      # only work notes
python -m cli.notes list                            # personal notes, untouched
```

### Spec

- `--file PATH` on the **top-level** parser (before the subcommand), not on each subparser.
- Defaults to `NOTES_FILE` from `storage.py` when omitted.
- `main()` resolves it once: `notes_file = args.file or NOTES_FILE`, then passes it to whichever `cmd_*` runs.
- Every existing command keeps working unchanged when `--file` is absent.

### Why this is the test

If your refactor was real, this is a change in exactly one file (`cli.py`) plus one argparse line. `commands.py` and `storage.py` don't change at all — they already take the path as a parameter.

**If you find yourself editing `commands.py` or `storage.py` to make this work, the "no global state" rule wasn't actually followed.** Go back and finish step 3 and 4 properly. That's the real acceptance test for the refactor, and it's why this block exists.

### Verify

```bash
rm -f /tmp/work.json ~/.notes.json
python -m cli.notes add "personal note"
python -m cli.notes --file /tmp/work.json add "work note"
python -m cli.notes list                            # only "personal note"
python -m cli.notes --file /tmp/work.json list      # only "work note"
git diff --stat HEAD~1                              # cli.py should be the only module changed
```

```bash
git commit -m "day-03a: add --file override, enabled by parameterized storage"
```

---

## Common pitfalls today

1. **`ModuleNotFoundError: No module named 'cli'`** — wrong directory. Run from the repo root; that's why Block 0 moved the package there.
2. **`ImportError: attempted relative import with no known parent package`** — you ran `python cli/notes/__main__.py` instead of `python -m cli.notes`.
3. **Circular import.** `commands.py` imports `storage.py` and `storage.py` imports `commands.py` → "cannot import name X from partially initialized module." Fix: extract the shared code to a third module, or import inside the function body.
4. **Confusing `__init__.py` with `__main__.py`.** `__init__.py` runs when the package is *imported*; `__main__.py` runs on `python -m`. Different files, different events.
5. **Forgetting callers after a signature change.** `cmd_add` gains `notes_file` → every caller breaks. `grep -rn "cmd_add(" cli/` before moving on.
6. **Stale `__pycache__`.** Change not taking effect? `find . -name __pycache__ -exec rm -rf {} +`.

---

## Self-assessment

Answers in `week1/day-03a-answers.md`, committed. Short is fine; blank is not.

1. What's the difference between `import x` and `from x import y`? When does it matter?
2. Why does `from .storage import load_notes` fail as `python cli/notes/__main__.py` but succeed as `python -m cli.notes`?
3. What does `__init__.py` do? Can it be empty?
4. In LEGB, what does E stand for? Give an example.
5. **Using LEGB, explain precisely why `build_parser()` raised `NameError: name 'args' is not defined` when `args` was clearly defined in `main()`.** Name all four scopes and say what was in each.
6. Why did `--file` require changes in only one module? What would you have had to change if `NOTES_FILE` were still read globally inside `cmd_add`?
7. What's in `sys.path`, and why did moving `cli/` from `week1/` to the repo root change where you can run `python -m cli.notes` from?

---

## Anti-stall guardrails

**Failure mode #1: Block 0 and the refactor get mixed together.**
Block 0 fixes behavior and changes no structure. The refactor moves code and changes no behavior. Separate commits, so when something breaks you know which kind of change did it.

**Failure mode #2: the refactor breaks it and you can't find why.**
Tiny steps, run after each. If step 3 broke it and step 2 worked, that's ~20 lines of diff. `git diff` is the tool.

**Failure mode #3: two hours on the perfect import structure.**
There's no perfect structure for a 4-file package. Take the obvious split and stop. The insight comes from doing this five more times in this curriculum.

**Failure mode #4 (the real one): ticking a box for a command you didn't run.**
Every box below maps to a command. Run it, paste the output in the PR. Day 3b builds a new package; Day 4 refactors alongside this one; Day 5 writes tests against it. Broken foundations don't stay contained.

---

## Deliverable checklist

Block 0:
- [ ] `cli/` at repo root; `python -m cli.notes list` runs from the repo root
- [ ] All 8 Day 2 defects fixed
- [ ] Day 2 acceptance sequence matches spec output
- [ ] `python -m cli.notes done 99 2>/dev/null` prints nothing, exits 1
- [ ] All 10 `week1/practice/day02/` files exit 0

Refactor:
- [ ] `cli/notes/` split into `cli.py`, `commands.py`, `storage.py`, `exceptions.py`, `__main__.py`
- [ ] `__main__.py` is 3 lines plus the guard
- [ ] Relative imports inside the package
- [ ] No global state — `NOTES_FILE` passed to every command
- [ ] Acceptance output identical to pre-refactor

Build:
- [ ] `--file` works; two note files stay independent
- [ ] `git diff --stat` shows `cli.py` as the only module changed by it

Process:
- [ ] `week1/day-03a-answers.md` with all 7 answers
- [ ] ≥10 commits on `day-03a-fix-and-split`, all prefixed `day-03a:`
- [ ] **PR opened with acceptance-command output pasted into the description**, then merged to `main`

---

## Done when

```bash
python -m cli.notes add "test" && python -m cli.notes list
python -m cli.notes --file /tmp/work.json add "work" && python -m cli.notes --file /tmp/work.json list
python -m cli.notes done 99 2>/dev/null; echo "exit: $?"     # exit: 1, nothing above it
cd week1/practice/day02 && for f in *.py; do python "$f" >/dev/null || echo "FAIL $f"; done; cd -
```

All clean, and **you** ran them — that's the day. Tomorrow (3b) you build a package from an empty directory, where there's no working code to fall back on.

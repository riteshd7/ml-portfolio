# Day 2 — Strings, files, error handling, argparse

> Week 1 · Python fluency, blank-editor reps · **Day 2 of 30**

---

## Why today exists

Yesterday you wrote 4 exercises that lived inside one file each. Today you'll build something different: a real command-line tool with **persistent state on disk**. The `notes` CLI you finish today will let you run `notes add "buy milk"`, then close the terminal, come back tomorrow, and `notes list` will still show your note.

This introduces three skills that show up in every real program:

1. **Reading and writing files** — every database, model file, CSV, log, and config in your future career is just bytes-to-disk. Today's `notes.json` is the simplest possible version.
2. **Validating user input** — users will pass garbage to your code. Real programs detect garbage early and produce helpful errors instead of crashing on line 47.
3. **Building a CLI with `argparse`** — the standard library's command-line parser. Every Python tool worth shipping uses it (or a wrapper over it).

By Day 7 your `expense-tracker` capstone will use all three. Today is the foundation.

---

## What you'll be able to do by EOD

- Read and write JSON files in Python without crashing on missing/corrupt input
- Define and raise custom exceptions, and explain when to use them
- Build a multi-command CLI tool using `argparse`
- Distinguish between `EAFP` and `LBYL` error-handling styles and pick correctly
- Use `pathlib.Path` instead of string paths
- Write a script that another person could install and run from instructions in your README

---

## Today's schedule (target: 6.5 hours)

| Block | Time | What |
|-------|------|------|
| Morning concept | 90 min | Read the concept primer below |
| Practice | 2 hrs | 10 small string + file problems |
| Build | 3 hrs | The `notes` CLI |
| Wrap up | 30 min | Final commit + push |

---

## Concept primer (90 min reading)

### 1. String methods you actually use (15 min)

You'll use these constantly. Memorize them; don't re-google.

```python
s = "  Hello, World!  "

s.strip()          # "Hello, World!"          — remove leading/trailing whitespace
s.lower()          # "  hello, world!  "
s.upper()          # "  HELLO, WORLD!  "
s.replace(",", "") # "  Hello World!  "
s.split(",")       # ["  Hello", " World!  "]  — split on a delimiter
s.split()          # ["Hello,", "World!"]      — no arg splits on ANY whitespace
",".join(["a","b","c"])    # "a,b,c"          — opposite of split

s.startswith("  H")   # True
s.endswith("!  ")     # True
"world" in s.lower()  # True

s.find("World")       # 9        — index, or -1 if not found
s.count("l")          # 3

f"{name} is {age}"    # f-strings — preferred over .format() and %
```

**Common pitfall:** `s.replace(...)` returns a NEW string; it doesn't mutate. Strings are immutable in Python.

```python
s = "hello"
s.replace("h", "j")    # returns "jello"
print(s)               # "hello" — unchanged!

s = s.replace("h", "j")  # the assignment is what matters
```

### 2. File I/O — the modern way (15 min)

The right way to open a file is the `with` statement:

```python
with open("notes.json", "r", encoding="utf-8") as f:
    contents = f.read()
# file is automatically closed here, even if an error occurred
```

`with open(...) as f:` does two things:
- Opens the file
- Guarantees `f.close()` runs when the block exits (success or error)

**Why this matters:** without `with`, a forgotten `close()` leaks file handles. On Windows, an unclosed file can't be deleted by another process. The `with` statement makes leaks impossible.

#### Read modes

```python
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()              # whole file as one string

with open("file.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()           # list of strings (one per line, with \n)

with open("file.txt", "r", encoding="utf-8") as f:
    for line in f:                  # iterate line by line — best for big files
        process(line.strip())
```

#### Write modes

```python
with open("file.txt", "w", encoding="utf-8") as f:    # "w" = overwrite
    f.write("hello\n")

with open("file.txt", "a", encoding="utf-8") as f:    # "a" = append
    f.write("more\n")
```

**`"w"` overwrites without warning.** This is the #1 way to lose work. Always confirm the path before opening in `"w"`.

#### `pathlib.Path` — better than string paths

```python
from pathlib import Path

p = Path("data") / "notes.json"       # cross-platform path joining
p.exists()                             # True/False
p.parent.mkdir(parents=True, exist_ok=True)   # ensure parent dir
p.read_text(encoding="utf-8")          # shortcut for open + read
p.write_text("hello", encoding="utf-8") # shortcut for open + write
```

`Path` objects are usable anywhere a string path is expected. Use them.

### 3. JSON in Python (10 min)

JSON is the default data interchange format for everything: APIs, configs, your `notes.json` today.

```python
import json

# Python dict/list <-> JSON string
data = {"name": "Alice", "age": 30, "tags": ["python", "ml"]}

s = json.dumps(data)              # dict -> JSON string
s = json.dumps(data, indent=2)    # pretty-printed (use this for human-readable files)

parsed = json.loads(s)            # JSON string -> dict

# Read/write files directly
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    parsed = json.load(f)
```

Note: `json.dump` (no s) writes to a file. `json.dumps` (with s = "string") returns a string. Same for `load` vs `loads`. The s suffix means "string". Beginners conflate these.

**Edge cases:**
- An empty file is NOT valid JSON. Reading it raises `json.JSONDecodeError`. Handle this.
- Non-ASCII characters: `json.dump(..., ensure_ascii=False)` writes them as-is instead of `\uXXXX` escapes.

### 4. Errors and exceptions (20 min)

#### The two error-handling styles

**LBYL — Look Before You Leap:**
```python
if path.exists():
    contents = path.read_text()
else:
    contents = "{}"
```

**EAFP — Easier to Ask Forgiveness than Permission:**
```python
try:
    contents = path.read_text()
except FileNotFoundError:
    contents = "{}"
```

Python's culture prefers EAFP. Why? **Race conditions.** Between your `path.exists()` check and `path.read_text()` call, the file could be deleted by another process. EAFP handles the actual failure, not the hypothetical pre-check.

Use LBYL only when:
- The check is cheap and the operation is expensive
- You need to handle multiple cases without exceptions

#### Catching exceptions

```python
try:
    risky_operation()
except FileNotFoundError as e:
    print(f"file missing: {e}")
except json.JSONDecodeError as e:
    print(f"bad JSON: {e}")
except Exception as e:
    print(f"unexpected: {e}")
    raise   # re-raise so the program still fails loudly
```

**Anti-pattern: catching `Exception` and silently passing.** This hides bugs. If you catch a broad `Exception`, either log + re-raise, or have a damn good reason.

#### Custom exceptions

```python
class NoteNotFoundError(Exception):
    """Raised when a note with the given id doesn't exist."""

# Use it:
def delete_note(notes, note_id):
    if note_id not in notes:
        raise NoteNotFoundError(f"no note with id {note_id}")
    del notes[note_id]
```

**When to define a custom exception?** When callers might want to catch *your specific* error without catching unrelated ones. `KeyError` is too generic — code calling `delete_note` might catch it and think it's a different problem.

For tiny scripts, built-in exceptions (`ValueError`, `KeyError`, `FileNotFoundError`) are fine. For libraries, define your own.

### 5. `argparse` — the standard CLI library (20 min)

`argparse` parses command-line arguments. You define what arguments your program accepts; `argparse` handles parsing, type conversion, validation, and `--help` output for free.

#### Minimal example

```python
import argparse

parser = argparse.ArgumentParser(description="A simple greeter")
parser.add_argument("name", help="who to greet")
parser.add_argument("--loud", action="store_true", help="shout the greeting")

args = parser.parse_args()
greeting = f"Hello, {args.name}!"
if args.loud:
    greeting = greeting.upper()
print(greeting)
```

Run it:
```bash
$ python greet.py World
Hello, World!

$ python greet.py World --loud
HELLO, WORLD!

$ python greet.py --help     # argparse generates this for free
```

#### Subcommands (what you'll use today)

```python
parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command", required=True)

p_add = sub.add_parser("add", help="add a note")
p_add.add_argument("text")

p_list = sub.add_parser("list", help="list all notes")

p_done = sub.add_parser("done", help="mark a note done")
p_done.add_argument("note_id", type=int)

args = parser.parse_args()

if args.command == "add":
    add_note(args.text)
elif args.command == "list":
    list_notes()
elif args.command == "done":
    mark_done(args.note_id)
```

This gives you `python notes.py add "buy milk"`, `python notes.py list`, `python notes.py done 3`. Argparse handles `--help` for the top level AND each subcommand.

---

## Pre-flight check

```bash
cd ~/Projects/ml-portfolio
source .venv/bin/activate
git status                    # should be clean (yesterday's work merged)
git checkout main
git pull
git checkout -b day-02-notes-cli
```

If `git status` shows uncommitted changes from Day 1: commit or stash them first. Don't start Day 2 with a dirty tree.

---

## Practice (2 hours) — 10 small problems

Create `week1/practice/day02/` and one file per problem. Each file:
- Has a docstring describing the problem
- Implements the function(s)
- Has an `if __name__ == "__main__":` block with at least 3 assertions

**Rules: no LLM, no Stack Overflow first pass. Time-box each problem at 12 minutes; if you blow through, move on and return at the end.**

### Problem 1: `reverse_string.py` — Reverse without slicing

```python
def reverse(s: str) -> str:
    """Return s reversed, WITHOUT using s[::-1] or reversed()."""
    ...
```

Assertions:
```python
assert reverse("") == ""
assert reverse("a") == "a"
assert reverse("hello") == "olleh"
assert reverse("ab cd") == "dc ba"
```

### Problem 2: `palindrome.py` — Case-insensitive, ignoring non-alpha

```python
def is_palindrome(s: str) -> bool:
    """True if s reads the same forwards and backwards, ignoring case
    and non-alphabetic characters. Empty string is True."""
```

Assertions:
```python
assert is_palindrome("racecar")
assert is_palindrome("A man, a plan, a canal: Panama")
assert is_palindrome("")
assert not is_palindrome("hello")
assert is_palindrome("Was it a car or a cat I saw?")
```

### Problem 3: `count_vowels.py`

```python
def count_vowels(s: str) -> dict:
    """Return a dict mapping each vowel (a/e/i/o/u, lowercase) to its count.
    Vowels not present should NOT appear in the dict."""
```

Assertions:
```python
assert count_vowels("hello") == {"e": 1, "o": 1}
assert count_vowels("AaEe") == {"a": 2, "e": 2}
assert count_vowels("xyz") == {}
```

### Problem 4: `line_count.py`

```python
def line_count(filepath: str) -> int:
    """Return the number of lines in the file. Empty file returns 0."""
```

Test by writing a temp file in your assertions block:
```python
from pathlib import Path
tmp = Path("/tmp/lc_test.txt")
tmp.write_text("a\nb\nc\n")
assert line_count(str(tmp)) == 3
tmp.write_text("")
assert line_count(str(tmp)) == 0
```

### Problem 5: `word_count.py`

```python
def word_count(filepath: str) -> int:
    """Total word count in the file. Words = whitespace-separated."""
```

### Problem 6: `strip_comments.py`

```python
def strip_comments(filepath: str) -> str:
    """Read a Python file. Return its contents with full-line comments and
    trailing inline comments removed. Preserve blank lines.

    A 'comment' is anything from a # to end of line. Be careful: a # inside
    a string literal is NOT a comment. For today's exercise, you can ignore
    string literals (just strip everything from # onward)."""
```

### Problem 7: `longest_line.py`

```python
def longest_line(filepath: str) -> str:
    """Return the longest line in the file (trailing \\n stripped).
    On ties, return the FIRST one. Empty file returns ''."""
```

### Problem 8: `dedupe_lines.py`

```python
def dedupe_lines(input_path: str, output_path: str) -> int:
    """Read input, write each unique line to output ONCE, in order of
    first appearance. Return the number of lines written.

    Hint: a `set` for "seen" + a list for "order"."""
```

### Problem 9: `merge_alternating.py`

```python
def merge_alternating(path_a: str, path_b: str, output_path: str) -> None:
    """Merge two files line-by-line into output: line 1 of a, line 1 of b,
    line 2 of a, line 2 of b, ... If one file runs out, append the rest of
    the other."""
```

### Problem 10: `caesar.py`

```python
def caesar(text: str, shift: int) -> str:
    """Caesar cipher. Shift letters by `shift` positions (wrap a-z and A-Z).
    Non-letters pass through unchanged. Negative shift = decrypt."""
```

Assertions:
```python
assert caesar("abc", 1) == "bcd"
assert caesar("xyz", 1) == "yza"
assert caesar("Hello, World!", 13) == "Uryyb, Jbeyq!"  # ROT13
assert caesar("Uryyb, Jbeyq!", -13) == "Hello, World!"
```

After all 10 work, commit:
```bash
git add week1/practice/day02/
git commit -m "day-02: complete 10 string and file practice problems"
```

---

## Build session — `notes` CLI (3 hours)

### What you're building

A command-line tool that manages a list of personal notes, persisting them to JSON on disk between runs.

```bash
$ python -m cli.notes add "buy milk"
Added note 1: buy milk

$ python -m cli.notes add "call dentist"
Added note 2: call dentist

$ python -m cli.notes list
1. [ ] buy milk          (added 2026-05-02)
2. [ ] call dentist      (added 2026-05-02)

$ python -m cli.notes done 1
Marked note 1 as done.

$ python -m cli.notes list
1. [x] buy milk          (added 2026-05-02)
2. [ ] call dentist      (added 2026-05-02)

$ python -m cli.notes rm 1
Removed note 1.

$ python -m cli.notes done 99
Error: no note with id 99 (run `notes list` to see ids)
```

### Folder structure

```
cli/
├── __init__.py
└── notes/
    ├── __init__.py
    ├── __main__.py         # argparse + dispatch
    └── (storage logic in __main__.py is fine for today; Day 3 splits it)
```

`__main__.py` is special — it's what runs when you do `python -m cli.notes`. The `__init__.py` files (can be empty) mark these as Python packages.

### Spec

**Storage:** A JSON file at `~/.notes.json` (in the user's home directory, not the project). Format:

```json
[
    {
        "id": 1,
        "text": "buy milk",
        "done": false,
        "created": "2026-05-02"
    },
    {
        "id": 2,
        "text": "call dentist",
        "done": false,
        "created": "2026-05-02"
    }
]
```

**Commands:**

| Command | Args | Behavior |
|---------|------|----------|
| `add` | `text` (string) | Append a new note with auto-incremented id, today's date, `done: false`. Print confirmation. |
| `list` | (none) | Print all notes. Format: `{id}. [{x or space}] {text} (added {date})`. If empty, print `No notes yet.` |
| `done` | `id` (int) | Mark the note with that id as done. Error if id doesn't exist. |
| `rm` | `id` (int) | Remove the note with that id. Error if id doesn't exist. |

**Errors:** Use a custom exception `NoteNotFoundError`. Catch it at the top of `main()` and print a friendly message to stderr; exit with code 1.

**Edge cases:**
- File doesn't exist on first `list` → treat as empty list, don't crash
- File exists but is empty/corrupt JSON → print error, exit code 1, don't lose user data (fail safe)
- `add` with empty text → reject with error
- `done` on already-done note → succeed silently (idempotent)

### Implementation skeleton

Don't copy this verbatim — type it yourself, then fill in the TODOs.

```python
"""Notes CLI — a tiny command-line note manager."""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

NOTES_FILE = Path.home() / ".notes.json"


class NoteNotFoundError(Exception):
    """Raised when a referenced note id doesn't exist."""


def load_notes():
    """Read notes from disk. Return [] if file doesn't exist."""
    # TODO


def save_notes(notes):
    """Write notes to disk."""
    # TODO


def next_id(notes):
    """Return max existing id + 1, or 1 if empty."""
    # TODO


def cmd_add(text):
    # TODO: load, append, save, print confirmation


def cmd_list():
    # TODO: load, print each note formatted, or "No notes yet."


def cmd_done(note_id):
    # TODO: load, find by id (raise NoteNotFoundError if missing), set done=True, save


def cmd_rm(note_id):
    # TODO: load, filter out by id (raise NoteNotFoundError if missing), save


def build_parser():
    parser = argparse.ArgumentParser(prog="notes", description="A tiny note manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a note")
    p_add.add_argument("text", help="the note text")

    sub.add_parser("list", help="list all notes")

    p_done = sub.add_parser("done", help="mark a note done")
    p_done.add_argument("note_id", type=int)

    p_rm = sub.add_parser("rm", help="remove a note")
    p_rm.add_argument("note_id", type=int)

    return parser


def main():
    args = build_parser().parse_args()
    try:
        if args.command == "add":
            cmd_add(args.text)
        elif args.command == "list":
            cmd_list()
        elif args.command == "done":
            cmd_done(args.note_id)
        elif args.command == "rm":
            cmd_rm(args.note_id)
    except NoteNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### Testing the CLI manually

After implementing, run this exact sequence and verify the output matches:

```bash
rm -f ~/.notes.json   # start clean

python -m cli.notes list
# Expected: No notes yet.

python -m cli.notes add "buy milk"
python -m cli.notes add "call dentist"
python -m cli.notes list
# Expected: 2 notes listed

python -m cli.notes done 1
python -m cli.notes list
# Expected: note 1 shows [x], note 2 shows [ ]

python -m cli.notes done 99
# Expected: error message, exit code 1
echo $?       # should print 1

python -m cli.notes rm 2
python -m cli.notes list
# Expected: only note 1, marked done
```

### Add `argparse` validation

Reject empty text in `add`. After argparse, check:
```python
if not args.text.strip():
    parser.error("note text cannot be empty")    # argparse exits with proper error
```

### Commit your work

Don't wait until everything works to commit. Commit after each command:
```bash
git commit -m "day-02: implement notes add command with JSON persistence"
git commit -m "day-02: implement notes list with formatting"
git commit -m "day-02: implement notes done with error handling"
git commit -m "day-02: implement notes rm"
```

---

## Common pitfalls today

1. **`json.load(f)` on missing file → `FileNotFoundError`.** Wrap with `try/except FileNotFoundError` in `load_notes` and return `[]`.

2. **`json.load(f)` on empty file → `json.JSONDecodeError`.** This is a different exception than `FileNotFoundError`. Catch both, OR check `path.read_text().strip() == ""` before parsing.

3. **Forgetting `parents=True` on `mkdir`.** If `~/.notes.json` is in a folder that doesn't exist, `open(... "w")` will fail. For Day 2 we use `~/`, which always exists, so this is fine — but remember it for tomorrow.

4. **`date.today()` returns a `date` object, not a string.** Use `date.today().isoformat()` to get `"2026-05-02"`. JSON can't serialize `date` objects directly.

5. **Mutating the list while iterating.** In `cmd_rm`, build a NEW list with the filtered notes; don't `notes.remove(...)` while iterating.

6. **Treating `args.note_id` as a string.** Argparse's `type=int` already converts. If you forget that, `notes[note_id]` will silently fail to match.

7. **Running the script as `python cli/notes/__main__.py`** — this works but breaks relative imports later. Always use `python -m cli.notes`.

---

## Self-assessment

1. Why does `with open(...) as f:` exist? What does it guarantee?
2. What's the difference between `json.dumps` and `json.dump`?
3. When would you define a custom exception class instead of using `KeyError`?
4. What does `argparse`'s `add_subparsers(dest="command", required=True)` do?
5. In `EAFP`, why is it preferred over `LBYL` for file I/O specifically?
6. What's `__main__.py` and why do we use it instead of `notes.py`?

If 4+ of these stump you, re-read the relevant section before bed.

---

## Stretch (if you finish before 6 hours)

- Add a `--due YYYY-MM-DD` flag to `add` and show overdue notes in red in `list` (using ANSI escape codes)
- Add a `find <query>` subcommand that does case-insensitive substring search across note text
- Add a `clear-done` subcommand that removes all notes marked done

Each of these is ~30 minutes if your base implementation is clean.

---

## Anti-stall guardrails for today

**Failure mode #1: getting stuck on argparse subcommands and rage-quitting.**

- The skeleton above is enough to compile and run. If you get a confusing argparse error, copy the skeleton verbatim, get it running, then modify one piece at a time.

**Failure mode #2: spending 90 minutes on the 10 practice problems and skipping the CLI build.**

- Hard cap practice at 2 hours. The CLI is the day's main deliverable, not the practice. If problems 8–10 aren't done by hour 3, commit what works and start the CLI.

**Failure mode #3: refactoring `__main__.py` into 5 files because "it's getting messy".**

- Don't. Day 3 explicitly refactors this into `storage.py`/`commands.py`/`cli.py`. Today the goal is "one ugly working file." The discipline of Day 3 is what teaches modular design — premature splitting today robs you of that lesson.

---

## Deliverable checklist

- [ ] `week1/practice/day02/` with 10 files, all running and asserting correctly
- [ ] `cli/__init__.py` (empty)
- [ ] `cli/notes/__init__.py` (empty)
- [ ] `cli/notes/__main__.py` with all 4 commands working
- [ ] Manual test sequence above produces expected output
- [ ] Custom `NoteNotFoundError` defined and used
- [ ] At least 7 commits on `day-02-notes-cli` branch with `day-02:` prefix
- [ ] Branch merged to `main` and pushed
- [ ] One green square on contribution graph today

---

## Done when

```bash
# These commands all work and behave per the spec:
python -m cli.notes add "test"
python -m cli.notes list
python -m cli.notes done 1
python -m cli.notes rm 1
python -m cli.notes done 99    # prints error, exits 1

# All 10 practice files run cleanly:
for f in week1/practice/day02/*.py; do echo "$f"; python "$f"; done
```

If yes: you've shipped your first stateful CLI. Tomorrow you'll refactor it into modules.

If not: commit partial work. Note in `DAY02_LOG.md` which commands work and which don't. Continue tomorrow morning before starting Day 3 — but don't burn past 8 hours today.

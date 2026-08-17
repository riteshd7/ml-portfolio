# Day 7 — Week-1 capstone: `expense-tracker` CLI, alone

> Week 1 · Python fluency, blank-editor reps · **Day 7 of 30 — final day of Week 1**

---

## Why today exists

Six days ago you couldn't type Python from a blank file. Today you'll build a complete CLI tool from a one-page spec, in a fresh repo, alone, in 5–6 hours. No template. No starter code. No copy-pasting from prior days (except utility patterns you genuinely understand).

This is the proof-of-concept day for the entire 30-day plan. **If you can build this today, the rest of the curriculum will work.** Weeks 2–4 require steadily growing build-muscle; Week 1 has been training that muscle through scaffolded exercises. Today's the unscaffolded test.

You'll also use SQLite for the first time. SQLite is in Python's stdlib — no install required — and it's the database powering Firefox, Chrome, your phone's apps, every iOS app, and roughly half of all web apps. By tonight you'll have written real SQL queries against a real database.

---

## What you'll be able to do by EOD

- Build a multi-command CLI from scratch in one session
- Design a SQLite schema for a small but real domain
- Write parameterized SQL queries (and explain why parameterization matters)
- Make decisions about file layout, error handling, and UX without external prompts
- Ship a project with a README clear enough for a stranger to use

---

## Today's schedule (target: 6 hours)

| Block | Time | What |
|-------|------|------|
| Morning concept | 30 min | Brief SQLite primer |
| Build | 5 hrs | The expense tracker, end to end |
| Wrap up | 30 min | README, screenshot, commit, push, week-1 retrospective |

The schedule is intentionally shorter today. You've earned an early evening.

---

## Concept primer (30 min)

### SQLite via Python's stdlib `sqlite3`

SQLite stores an entire database in **one file**. No server, no setup, no config. You open the file, you read/write, you close. That's it.

```python
import sqlite3

# Connect — creates the file if it doesn't exist
conn = sqlite3.connect("expenses.db")

# Get a cursor for issuing queries
cur = conn.cursor()

# Schema (run once)
cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        note TEXT
    )
""")

# Insert a row — use ? placeholders, NEVER string formatting
cur.execute(
    "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
    (250.0, "food", "2026-05-02", "lunch")
)
conn.commit()                    # writes are NOT persisted until commit

# Query
cur.execute("SELECT * FROM expenses WHERE category = ?", ("food",))
rows = cur.fetchall()           # list of tuples
for row in rows:
    print(row)                  # (1, 250.0, 'food', '2026-05-02', 'lunch')

conn.close()
```

#### The single most important rule: parameterize

**NEVER** do this:
```python
cur.execute(f"SELECT * FROM expenses WHERE category = '{user_input}'")
```

If `user_input` is `"'; DROP TABLE expenses; --"`, you've just lost all data. This is the textbook **SQL injection** vulnerability.

**ALWAYS** do this:
```python
cur.execute("SELECT * FROM expenses WHERE category = ?", (user_input,))
```

The `?` is a placeholder. The driver substitutes the value safely, treating it as data, not SQL.

#### Convenient row access — `Row` factory

By default, query results come as tuples. Configure the connection to return dict-like rows instead:

```python
conn = sqlite3.connect("expenses.db")
conn.row_factory = sqlite3.Row

cur = conn.execute("SELECT * FROM expenses LIMIT 1")
row = cur.fetchone()
row["amount"]                    # access by column name
row[0]                           # also works by index
dict(row)                        # convert to plain dict
```

#### Transactions

`conn.commit()` saves changes. `conn.rollback()` undoes uncommitted changes. By default, every `execute()` starts an implicit transaction; `commit()` ends it.

For a CLI tool that does one operation per run, you'll commit after each write and that's plenty.

#### Schema migrations — for today, just `CREATE TABLE IF NOT EXISTS`

Real apps have migration tools. Today, every connection just runs the `CREATE TABLE IF NOT EXISTS` SQL again. That's safe to repeat: if the table already exists nothing happens, and if it doesn't, it's created. (The word for "safe to run over and over" is **idempotent** — you'll meet it constantly.)

---

## Pre-flight check

```bash
cd ~/Projects/ml-portfolio
source .venv/bin/activate
git status
git checkout main && git pull
```

Note: today's code does **not** go in `ml-portfolio`, so don't branch it yet. You'll come
back to this repo once, at the end of the day, for the Week 1 retrospective.

**Decision: where does the project live?**

Two options:
- **Option A** — A dedicated GitHub repo `expense-tracker` (separate from `ml-portfolio`).
- **Option B** — A subfolder `projects/expense-tracker/` inside `ml-portfolio`.

**Pick Option A.** Reasoning: by Day 25 you'll be pinning repos on your GitHub profile. A standalone `expense-tracker` is one of those pins. Subfolder projects don't pin. The 5 minutes to create a separate repo today saves rebuilding the structure on Day 25.

```bash
cd ~/Projects
mkdir expense-tracker
cd expense-tracker
git init
python -m venv .venv
source .venv/bin/activate
```

You'll create `requirements.txt`, `.gitignore`, etc. as you go — same pattern as Day 1.

---

## The spec — read carefully, then start

### What the user can do

```bash
$ expense add 250 food --note "lunch with team"
Added expense #1: ₹250.00 in food on 2026-05-02

$ expense add 1200 transport --note "uber to airport"
Added expense #2: ₹1200.00 in transport on 2026-05-02

$ expense add 80 food
Added expense #3: ₹80.00 in food on 2026-05-02

$ expense list
ID  DATE        CATEGORY    AMOUNT      NOTE
─────────────────────────────────────────────────────────
3   2026-05-02  food        ₹    80.00
2   2026-05-02  transport   ₹  1200.00  uber to airport
1   2026-05-02  food        ₹   250.00  lunch with team

$ expense list --category food
3   2026-05-02  food        ₹    80.00
1   2026-05-02  food        ₹   250.00  lunch with team

$ expense list --month 2026-05
[same as `list` if all expenses are in May 2026]

$ expense summary
─────────────────────────────────────
Total spend (all time):  ₹  1530.00
This month (2026-05):    ₹  1530.00
Last month (2026-04):    ₹     0.00

By category, this month:
   food         ₹   330.00  (21.6%)
   transport   ₹  1200.00  (78.4%)

3 expenses total.

$ expense export expenses.csv
Exported 3 expenses to expenses.csv

$ expense rm 2
Removed expense #2: ₹1200.00 in transport
```

### Database file location

Store the SQLite DB at `~/.expenses.db` (in the user's home dir, like Day 2's `~/.notes.json`).

This means data persists across project changes. If you rerun the CLI from a different directory, it still finds your data.

### Schema

```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL CHECK (amount > 0),
    category TEXT NOT NULL,
    date TEXT NOT NULL,                    -- ISO format YYYY-MM-DD
    note TEXT                              -- nullable
);

CREATE INDEX IF NOT EXISTS idx_date ON expenses(date);
CREATE INDEX IF NOT EXISTS idx_category ON expenses(category);
```

### Commands — full spec

#### `add`
```
expense add AMOUNT CATEGORY [--note TEXT] [--date YYYY-MM-DD]
```
- `AMOUNT` — float, must be > 0
- `CATEGORY` — non-empty string, lowercased before storing
- `--note` — optional free-text
- `--date` — optional, defaults to today (ISO format)
- Output: `Added expense #{id}: ₹{amount} in {category} on {date}`

#### `list`
```
expense list [--category TEXT] [--month YYYY-MM] [--limit N]
```
- No filters → list all expenses, most recent first
- `--category` → filter to that category (case-insensitive match)
- `--month YYYY-MM` → only that calendar month
- `--limit` → cap the number of rows shown (default 50)
- Output: tabular, aligned columns. If no expenses match, print `No expenses found.`

#### `summary`
```
expense summary
```
- Total spend across all time
- This month's total (current calendar month)
- Last month's total
- Per-category breakdown for this month with percentages, sorted by amount desc
- Total count

#### `export`
```
expense export OUTPUT_FILE
```
- Writes a CSV with columns: `id, date, category, amount, note`
- Header row included
- Print `Exported N expenses to {file}` on success

#### `rm`
```
expense rm ID
```
- Removes the expense with that id
- Print `Removed expense #{id}: ₹{amount} in {category}`
- If id doesn't exist, print error and exit code 1

### Edge cases

- DB file doesn't exist on first run → connect creates it; schema migration creates the table
- `add` with negative amount → reject with helpful error. **Validate in Python, not only
  via the schema.** The `CHECK (amount > 0)` constraint does catch it, but it surfaces as
  `sqlite3.IntegrityError` — a database error leaking out at the user. Check the value in
  `cmd_add` and raise `ValueError` with a readable message; treat the constraint as a
  safety net behind that, not as the error path.
- `add` with empty category → reject
- `list --category` with no matches → print `No expenses found.`, exit 0 (not an error)
- `rm` with missing id → error message, exit 1
- `--date` in the future → allow it (people pre-record planned expenses)
- `--date` in invalid format → error

### Project layout

```
expense-tracker/
├── .venv/                          # gitignored
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
├── expense_tracker/
│   ├── __init__.py
│   ├── __main__.py                 # `python -m expense_tracker`
│   ├── cli.py                      # argparse + dispatch
│   ├── commands.py                 # one function per command
│   ├── db.py                       # connection, schema, CRUD helpers
│   └── formatting.py               # table, currency, percentages
└── tests/
    ├── __init__.py
    ├── conftest.py                 # shared fixtures (a temp DB)
    └── test_commands.py            # at least 5 tests
```

### Tests required (minimum 5)

- [ ] `test_add_creates_expense` — adding returns a valid id, row exists in DB
- [ ] `test_add_rejects_negative_amount` — `pytest.raises(ValueError)`
- [ ] `test_list_filter_by_category` — only matching rows returned
- [ ] `test_list_filter_by_month` — only rows in that month
- [ ] `test_summary_per_category_percentages` — verify math
- [ ] `test_rm_missing_id_raises` — `pytest.raises(KeyError)` or similar
- [ ] `test_export_writes_valid_csv` — file written with header + correct rows

Use a `conftest.py` fixture that gives each test a fresh temp DB:

```python
import pytest
from expense_tracker.db import init_db

@pytest.fixture
def db_path(tmp_path):
    p = tmp_path / "test.db"
    init_db(p)
    return p
```

Pass `db_path` into your command functions (which is why they take a path as a parameter — not a global).

### README requirements

Create `README.md` with these sections:

```markdown
# expense-tracker

A small CLI tool for tracking personal expenses, with SQLite persistence.

## Why I built this

[1 sentence — your honest reason. "Day 7 of a 30-day Python push" is fine.]

## Demo

[Screenshot of `expense summary` output — take with `cmd-shift-4` on macOS, embed as `![demo](demo.png)`]

## Features

- Add, list, filter, summarize, export, remove expenses
- SQLite-backed (no setup; data persists in `~/.expenses.db`)
- CSV export

## Install

    git clone https://github.com/[you]/expense-tracker
    cd expense-tracker
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .

## Usage

    expense add 250 food --note "lunch"
    expense list
    expense list --category food
    expense list --month 2026-05
    expense summary
    expense export expenses.csv
    expense rm 1

## Tech

- Python 3.11
- SQLite (stdlib)
- argparse (stdlib)
- pytest

## License

MIT
```

### `pyproject.toml`

A minimal one that lets `pip install -e .` work and `expense` become a system command:

```toml
[project]
name = "expense-tracker"
version = "0.1.0"
description = "A small CLI tool for tracking personal expenses"
requires-python = ">=3.11"
dependencies = []

[project.scripts]
expense = "expense_tracker.cli:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

After writing this:
```bash
pip install -e .
```

Now `expense add 250 food` works from anywhere.

---

## Suggested order of work

Don't try to write the whole thing top-to-bottom. Build it in **vertical slices** — one thin path through every layer at a time (CLI → command → database), so each slice gives you something you can actually run. The alternative, finishing all of `db.py` before any of it is reachable, means you find out at hour 4 whether it works.

### Slice 1 — Skeleton + schema (45 min)

1. Create folders and empty files
2. `db.py`: write `init_db(path)` that creates the schema. Test it manually:
   ```python
   from expense_tracker.db import init_db
   init_db("/tmp/test.db")     # creates the file with the table
   ```
3. `__main__.py` and `cli.py` minimal: argparse parses one command (`add`) and prints "not implemented"
4. `pip install -e .` works; `expense add 1 food` prints "not implemented"
5. **Commit:** `day-07: skeleton with schema and argparse stub`

### Slice 2 — `add` end-to-end (45 min)

1. Implement `add_expense(db_path, amount, category, date, note)` in `db.py`
2. Implement `cmd_add` in `commands.py` that wraps it, validates inputs, prints confirmation
3. Wire up `cli.py` to dispatch to `cmd_add`
4. Manual test: `expense add 250 food --note "lunch"` → check `~/.expenses.db` has the row (`sqlite3 ~/.expenses.db "SELECT * FROM expenses;"`)
5. Write `tests/test_commands.py::test_add_creates_expense`
6. **Commit:** `day-07: implement add command with validation`

### Slice 3 — `list` (45 min)

1. `db.py`: `list_expenses(db_path, category=None, month=None, limit=50)` returns list of rows
2. `formatting.py`: `format_table(rows)` returns a string with aligned columns
3. `commands.py`: `cmd_list` calls db + formatter, prints
4. Manual test: add 3 expenses, list them
5. Tests: `test_list_filter_by_category`, `test_list_filter_by_month`
6. **Commit:** `day-07: implement list with filtering`

### Slice 4 — `summary` (60 min)

The most numerically interesting command. Be careful with the math.

1. `db.py`: `total_by_month(db_path, year_month)`, `total_by_category_for_month(db_path, year_month)`, `total_all(db_path)`
2. `formatting.py`: helpers for currency formatting and percentages
3. `commands.py`: `cmd_summary` calls all three, formats the report
4. Manual test
5. Test: `test_summary_per_category_percentages`
6. **Commit:** `day-07: implement summary with per-category breakdown`

### Slice 5 — `export` and `rm` (45 min)

1. `commands.py`: `cmd_export` (open CSV, use `csv.DictWriter`, iterate rows)
2. `commands.py`: `cmd_rm` (DELETE WHERE id=?, raise if no rows affected)
3. Tests for both
4. **Commit:** `day-07: implement export to CSV and rm command`

### Slice 6 — Polish (45 min)

1. README with screenshot
2. Error messages reviewed for friendliness
3. `--help` output reviewed (argparse generates it; make sure `description` and `help=` strings make sense)
4. Run all tests one final time: `pytest -v`
5. Take a screenshot of `expense summary` after adding ~10 fake expenses; save as `demo.png`
6. **Commit:** `day-07: polish — README, error messages, demo screenshot`

### Slice 7 — Push and create the GitHub repo (15 min)

1. Create empty repo on GitHub: `expense-tracker`
2. `git remote add origin git@github.com:[you]/expense-tracker.git`
3. `git push -u origin main`
4. On GitHub, edit the repo description and add the demo screenshot to the repo settings
5. **Commit & push:** all done

---

## Common pitfalls today

1. **Forgetting `conn.commit()`.** `INSERT` runs but data isn't saved. The next run starts empty.

2. **Using string formatting in SQL.** `f"...WHERE category = '{cat}'"`. SQL injection. Always `?`.

3. **Date string format inconsistencies.** ISO `YYYY-MM-DD` everywhere. Don't mix with `DD/MM/YYYY` or `MM-DD-YY`.

4. **`--month` filter — comparing strings vs dates.** Storing dates as ISO strings works because they sort lexicographically the same as chronologically: `"2026-05"` matches a `LIKE "2026-05%"` query. Don't try to parse strings to date objects in SQL.

5. **`AUTOINCREMENT` ids being reused after `rm`.** They aren't. SQLite's `AUTOINCREMENT` guarantees ids never repeat in a table. You may see gaps; that's correct.

6. **Forgetting `if __name__ == "__main__":` in `__main__.py`.** Without it, `python -m expense_tracker` won't run anything.

7. **`pip install -e .` fails because `pyproject.toml` is malformed.** Validate with `python -c "import tomllib; tomllib.loads(open('pyproject.toml','rb').read().decode())"`.

8. **Tests pass locally but "feel wrong".** Verify each test actually has at least one `assert`. A test with no assertions always passes.

---

## Anti-stall guardrails for today

**Failure mode #1: scope creep.**

You'll be tempted to add: tags, recurring expenses, budget limits, currency conversion, charts, sync to Google Sheets. **Don't.** The spec is the spec. Ship the spec. You can add features later — but only AFTER the base ships.

**Failure mode #2: starting with the "right" architecture.**

Spending an hour deciding whether `db.py` should expose a `Database` class or just functions. **Pick one in 30 seconds and move on.** Functions for today (we already practiced classes Day 4). The architecture choice doesn't matter; the shipped tool does.

**Failure mode #3: hour 4 panic when slices 4+5 aren't done.**

If at hour 4 only `add` and `list` work: ship those, write a README that honestly describes what's done, push it. **A working subset that's deployed > a complete version that doesn't compile.** You can finish the rest tomorrow as a Week-2 morning warmup.

**Failure mode #4: the test fixture rabbit hole.**

The pytest fixture for a temp DB is genuinely fiddly. If you're 30 min in and tests still won't run, simplify: hardcode `/tmp/test_expenses.db`, `os.remove` it at test start, move on. Perfect fixtures can wait.

---

## Self-assessment

1. Why use `?` placeholders in SQL instead of f-strings?
2. What does `conn.commit()` do, and what happens if you forget it?
3. Why is `~/.expenses.db` a better location than `./expenses.db`?
4. In the schema, why `date TEXT` instead of a SQLite `DATE` type?
5. Why split `db.py` and `commands.py` into separate files?
6. How would you change the design if multiple users needed to share the same data?

---

## Stretch (only if you finish before hour 5)

- Add an `--ascii-chart` flag to `summary` that draws a horizontal bar chart of categories
- Add `expense edit ID --amount X --category Y` to modify an existing expense
- Add a config file at `~/.expensesrc` with default category and date format

---

## Deliverable checklist

- [ ] New GitHub repo `expense-tracker`, public
- [ ] All 6 commands working: `add`, `list`, `summary`, `export`, `rm`, `--help`
- [ ] At least 5 pytest tests, all green
- [ ] `pip install -e .` succeeds; `expense ...` runs from anywhere
- [ ] `README.md` with the sections above + screenshot of `summary` output
- [ ] `~/.expenses.db` actually accumulates expenses across runs
- [ ] At least 8 commits today, all with `day-07:` prefix
- [ ] `expense-tracker` pushed to its own GitHub repo (`main`)
- [ ] `WEEK1_REVIEW.md` merged into `ml-portfolio` via PR
- [ ] `expense-tracker` repo visible on your GitHub profile

---

## Done when

```bash
expense add 250 food --note "lunch"
expense add 1200 transport
expense list
expense summary
expense export /tmp/exp.csv && cat /tmp/exp.csv
expense rm 1
expense list
pytest -v
```

Every command produces sensible output. All tests pass.

---

## Week 1 retrospective (15 min, end of day)

Open or create `WEEK1_REVIEW.md` at the main `ml-portfolio` repo root (NOT in `expense-tracker`). Answer honestly:

1. **What can I do now that I couldn't 7 days ago?** (Be specific. "I can write a CLI from scratch.")
2. **Which day was hardest, and why?**
3. **Where am I weakest entering Week 2?**
4. **Did I skip anything from the curriculum, and what was the cost?**
5. **What's my biggest worry about Week 2 (data stack)?**

This document is for you, not anyone else. Keep it terse.

```bash
cd ~/Projects/ml-portfolio
git checkout -b day-07-retrospective
git add WEEK1_REVIEW.md
git commit -m "day-07: week 1 retrospective"
git push -u origin day-07-retrospective
# then open the PR and merge it, same as every other day
```

---

## Take the evening off

You shipped a working CLI tool, alone, in one day. That wasn't possible 7 days ago. Don't celebrate by jumping into Week 2. **Close the laptop. Eat. Sleep early.**

Tomorrow you start NumPy. The next 7 days are the data stack.

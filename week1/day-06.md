# Day 6 — Standard library tour: regex, CSV, JSON, datetime

> Week 1 · Python fluency, blank-editor reps · **Day 6 of 30**

---

## Why today exists

Most of the data work you'll do for the next 24 days is **parsing structured text**. CSVs to read into pandas. JSON from APIs. Regex to clean dirty fields. Dates to align time-series. All of these are in Python's standard library — no third-party packages needed — and none of them are hard. But each one has a few traps that are easy to fall into and hard to spot afterwards. The point of today is to hit those traps once, in a low-stakes setting, so they don't bite you on Day 10 when you're cleaning the Bengaluru rent dataset and on Day 22 when you're polishing the capstone.

You'll also build a `log_analyzer` — a CLI that parses real Apache/Nginx logs and produces summary reports. This is a tiny version of what every backend engineer does monthly. It's good portfolio material ("I built a log parser") and it forces you to use regex on real, ugly input.

---

## What you'll be able to do by EOD

- Write regex patterns for common cases (emails, dates, URLs, IPs) without copy-pasting from Stack Overflow
- Use named groups (`(?P<name>...)`) and explain why they beat positional groups
- Read and write CSVs correctly (with headers, with quoted fields, with non-comma delimiters)
- Parse and format dates with `datetime` (knowing the difference between `strptime` and `strftime`)
- Use `pathlib.Path` for everything path-related
- Build a multi-report CLI that processes a real log file in <50ms

---

## Today's schedule (target: 6.5 hours)

| Block | Time | What |
|-------|------|------|
| Morning concept | 75 min | Read the concept primer below |
| Practice | 2 hrs | 5 regex problems |
| Build | 3 hrs | `log_analyzer` CLI |
| Wrap up | 30 min | Commit + push |

---

## Concept primer (75 min)

### 1. Regex — the 10% you'll use 90% of the time (20 min)

Regular expressions are a tiny special-purpose language: it does exactly one job — describing patterns in text — and nothing else. Python's `re` module lets you use it.

#### The atoms

| Pattern | Matches |
|---------|---------|
| `a` | The literal character a |
| `.` | Any single character (except newline) |
| `\d` | A digit (0-9) |
| `\D` | NOT a digit |
| `\w` | A word character (a-z, A-Z, 0-9, _) |
| `\W` | NOT a word character |
| `\s` | Whitespace (space, tab, newline) |
| `\S` | NOT whitespace |
| `[abc]` | Any of a, b, c |
| `[a-z]` | Any lowercase letter |
| `[^abc]` | NOT a, b, or c |

#### Repetition

| Pattern | Means |
|---------|-------|
| `a*` | Zero or more a's |
| `a+` | One or more a's |
| `a?` | Zero or one a |
| `a{3}` | Exactly 3 a's |
| `a{2,4}` | Between 2 and 4 a's |
| `a{2,}` | At least 2 a's |

By default, repetition is **greedy** — it matches as much as possible. Add `?` to make it lazy: `a+?` matches as little as possible.

#### Anchors

| Pattern | Means |
|---------|-------|
| `^` | Start of string (or line, in MULTILINE mode) |
| `$` | End of string (or line) |
| `\b` | Word boundary |

#### Groups

| Pattern | Means |
|---------|-------|
| `(...)` | Capturing group (positional) |
| `(?P<name>...)` | Named capturing group |
| `(?:...)` | Non-capturing group (just for grouping, doesn't capture) |

#### The functions

```python
import re

# Search for first match anywhere
m = re.search(r"\d+", "abc 123 def 456")
m.group()      # "123"

# Find ALL matches
re.findall(r"\d+", "abc 123 def 456")     # ["123", "456"]

# Find all matches AS match objects (so you can access groups)
for m in re.finditer(r"\d+", "abc 123 def 456"):
    print(m.start(), m.group())

# Substitute
re.sub(r"\d+", "X", "abc 123 def 456")    # "abc X def X"

# Split (regex as delimiter)
re.split(r"\s+", "a   b\tc")              # ["a", "b", "c"]

# Compile once, reuse — faster for repeated use
pat = re.compile(r"\d+")
pat.findall("abc 123")
```

#### Named groups in action

```python
log_line = '127.0.0.1 - - [02/May/2026:10:23:45 +0530] "GET /api/users HTTP/1.1" 200 1234'

pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'
    r'-\s+-\s+'
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>\w+)\s+(?P<url>\S+)\s+\S+"\s+'
    r'(?P<status>\d+)\s+'
    r'(?P<bytes>\d+)'
)

m = pattern.search(log_line)
m.group("ip")          # "127.0.0.1"
m.group("status")      # "200"
m.groupdict()
# {'ip': '127.0.0.1', 'timestamp': '02/May/2026:...', 'method': 'GET', ...}
```

Named groups are dramatically more readable than positional `m.group(1), m.group(2)`. **Always name your groups.**

#### Raw strings

```python
re.search("\\d+", "abc 123")     # works but ugly
re.search(r"\d+", "abc 123")     # raw string — `\d` is literal backslash-d
```

`r"..."` tells Python "don't interpret backslash escapes." Always use raw strings for regex patterns.

#### The "regex isn't real parsing" rule

Regex is great for:
- Extracting fields from semi-structured text (logs, free-form fields)
- Validation ("is this a valid email format?")
- Search-and-replace

Regex is BAD for:
- Parsing nested structures (HTML, JSON, code) — use a real parser
- Anything requiring counting (regex can't count balanced parens)

When you find yourself writing a regex with `(?:.+?){0,5}` and three lookaheads, stop. Use a parser.

### 2. CSV — read and write correctly (15 min)

CSVs are deceptively simple. Real-world ones have:
- Quoted fields (`"hello, world"` is one field, not two)
- Escaped quotes inside quotes (`"she said ""hi"""`)
- Different delimiters (TSV uses tab, European CSVs use semicolon)
- Different encodings (UTF-8, Latin-1, Windows-1252)

The standard library `csv` module handles most of this for you.

#### Reading

```python
import csv

with open("data.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)            # row is a list of strings
```

`newline=""` is required — let the csv module handle line endings, don't let Python's `open()` translate them.

#### DictReader — usually what you want

```python
with open("data.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])    # row is a dict, keyed by header row
```

`DictReader` reads the first row as headers and gives you a dict per row. Way more readable than positional indexing.

#### Writing

```python
with open("out.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Alice", 30])
    writer.writerow(["Bob, Jr.", 40])    # comma in name handled automatically
```

Or with dicts:
```python
with open("out.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 40}])
```

#### Pitfalls

- All values come back as strings. `int(row["age"])` if you want a number.
- Empty cells come back as empty strings, not `None`.
- BOM (byte order mark) at start of UTF-8 files: use `encoding="utf-8-sig"` if Excel exported it.

### 3. JSON — beyond load/dump (10 min)

You used `json.load` and `json.dump` on Day 2. Today, deeper:

#### `json.dump` options

```python
json.dump(data, f,
    indent=2,                  # pretty-print with 2-space indent
    sort_keys=True,            # alphabetize keys
    ensure_ascii=False,        # write non-ASCII as-is (not \uXXXX)
)
```

#### Custom serialization

JSON can't natively encode `datetime`, `Decimal`, sets, custom classes. Two options:

```python
# Option 1: convert to JSON-friendly types yourself before dumping
data = {"created": today.isoformat()}

# Option 2: pass a default function
def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"can't serialize {type(obj)}")

json.dump(data, f, default=serialize)
```

#### Loading: `json.loads` on user input

JSON parsing can fail on bad input. Always wrap user-provided JSON in `try`:

```python
try:
    data = json.loads(user_input)
except json.JSONDecodeError as e:
    print(f"bad JSON at line {e.lineno}, col {e.colno}: {e.msg}")
```

### 4. `datetime` — dates and times (15 min)

The `datetime` module has four classes you'll meet:

- `date` — a calendar date (year, month, day)
- `time` — a time of day (hour, minute, second)
- `datetime` — both combined
- `timedelta` — a duration

```python
from datetime import date, datetime, timedelta

# Today
date.today()              # date(2026, 5, 2)
datetime.now()            # datetime(2026, 5, 2, 14, 30, 45, 123456)

# Construct
date(2026, 5, 2)
datetime(2026, 5, 2, 14, 30)

# Arithmetic
tomorrow = date.today() + timedelta(days=1)
last_week = date.today() - timedelta(weeks=1)

# Difference between dates
(date(2026, 12, 31) - date(2026, 1, 1)).days     # 364
```

#### Parsing strings — `strptime`

```python
datetime.strptime("2026-05-02", "%Y-%m-%d")            # datetime(2026, 5, 2, 0, 0)
datetime.strptime("02/May/2026:10:23:45", "%d/%b/%Y:%H:%M:%S")
```

The format codes:
- `%Y` — 4-digit year
- `%y` — 2-digit year
- `%m` — 2-digit month
- `%b` — abbreviated month name (Jan, Feb, Mar)
- `%B` — full month name
- `%d` — 2-digit day
- `%H` — 24-hour
- `%I` — 12-hour
- `%M` — minute
- `%S` — second
- `%p` — AM/PM
- `%z` — timezone offset (+0530)
- `%a` — abbreviated weekday (Mon, Tue)

You'll memorize the common ones with practice. Cheat sheet: https://strftime.org/

#### Formatting dates — `strftime`

```python
today = date.today()
today.strftime("%Y-%m-%d")          # "2026-05-02" — ISO format
today.strftime("%B %d, %Y")          # "May 02, 2026"
today.isoformat()                    # "2026-05-02" — shortcut for ISO

datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # human-readable timestamp
```

**The mnemonic: `strptime` PARSES (string → object). `strftime` FORMATS (object → string).**

#### Pitfall: timezone-naive vs timezone-aware

```python
datetime.now()                       # naive — no timezone info
datetime.now(timezone.utc)           # aware — knows it's UTC
```

Mixing naive and aware datetimes raises `TypeError`. For today's exercise we'll stay naive (logs typically have a single timezone). For real apps, prefer timezone-aware.

### 5. `pathlib` deep dive (10 min)

You met `Path` on Day 2. More tricks:

```python
from pathlib import Path

p = Path("week1/python/01_number_stats.py")

p.exists()                       # True
p.is_file()                      # True
p.is_dir()                       # False
p.suffix                         # ".py"
p.stem                           # "01_number_stats"
p.name                           # "01_number_stats.py"
p.parent                         # Path("week1/python")
p.parts                          # ("week1", "python", "01_number_stats.py")
p.absolute()                     # full path
p.resolve()                      # full path with symlinks resolved

# Reading and writing as one-liners
p.read_text(encoding="utf-8")
p.write_text("hello", encoding="utf-8")
p.read_bytes()
p.write_bytes(b"hello")

# Globbing
list(Path("week1").glob("**/*.py"))     # all .py recursively
list(Path("week1").glob("*.md"))        # only top-level .md
```

`Path` should replace every `os.path.join` you'd write. It's better in every dimension.

### 6. The standard library you'll meet later (5 min)

Bookmarks for the future, no need to read deeply today:

- `collections` — `Counter`, `defaultdict`, `deque`, `namedtuple`. You used `Counter` on Day 1.
- `itertools` — efficient looping primitives: `chain`, `combinations`, `groupby`, `islice`.
- `functools` — `lru_cache` for memoization, `partial` for currying.
- `dataclasses` — auto-generated `__init__`, `__eq__`, `__repr__` from class annotations. Underrated.
- `typing` — type hints. You'll use these on Day 23.
- `subprocess` — run shell commands from Python.
- `urllib`, `http.client` — basic HTTP. (For real HTTP work, install `requests`.)

---

## Pre-flight check

```bash
cd ~/Projects/ml-portfolio
source .venv/bin/activate
git status
git checkout main && git pull
git checkout -b day-06-stdlib
mkdir -p week1/practice/day06
mkdir -p log_analyzer
```

---

## Practice (2 hours) — 5 regex problems

Create `week1/practice/day06/regex_problems.py`. **No LLM, no Stack Overflow first pass.** Use the cheat sheet at https://docs.python.org/3/howto/regex.html if needed.

```python
"""Five regex problems. Use named groups everywhere."""
import re


def extract_emails(text: str) -> list[str]:
    """Return all email addresses in text. Match the common forms:
    foo@bar.com, foo.bar@baz.co.uk, foo+tag@bar.com."""
    # TODO


def extract_phone_numbers(text: str) -> list[str]:
    """Return all Indian phone numbers in text.
    Match: +91-9876543210, +919876543210, 9876543210, 98765 43210, 098765-43210.
    Return them in the original form (don't normalize)."""
    # TODO


def extract_dates(text: str) -> list[str]:
    """Return all dates matching DD/MM/YYYY or DD-MM-YYYY formats.
    Years 1900-2099. Months 01-12. Days 01-31 (don't validate calendar correctness).
    Return them in their original form."""
    # TODO


def extract_urls(text: str) -> list[str]:
    """Return all URLs starting with http:// or https://.
    Stop at whitespace, end of string, or trailing punctuation (.,!?)."""
    # TODO


def extract_hashtags(text: str) -> list[str]:
    """Return all hashtags from a tweet-like string.
    A hashtag is # followed by 1+ word characters.
    Return without the # symbol."""
    # TODO


# Tests
if __name__ == "__main__":
    assert sorted(extract_emails(
        "Email me at foo@bar.com or foo.bar+spam@baz.co.uk"
    )) == ["foo.bar+spam@baz.co.uk", "foo@bar.com"]

    nums = extract_phone_numbers(
        "Call +91-9876543210 or 9876543210 or +919876543210"
    )
    assert len(nums) == 3

    dates = extract_dates("Born 02/05/1995. Met on 14-02-2020. Wedding 15/04/2024.")
    assert dates == ["02/05/1995", "14-02-2020", "15/04/2024"]

    urls = extract_urls(
        "See https://example.com or http://foo.bar/baz?q=1 . Also visit https://x.io!"
    )
    assert "https://example.com" in urls
    assert "http://foo.bar/baz?q=1" in urls
    assert "https://x.io" in urls
    # Trailing punctuation NOT included
    assert "https://example.com." not in urls

    tags = extract_hashtags("Loving #python and #MachineLearning today! #100daysofcode")
    assert sorted(tags) == sorted(["python", "MachineLearning", "100daysofcode"])

    print("All regex tests passed.")
```

Commit:
```bash
git add week1/practice/day06/regex_problems.py
git commit -m "day-06: implement 5 regex problems with named groups"
```

---

## Build session — `log_analyzer` CLI (3 hours)

### What you're building

A package that parses a web server access log and produces 4 reports:

```bash
$ python -m log_analyzer access.log

╔══════════════════════════════════════════════════════╗
║              Log Analysis Report                      ║
╚══════════════════════════════════════════════════════╝

File: access.log     Lines: 12,453     Parsed: 12,440 (99.9%)

── Top 10 IPs ──────────────────────────────────────────
   1. 203.0.113.42       4,231 requests
   2. 198.51.100.7       2,108 requests
   3. ...

── Top 10 URLs ─────────────────────────────────────────
   1. /api/users         3,890 requests
   2. /                  2,540 requests
   3. ...

── Status code summary ─────────────────────────────────
   2xx Success:    11,902 (95.7%)
   3xx Redirect:      230 (1.8%)
   4xx Client error:   240 (1.9%)
   5xx Server error:    68 (0.5%)

── Requests per hour ───────────────────────────────────
   00:00 ▇▇▇▇▇▇                       234
   01:00 ▇▇▇▇                          156
   ...
```

### Get a sample log

The "Common Log Format" / "Combined Log Format" is what Apache and Nginx use. Search GitHub for "sample apache access log" — many gists have one. Or generate one:

```bash
# Tiny synthetic log for testing — save to log_analyzer/sample.log
cat > log_analyzer/sample.log << 'EOF'
127.0.0.1 - - [02/May/2026:10:23:45 +0530] "GET /api/users HTTP/1.1" 200 1234
127.0.0.1 - - [02/May/2026:10:24:12 +0530] "POST /api/login HTTP/1.1" 200 567
192.168.1.5 - - [02/May/2026:10:25:01 +0530] "GET / HTTP/1.1" 200 4567
192.168.1.5 - - [02/May/2026:10:25:30 +0530] "GET /missing HTTP/1.1" 404 234
10.0.0.3 - - [02/May/2026:11:01:00 +0530] "GET /api/users HTTP/1.1" 500 100
10.0.0.3 - - [02/May/2026:11:02:00 +0530] "GET /api/users HTTP/1.1" 200 1234
EOF
```

For a real test, find a sample log file with at least 1000 lines. Search:
- "elastic.co sample logs"
- "logstash sample data"
- GitHub: `filename:access.log size:>10000`

### Folder structure

```
log_analyzer/
├── __init__.py
├── __main__.py            # CLI: argparse, dispatch
├── parser.py              # parse_line, parse_file
├── reports.py             # top_ips, top_urls, status_summary, hourly_histogram
├── formatting.py          # text formatting helpers (the bar chart, the boxes)
└── sample.log             # for manual testing
```

### Spec

#### `parser.py`

```python
"""Parse Apache/Nginx common log format lines."""
import re
from datetime import datetime
from typing import NamedTuple


# Combined Log Format pattern with named groups
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+'
    r'\S+\s+\S+\s+'                       # ident, user (usually -)
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<url>\S+)\s+\S+"\s+'   # request line
    r'(?P<status>\d+)\s+'
    r'(?P<bytes>\d+|-)'
)


class LogEntry(NamedTuple):
    ip: str
    timestamp: datetime
    method: str
    url: str
    status: int
    bytes: int            # 0 if "-"


def parse_line(line: str) -> LogEntry | None:
    """Parse one log line. Return LogEntry on success, None on parse failure."""
    # TODO


def parse_file(path: str) -> tuple[list[LogEntry], int]:
    """Parse every line in the file. Return (entries, parse_failures_count)."""
    # TODO
```

#### `reports.py`

```python
from collections import Counter
from .parser import LogEntry


def top_ips(entries: list[LogEntry], n: int = 10) -> list[tuple[str, int]]:
    """Top n IPs by request count, descending."""
    # TODO


def top_urls(entries: list[LogEntry], n: int = 10) -> list[tuple[str, int]]:
    """Top n URLs by request count, descending."""
    # TODO


def status_summary(entries: list[LogEntry]) -> dict[str, int]:
    """Return counts grouped by status class.
    Keys: "2xx", "3xx", "4xx", "5xx" (always present, 0 if no occurrences)."""
    # TODO


def hourly_histogram(entries: list[LogEntry]) -> dict[int, int]:
    """Return dict mapping hour (0-23) to request count.
    All 24 hours always present (0 if no requests that hour)."""
    # TODO
```

#### `formatting.py`

```python
def format_box(title: str, width: int = 56) -> str:
    """Format a title in a box."""
    # TODO

def format_section_header(title: str, width: int = 56) -> str:
    """Format `── Title ─────────...` style header."""
    # TODO

def format_bar(value: int, max_value: int, width: int = 30) -> str:
    """Format a bar of width `width` chars proportional to value/max_value.
    Use the █ (or ▇) character."""
    # TODO

def format_top_n(items: list[tuple[str, int]], indent: int = 3) -> str:
    """Format a top-N list as numbered lines."""
    # TODO
```

#### `__main__.py`

```python
import argparse
from .parser import parse_file
from .reports import top_ips, top_urls, status_summary, hourly_histogram
from .formatting import format_box, format_section_header, format_bar, format_top_n


def main():
    parser = argparse.ArgumentParser(prog="log_analyzer")
    parser.add_argument("logfile", help="path to access log")
    parser.add_argument("--top", type=int, default=10, help="how many top items")
    parser.add_argument("--json", action="store_true", help="output JSON instead")
    args = parser.parse_args()

    entries, failures = parse_file(args.logfile)
    total = len(entries) + failures

    # if --json: print json.dumps of all reports
    # else: print formatted reports as in the example

    # TODO


if __name__ == "__main__":
    main()
```

### Manual test sequence

```bash
$ python -m log_analyzer log_analyzer/sample.log
# Should produce a small but well-formatted report

$ python -m log_analyzer log_analyzer/sample.log --top 3
# Top sections show only 3

$ python -m log_analyzer log_analyzer/sample.log --json | python -m json.tool
# Should be valid JSON
```

### `log_analyzer/README.md`

```markdown
# log_analyzer

Parses Apache/Nginx access logs and produces summary reports.

## Usage

    python -m log_analyzer path/to/access.log
    python -m log_analyzer path/to/access.log --top 5
    python -m log_analyzer path/to/access.log --json > report.json

## Sample output

[paste the actual output of running it on sample.log]
```

### Tests

Add `tests/test_log_parser.py` with at least 5 tests:

- [ ] `test_parse_simple_get_line`
- [ ] `test_parse_with_dash_for_bytes`
- [ ] `test_parse_returns_none_on_garbage`
- [ ] `test_top_ips_returns_descending_count`
- [ ] `test_status_summary_has_all_keys`

Run: `pytest tests/test_log_parser.py -v`. All green.

### Commits

```bash
git commit -m "day-06: log_analyzer parser with regex named groups"
git commit -m "day-06: log_analyzer reports module (top ips, urls, status, hourly)"
git commit -m "day-06: log_analyzer formatting (box, bar, sections)"
git commit -m "day-06: log_analyzer CLI with --top and --json flags"
git commit -m "day-06: log_analyzer pytest tests"
git commit -m "day-06: log_analyzer README with sample output"
```

---

## Common pitfalls today

1. **Forgetting the `r` prefix on regex.** On your Python (3.14) the interpreter warns you:

   ```
   SyntaxWarning: "\d" is an invalid escape sequence. Did you mean "\\d"?
   A raw string is also an option.
   ```

   It still runs — `"\d+"` happens to survive because `\d` isn't a real escape — but
   `"\b"` is the backspace character, so that one silently stops matching what you meant.
   Take the warning seriously; it will become an error in a future Python. Always: `r"..."`.

2. **Greedy matching swallowing too much.** `r"<(.+)>"` on `<a><b>` matches `a><b`, not `a` then `b`. Use `r"<(.+?)>"` (lazy) to match the shortest.

3. **CSV without `newline=""`.** On Windows, lines end in `\r\n`. Without `newline=""`, Python's `open()` translates them, but the `csv` module also translates them, and you get blank rows between every real row.

4. **`datetime.strptime` format string mismatch.** If the log has `02/May/2026:10:23:45` and you write `"%d/%m/%Y:%H:%M:%S"`, you'll get a `ValueError` because `%m` is numeric month and `May` is text. Use `%b` for abbreviated month names.

5. **Forgetting to lowercase URLs/IPs before counting.** `/API/users` and `/api/users` will count as different unless you normalize.

6. **Off-by-one on the histogram.** Hours go 0–23, not 1–24. `for hour in range(24):` (inclusive 0, exclusive 24).

7. **Reading huge files into memory.** For a 1GB log, `.readlines()` will OOM. Stream line by line: `for line in f: ...`. (Today's logs are small enough not to matter; remember it for later.)

---

## Self-assessment

1. What does `r"\d+"` mean, and why the `r`?
2. Why use `(?P<name>...)` instead of just `(...)`?
3. What's the difference between `re.search` and `re.match`?
4. Why does `csv.reader` need `newline=""` in `open()`?
5. What's the difference between `strptime` and `strftime`?
6. In a log line `127.0.0.1 - - [02/May/2026:10:23:45 +0530]`, why does the regex `\[(?P<timestamp>.+)\]` work but is risky?

---

## Stretch (only if you finish before 6 hours)

- Add a `--filter STATUS` flag that filters to only specific status codes (e.g. `--filter 4xx` shows only client errors)
- Add a `--since YYYY-MM-DD` flag to filter by date
- Detect potential attack patterns: a single IP with >50 4xx responses in an hour. Flag in red.

---

## Anti-stall guardrails for today

**Failure mode #1: regex perfection.**

You'll be tempted to write a regex that handles every conceivable email format including RFC 5322 (which is, famously, ~6000 characters of regex). Don't. The "common case" regex covers 99% of real input. If your regex tests pass and your sample log parses, ship it.

**Failure mode #2: CSV format adventures.**

The exercises today don't use CSV — that's intentional, you'll meet CSV again on Day 7 (expense tracker export) and Day 9 (loading the rent dataset). The brief CSV section is for awareness, not deep practice.

**Failure mode #3: making the log_analyzer "production-grade".**

Don't add: streaming parsers, multiprocessing, GeoIP lookup, configurable formats. Today's deliverable is "it works on a sample log and prints pretty reports." That's it.

---

## Deliverable checklist

- [ ] `week1/practice/day06/regex_problems.py` runs with all assertions passing
- [ ] `log_analyzer/` package with 5 files
- [ ] `python -m log_analyzer log_analyzer/sample.log` produces formatted output
- [ ] `python -m log_analyzer log_analyzer/sample.log --json` produces valid JSON
- [ ] `log_analyzer/README.md` with usage and sample output
- [ ] `tests/test_log_parser.py` with at least 5 tests, all green
- [ ] At least 7 commits today on `day-06-stdlib`
- [ ] Branch merged to `main`
- [ ] **Tomorrow is Day 7 — the Week 1 capstone, alone, no template. Mentally prepare.**

---

## Done when

```bash
python week1/practice/day06/regex_problems.py     # All regex tests passed.
python -m log_analyzer log_analyzer/sample.log    # produces formatted report
pytest tests/test_log_parser.py -v                # all green
```

If yes: you've now wrangled real-world dirty text. Tomorrow you build the entire week's capstone alone.

If not: commit partial work. Don't push past 8 hours today — Day 7 needs you fresh.

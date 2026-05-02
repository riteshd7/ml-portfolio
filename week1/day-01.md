# Day 1 — Repo setup + 4 foundational exercises

> Week 1 · Python fluency, blank-editor reps · **Day 1 of 30**

---

## Why today exists

You can read code, recognize syntax, follow along with a video but you you need to practice with an empty editor. **Today's job is to break that freeze.** By tonight you'll have written ~250 lines of working Python from scratch, with assertions that prove correctness, in a real repo with a virtual environment and version control.

Today is also where this kind of plan most often dies. The Nov 2025 → May 2026 stall in your git history is the warning. **The single most important deliverable today is a public commitment post.** More on that at the bottom.

---

## What you'll be able to do by EOD

- Explain what a `venv` is and why it matters
- Write a Python script that uses `if __name__ == "__main__":` correctly
- Write `assert` statements to validate your own code without `pytest`
- Use `git add`, `commit`, `push` on a feature branch, then merge
- Read a `KeyError` traceback and fix the bug in under 60 seconds
- Initialize a new Python project from scratch (venv, requirements.txt, .gitignore, README)

---

## Today's schedule (target: 6.5 hours)

| Block | Time | What |
|------|------|------|
| Morning concept | 60 min | Read the concept primer below |
| Repo setup | 60 min | Build session, part A — venv + .gitignore + requirements.txt + README |
| 4 exercises | 3.5 hours | Practice — see below |
| Wrap up | 30 min | Final commit, push, public post |

Stop at hour 6.5. If you're not done, ship what you have. **Better to commit imperfect code than to keep polishing.**

---

## Concept primer (60 min reading)

### 1. What is a virtual environment, really?

When you `pip install pandas`, where does pandas go? Without a venv: into your global Python install. After 6 months of side projects, your global Python is a swamp of conflicting versions.

A venv is just a folder that contains its own `python` binary and its own `site-packages/` directory. When you "activate" a venv, your shell's `PATH` is reordered so `python` points to the venv's binary instead of the system one. Nothing magical.

```bash
# Create
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Verify it worked
which python   # should print something ending in .venv/bin/python
```

You'll see `(.venv)` prepended to your shell prompt when active. **Always activate before working** in this repo. Add it to muscle memory: open terminal → `cd ml-portfolio` → `source .venv/bin/activate`.

To exit: `deactivate`.

### 2. `requirements.txt` — the manifest

Plain text file. One package per line, optionally with a version pin:

```
pandas==2.2.0
numpy==1.26.0
pytest>=8.0
```

Generate from your current environment:
```bash
pip freeze > requirements.txt
```

Install someone else's:
```bash
pip install -r requirements.txt
```

For Day 1, your `requirements.txt` only needs `pytest`. You'll add more as the curriculum progresses.

### 3. `.gitignore` — what NOT to commit

Without a `.gitignore`, you'll accidentally commit:
- `.venv/` — multi-hundred-MB folder, makes clone slow, breaks for others
- `__pycache__/` — compiled Python artifacts, change every run
- `.ipynb_checkpoints/` — Jupyter autosaves
- `*.pkl` — model files (Week 3+)
- Personal files like `.env` with API keys

The Python `.gitignore` template at https://github.com/github/gitignore/blob/main/Python.gitignore is what to start with. Copy that into your repo.

### 4. `if __name__ == "__main__":` — what does it actually do?

Every Python file has a special variable `__name__`. When you run a file directly (`python myscript.py`), `__name__` is set to `"__main__"`. When a file is imported (`import myscript`), `__name__` is set to `"myscript"`.

```python
def add(a, b):
    return a + b

if __name__ == "__main__":
    # This block ONLY runs when you execute this file directly
    assert add(2, 3) == 5
    print("tests passed")
```

The pattern lets a file serve two roles: a library (when imported) and an executable (when run). You'll see `if __name__ == "__main__":` blocks in all four exercises today — that's where the assertions live.

### 5. `assert` — the simplest test

```python
assert 2 + 2 == 4              # passes silently
assert 2 + 2 == 5              # raises AssertionError
assert 2 + 2 == 5, "math broke"  # raises with custom message
```

`assert` is your testing tool today. (Tomorrow you'll learn `pytest`, which is more structured.) The exercises today already have assertions written for you — your job is to make them all pass.

### 6. Git: the minimal flow for today

```bash
# Make a branch for the day's work
git checkout -b day-01-setup

# After making changes, see what changed
git status
git diff

# Stage and commit (atomic — one logical change per commit)
git add week1/python/01_number_stats.py
git commit -m "day-01: implement number stats functions"

# Push to GitHub
git push -u origin day-01-setup

# When the day is done, merge to main
git checkout main
git merge day-01-setup
git push
```

**Commit messages today must follow the format:** `day-01: <action verb> <thing>`. Examples:
- `day-01: implement count and mean for number stats`
- `day-01: add empty-list error handling to mode`
- `day-01: fix off-by-one in median tiebreaker`

NOT:
- ~~`wip`~~
- ~~`updates`~~
- ~~`changes from today`~~

---

## Pre-flight check

Before you start, verify in your terminal:

```bash
python --version    # 3.11 or newer
git --version       # any modern version
```

If `python --version` shows 3.10 or older, install 3.11+ first. The curriculum assumes 3.11.

---

## Build session, part A — Repo setup (60 min)

Do this first, before the exercises. The exercises need `pytest` installed and the venv active.

### Step 1 — Create the venv (5 min)

```bash
cd ~/Projects/ml-portfolio    # or wherever your repo is
python -m venv .venv
source .venv/bin/activate
which python                  # confirm: ends with .venv/bin/python
```

### Step 2 — Create `.gitignore` (10 min)

Copy the contents of GitHub's official Python `.gitignore` template into a new file at the repo root: `/.gitignore`.

URL: https://github.com/github/gitignore/blob/main/Python.gitignore

After saving, verify with:
```bash
git status   # should NOT list .venv/ or __pycache__/
```

If `.venv/` still appears in `git status`, the `.gitignore` isn't being read — check the file is at the repo root, not inside a folder.

### Step 3 — Create `requirements.txt` (5 min)

```
pytest>=8.0
```

That's it for today. Then install:
```bash
pip install -r requirements.txt
pytest --version    # should print a version
```

### Step 4 — Create `README.md` (30 min)

This README is **your** README, not the curriculum's. It tells visitors (recruiters, future you, the imagined-eventual-collaborator) what this repo is. Suggested structure:

```markdown
# ml-portfolio

A 30-day intensive Python + ML curriculum. This repo tracks my daily work
from "I know Python syntax" to "I have shipped a deployed ML project."

## Curriculum

See [CURRICULUM.md](CURRICULUM.md) for the full 30-day plan.

Daily logs live in `week1/`, `week2/`, `week3/`, `week4/`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Progress

- [ ] Week 1 — Python fluency
- [ ] Week 2 — Data stack + Git + light DSA
- [ ] Week 3 — ML core + capstone
- [ ] Week 4 — Polish, write, apply

## Capstone

Bengaluru Rent Predictor — link will appear here when deployed (Day 21).

## About me

[Your name], [your background in 1 line], [your contact].
```

Keep it short. You'll iterate on it across the 30 days.

### Step 5 — First commit (10 min)

```bash
git checkout -b day-01-setup
git add .gitignore requirements.txt README.md
git commit -m "day-01: initial repo setup with venv, gitignore, requirements"
git push -u origin day-01-setup
```

Verify on GitHub that the commit appears.

---

## The 4 exercises (3.5 hours total)

Open each file in `week1/python/`. Each file has:
- A long docstring explaining the goal, spec, edge cases, and forbidden tools
- Function stubs to implement
- An `if __name__ == "__main__":` block with assertions you must make pass

**The rule today: no LLM, no Stack Overflow on first pass.** Only:
- The docstring in the file
- Python's built-in `help()`: e.g. `help(str.split)`
- Official docs: https://docs.python.org/3/

Stuck for >15 minutes? *Then* search. Read the search result. Close the tab. Implement from memory.

### Exercise 1 — Number Stats (~30 min)

**File:** `week1/python/01_number_stats.py`

Implement 7 stat functions (count, sum, mean, median, mode, variance, stddev) plus a `summary()` wrapper. Pure Python — no numpy.

Run it:
```bash
python week1/python/01_number_stats.py
```

When all assertions pass, you'll see `All tests passed.`. Commit:
```bash
git add week1/python/01_number_stats.py
git commit -m "day-01: implement number stats with edge case handling"
```

**Hints (only read if stuck >15 min):**
<details>
<summary>Hint for median with even-length input</summary>
For a sorted list of length n: if n is odd, return `sorted_nums[n//2]`. If n is even, return the mean of `sorted_nums[n//2 - 1]` and `sorted_nums[n//2]`.
</details>
<details>
<summary>Hint for mode with ties</summary>
Use `Counter(nums)`. Find the max frequency. Return `sorted([k for k, v in counter.items() if v == max_freq])`.
</details>
<details>
<summary>Hint for variance</summary>
Compute the mean once, then `sum((x - mean)**2 for x in nums) / len(nums)`.
</details>

### Exercise 2 — Password Strength Checker (~45 min)

**File:** `week1/python/02_password_checker.py`

A function that returns `{"score": int, "strength": str, "issues": list}`. Five rules. No regex today.

```bash
python week1/python/02_password_checker.py
git add week1/python/02_password_checker.py
git commit -m "day-01: implement password strength checker"
```

**Hint:**
<details>
<summary>How to check "has at least one digit" without regex</summary>
`any(ch.isdigit() for ch in password)` — pythonic and fast.
</details>

### Exercise 3 — Word Frequency (~60 min)

**File:** `week1/python/03_word_frequency.py`

Read a file, count words, return top N. Two functions: `tokenize` and `top_words`.

The test creates a `sample_text.txt` for you if it doesn't exist. After you run the file once, that sample will be at `week1/python/sample_text.txt`. Add it to your commits.

```bash
python week1/python/03_word_frequency.py
git add week1/python/03_word_frequency.py week1/python/sample_text.txt
git commit -m "day-01: implement word frequency with stopword exclusion"
```

**Hints:**
<details>
<summary>Tokenizing without regex</summary>
Iterate character-by-character. Build up a current word in a buffer. When you hit a non-alpha character, push the buffer to the result list and start fresh. Lowercase as you go.
</details>
<details>
<summary>Sorting by count desc then word asc</summary>
`sorted(items, key=lambda kv: (-kv[1], kv[0]))` — negative count for desc, word for asc tiebreak.
</details>

### Exercise 4 — Inventory Manager (~75 min)

**File:** `week1/python/04_inventory_manager.py`

Seven functions sharing one dict. **No classes** — Day 4 will refactor this into a class, and that refactor will only feel meaningful if you do it functionally first.

```bash
python week1/python/04_inventory_manager.py
git add week1/python/04_inventory_manager.py
git commit -m "day-01: implement inventory manager with 7 functions"
```

**Hint:**
<details>
<summary>Returning the inventory from every function</summary>
The simplest approach: mutate `inv` in place AND return it. That way `inv = add_item(inv, ...)` works whether you mutate or copy. Be consistent — don't copy in some functions and mutate in others.
</details>

---

## Common pitfalls today

1. **Forgetting to activate the venv.** If `pip install pytest` says "Requirement already satisfied" but `pytest --version` says command not found, you forgot `source .venv/bin/activate`.

2. **Working in the wrong Python.** Run `which python` whenever in doubt. It should always end in `.venv/bin/python` while you're working in this repo.

3. **Editing a file but running an old cached version.** If your edit doesn't seem to take effect, you might be running a different file. Use `python -c "import os; print(os.path.abspath('01_number_stats.py'))"` to confirm the path.

4. **Shell punctuation issues with commit messages.** Use double quotes: `git commit -m "day-01: ..."`. Single quotes will break if the message contains apostrophes.

5. **Pushing to the wrong branch.** Run `git branch` before `git push` to confirm you're on `day-01-setup`, not `main`.

6. **Asserting a float exactly.** `assert mean([1.5, 2.5]) == 2.0` can fail due to floating-point representation. Use `abs(actual - expected) < 1e-9` instead. (The tests already do this where it matters.)

---

## Self-assessment (5 min at end of day)

Answer these from memory, no looking back at the doc:

1. What does `__name__ == "__main__"` mean, and when is it true?
2. What's the difference between `git add` and `git commit`?
3. Why do we use a venv instead of installing globally?
4. In `01_number_stats.py`, why does `mode([1, 1, 2, 2])` return `[1, 2]` instead of `1`?
5. What would happen if you forgot to put `encoding="utf-8"` in `open()` in `03_word_frequency.py` and the file contained "café"?
6. Why is `04_inventory_manager.py` written without classes today?

If you couldn't answer 4+ from memory, re-read the relevant section of the concept primer before bed.

---

## Stretch (only if you finish before 6 hours)

- Set up `pre-commit` hooks running `black` (formatter) and `ruff` (linter) on every commit. Tutorial: https://pre-commit.com/
- Add a fifth exercise to your repo: a function `roman_to_int(s)` and `int_to_roman(n)`. Write your own assertions.
- Look at how other people's `.gitignore` files differ from yours (search GitHub for popular Python repos).

---

## Anti-stall guardrails for today

**Most likely failure mode #1: getting stuck on Exercise 1's `mode` and quitting at hour 2.**

- Set a 15-minute timer per stuck point. If still stuck, read the hint. If still stuck, search. If still stuck, ship what works (e.g. mode that handles unique values but not ties) and add a `# TODO` comment. **Move on.** A working 80% > a perfect 0%.

**Most likely failure mode #2: spending all day on the README and never starting the exercises.**

- README gets 30 minutes. Set a timer. Hard stop. The README will improve every week of the curriculum — Day 1's version is intentionally rough.

**Most likely failure mode #3: not making the public commitment.**

- The commitment post is the single most important deliverable today. **Do it before the exercises, not after.** The shame asymmetry of public quitting > the comfort of skipping a day. Suggested format:

> Starting a 30-day Python + ML push today. Goal: ship a deployed ML project + apply to internships by [date]. Repo: github.com/[you]/ml-portfolio. Will post weekly progress. Roast me if I disappear.

Post on the platform you'd be most embarrassed to disappear from (LinkedIn for most people; X if your network is there).

---

## Deliverable checklist (commit by EOD)

- [ ] `.venv/` exists and is gitignored (NOT committed)
- [ ] `.gitignore` at repo root, contains the standard Python entries
- [ ] `requirements.txt` at repo root with at least `pytest>=8.0`
- [ ] `README.md` at repo root with the sections listed above
- [ ] `week1/python/01_number_stats.py` runs and prints "All tests passed."
- [ ] `week1/python/02_password_checker.py` runs and prints "All tests passed."
- [ ] `week1/python/03_word_frequency.py` runs and prints "All tests passed."
- [ ] `week1/python/04_inventory_manager.py` runs and prints "All tests passed."
- [ ] `week1/python/sample_text.txt` exists (created by Exercise 3)
- [ ] At least 6 commits on `day-01-setup` branch, all with `day-01: ...` prefix
- [ ] Branch merged into `main` and pushed to GitHub
- [ ] **Public commitment post** — Twitter/LinkedIn — with link to the repo
- [ ] One green square on your GitHub contribution graph today

---

## Done when

You can run this single command and see no errors:
```bash
for f in week1/python/*.py; do echo "=== $f ==="; python "$f" || break; done
```

Output should be 4 blocks each ending in `All tests passed.`

If yes: branch merged, public post live, sleep ready. Tomorrow you'll build a real CLI.
If not: commit the partial work, write 3 lines in `DAY01_LOG.md` about what's broken, and continue tomorrow morning. **Don't push past 8 hours today** — burnout on Day 1 kills Day 2.

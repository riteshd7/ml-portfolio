# Day 4 — Object-Oriented Programming

> Week 1 · Python fluency, blank-editor reps · **Day 4 of 30**

---

## Why today exists

You've now written ~600 lines of Python across 3 days, all of it functional — functions and dicts. That style works for small programs. But there's a class of problems where it breaks down: when the same data needs many operations, when you want to enforce invariants ("balance can never go negative"), or when state and behavior need to travel together.

That's what classes are for. Today is your first serious encounter with object-oriented programming. The math-strong-but-can't-build profile makes this day a trap: you'll be tempted to design beautiful inheritance hierarchies with abstract base classes and metaclasses. **Don't.** Two classes, then refactor yesterday's inventory exercise into a class. That's it.

The core insight by EOD: classes are not about elegance. They're about bundling data with the code that operates on it, so that callers don't have to reach inside the bundle to know what's going on. That's it. Every class you'll see in real codebases either does this well or fails to.

---

## What you'll be able to do by EOD

- Define a class with `__init__`, instance methods, and instance attributes
- Use `@property` to expose computed attributes that look like fields
- Use inheritance to share code between related classes (when it actually helps)
- Refactor a function-based module into a class-based one — and explain why
- Implement method chaining (`obj.foo().bar().baz()`) and explain when it makes sense
- Recognize when a class is the wrong tool and a function is enough

---

## Today's schedule (target: 6.5 hours)

| Block | Time | What |
|-------|------|------|
| Morning concept | 90 min | Read the concept primer below |
| Practice | 2 hrs | Banking exercise (BankAccount + SavingsAccount + Bank) |
| Build | 3 hrs | Refactor Day 1's `04_inventory_manager.py` into a class |
| Wrap up | 30 min | Final commit + push |

---

## Concept primer (90 min)

### 1. What's actually a class? (10 min)

A class is a template for creating objects. An object (also called an "instance") is a bundle of data + methods. You define the template once; you create many instances.

```python
class BankAccount:
    def __init__(self, owner, opening_balance=0):
        self.owner = owner
        self.balance = opening_balance
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.history.append(("withdraw", amount))


a = BankAccount("Alice", 100)
b = BankAccount("Bob")           # opening_balance defaults to 0
a.deposit(50)                    # a.balance is now 150
b.balance                         # 0 — instances are independent
```

Key points:
- `class BankAccount:` defines the template
- `__init__` runs when you call `BankAccount(...)` — it initializes a new instance
- `self` is the instance the method is being called on. **Always the first parameter** of an instance method.
- `self.owner = owner` creates an attribute on this specific instance. Different instances have different attributes.
- Methods are just functions defined inside a class

### 2. `__init__` is not a constructor (10 min)

In some languages (Java, C++), the constructor *creates* the object. In Python, `__init__` runs *after* the object is already created. The actual creation is `__new__`, which you almost never override.

The practical implication: `__init__` initializes attributes. It can't fail to create the object — only fail to initialize it correctly. If `__init__` raises, the partially-initialized object is garbage-collected.

```python
class Account:
    def __init__(self, balance):
        if balance < 0:
            raise ValueError("balance can't be negative")
        self.balance = balance

# Account(-10) raises before assignment; no broken object exists
```

### 3. Instance vs class attributes (10 min)

```python
class Dog:
    species = "Canis familiaris"          # CLASS attribute — shared across instances

    def __init__(self, name):
        self.name = name                  # INSTANCE attribute — per-instance


d1 = Dog("Rex")
d2 = Dog("Buddy")

d1.species         # "Canis familiaris" — looked up on the class
d2.species         # "Canis familiaris" — same object
d1.name            # "Rex"
d2.name            # "Buddy"

Dog.species = "Canis lupus"
d1.species         # "Canis lupus" — class attr changed for everyone
```

**Pitfall: mutable class attributes.**

```python
class Cart:
    items = []                    # CLASS attribute — SHARED!

    def add(self, item):
        self.items.append(item)


c1 = Cart()
c2 = Cart()
c1.add("apple")
c2.items          # ["apple"] — shared list! BUG.
```

The fix:
```python
class Cart:
    def __init__(self):
        self.items = []           # instance attribute — separate per cart
```

This is a classic beginner trap. **Mutable defaults belong in `__init__`, not at the class level.**

### 4. `@property` — computed attributes (10 min)

Sometimes you want callers to write `account.balance`, but `balance` is computed, not stored. `@property` lets you expose a method as if it were an attribute.

```python
class BankAccount:
    def __init__(self):
        self.history = []           # list of (kind, amount) tuples

    @property
    def balance(self):
        total = 0
        for kind, amount in self.history:
            total += amount if kind == "deposit" else -amount
        return total


a = BankAccount()
a.history.append(("deposit", 100))
a.balance                            # 100 — looks like a field, runs code
```

Why use `@property` over a method? Because `account.balance` reads like a noun (data) and `account.compute_balance()` reads like a verb (action). If callers think of it as data, expose it as data.

`@property` makes attributes read-only by default. To allow assignment, define a setter (you won't need this today).

### 5. Inheritance — when, and when NOT (15 min)

Inheritance lets one class extend another, reusing code:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, interest_rate=0.04):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate
```

`super().__init__(...)` calls the parent class's `__init__`. Without it, the parent's setup doesn't happen.

**When to use inheritance:**
- Subclass IS-A parent. SavingsAccount IS-A BankAccount. ✓

  ("IS-A" and "HAS-A" are the standard shorthand for the two ways classes relate.
  *IS-A* means the subclass is a kind of the parent, and inheritance fits.
  *HAS-A* means one class holds another as an attribute — that's **composition**,
  and it's the right answer far more often. `Bank` HAS-A list of accounts;
  it is not itself an account.)
- You want to override or extend specific methods.
- The relationship is stable; you won't be flipping the hierarchy in 3 months.

**When NOT to use inheritance (more common):**
- Just to share code → use plain functions or composition (have one class hold another as an attribute).
- Subclass *uses* parent but isn't a kind-of parent (e.g. `Stack` inheriting `list`) → use composition.
- You're 3 levels deep → 99% sure you've over-designed.

**Today: 1 level of inheritance, max.** `SavingsAccount(BankAccount)` and `Bank` (which holds many BankAccounts via composition). No further hierarchy.

### 6. Dunder methods — `__repr__`, `__eq__`, `__len__` (10 min)

Dunder ("double underscore") methods customize how Python's syntax works on your class.

```python
class Note:
    def __init__(self, id, text):
        self.id = id
        self.text = text

    def __repr__(self):
        return f"Note(id={self.id}, text={self.text!r})"

    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return self.id == other.id and self.text == other.text


n = Note(1, "hi")
print(n)                # uses __repr__ → "Note(id=1, text='hi')"
n == Note(1, "hi")      # True (because __eq__)
n == Note(1, "bye")     # False
```

Useful dunders:
- `__repr__` — debug-friendly representation. **Always define this.** It's what shows up in tracebacks and the REPL.
- `__str__` — human-friendly representation. Falls back to `__repr__` if not defined.
- `__eq__` — what `==` does
- `__len__` — what `len(obj)` does
- `__iter__` — what `for x in obj` does

You'll define `__repr__` on every class today. It costs nothing and saves hours of debugging.

### 7. Method chaining — when it works (10 min)

```python
result = (
    DataProcessor("file.csv")
    .drop_nulls()
    .normalize()
    .filter_by(lambda r: r.age > 18)
    .summary()
)
```

Each method returns `self`, so you can chain. This pattern is everywhere in pandas, jQuery, and Django ORM.

It works when:
- The methods naturally form a pipeline
- Each step transforms the same object
- You don't need branching or intermediate inspection

It DOESN'T work when:
- You need to return something other than `self` from a step
- The chain branches (`x.foo().bar()` AND `x.foo().baz()`)
- The chain is hard to debug — `obj.a().b().c()` failing in `b()` is harder to diagnose than 3 lines

For today's `DataProcessor`, chaining fits. Use it.

### 8. The deeper "why" (15 min)

Functions and dicts (Days 1–3 style) are the right tool when:
- The data is a value, not a thing-with-state. A list of numbers, a parsed JSON.
- The operations are stateless transforms.

Classes are the right tool when:
- The data has a lifecycle (open → modify → save).
- The data has invariants you want to enforce. ("balance ≥ 0" is enforced by `withdraw` raising.)
- The same caller will perform many operations on the same data — and you don't want them passing the data around.

Day 1's inventory exercise was deliberately functional. It works! But every function takes `inv` as the first argument, and callers have to thread `inv` through everything. A class lets you bundle `inv` with the operations:

```python
# Functional (Day 1):
inv = add_item({}, "SKU001", "Notebook", 50, 80.0)
inv = update_qty(inv, "SKU001", -10)
print(total_value(inv))

# OOP (today):
inv = Inventory()
inv.add_item("SKU001", "Notebook", 50, 80.0)
inv.update_qty("SKU001", -10)
print(inv.total_value)        # @property
```

The OOP version reads better because the noun (`inv`) and verbs (`add_item`, `update_qty`) are syntactically connected. That's not a small win — readability scales linearly with codebase size.

---

## Pre-flight check

```bash
cd ~/Projects/ml-portfolio
source .venv/bin/activate
git status                    # clean
git checkout main && git pull
git checkout -b day-04-oop
mkdir -p week1/practice/day04
```

---

## Practice (2 hours) — Banking exercise

Create `week1/practice/day04/banking.py`. Implement three classes per spec.

### `BankAccount`

```python
class BankAccount:
    """A simple bank account.

    Tracks balance and full transaction history. Withdrawals exceeding
    balance raise ValueError ("insufficient funds")."""

    def __init__(self, owner: str, opening_balance: float = 0):
        # owner: the account holder's name (string)
        # opening_balance: starting balance (must be >= 0; raise ValueError otherwise)
        # history: list of tuples (kind, amount) — kind is "deposit" or "withdraw"

    def deposit(self, amount: float) -> None:
        # amount must be > 0; raise ValueError if not.
        # increment balance, append to history.

    def withdraw(self, amount: float) -> None:
        # amount must be > 0; raise ValueError if not.
        # if amount > balance, raise ValueError("insufficient funds").
        # decrement balance, append to history.

    def __repr__(self) -> str:
        # return f"BankAccount(owner={owner!r}, balance={balance})"
```

### `SavingsAccount(BankAccount)`

```python
class SavingsAccount(BankAccount):
    """Bank account that earns periodic interest."""

    def __init__(self, owner: str, opening_balance: float = 0, interest_rate: float = 0.04):
        # call super().__init__ to set up the base
        # store interest_rate

    def apply_interest(self) -> None:
        # add (balance * interest_rate) to balance
        # append ("interest", interest_amount) to history

    def __repr__(self) -> str:
        # include rate
```

### `Bank`

A class that manages many accounts (composition, not inheritance — `Bank` HAS-A list of accounts, it doesn't IS-A account).

```python
class Bank:
    """Manages multiple accounts. Accounts are identified by sequential ints starting at 1."""

    def __init__(self, name: str):
        # name: bank's name
        # accounts: dict[int, BankAccount]
        # next_id: the id to assign to the next opened account (starts at 1)

    def open_account(self, owner: str, opening_balance: float = 0) -> int:
        # create a BankAccount, store it, return its new id

    def open_savings(self, owner: str, opening_balance: float = 0, interest_rate: float = 0.04) -> int:
        # create a SavingsAccount, store it, return its new id

    def get(self, account_id: int) -> BankAccount:
        # return the account, or raise KeyError("no such account: {id}")

    def transfer(self, from_id: int, to_id: int, amount: float) -> None:
        # withdraw from from_id, deposit into to_id
        # if either account is missing, raise KeyError
        # if from_id has insufficient funds, the original account is unchanged
        # (i.e. don't half-complete a transfer)

    @property
    def total_assets(self) -> float:
        # sum of balances across all accounts
```

### Test block

```python
if __name__ == "__main__":
    # BankAccount
    a = BankAccount("Alice", 100)
    a.deposit(50)
    assert a.balance == 150
    a.withdraw(30)
    assert a.balance == 120
    try:
        a.withdraw(1000)
    except ValueError:
        pass
    else:
        raise AssertionError("should have raised on overdraft")

    # SavingsAccount
    s = SavingsAccount("Bob", 1000, 0.05)
    s.apply_interest()
    assert s.balance == 1050
    s.deposit(50)                    # inherited
    assert s.balance == 1100

    # Bank with transfer
    b = Bank("MyBank")
    a_id = b.open_account("Alice", 100)
    bo_id = b.open_account("Bob", 50)
    b.transfer(a_id, bo_id, 30)
    assert b.get(a_id).balance == 70
    assert b.get(bo_id).balance == 80
    assert b.total_assets == 150

    # transfer atomicity
    try:
        b.transfer(a_id, bo_id, 10000)
    except ValueError:
        pass
    assert b.get(a_id).balance == 70    # unchanged
    assert b.get(bo_id).balance == 80   # unchanged

    print("Banking tests passed.")
```

Commit:
```bash
git add week1/practice/day04/banking.py
git commit -m "day-04: implement BankAccount, SavingsAccount, Bank with transfer atomicity"
```

---

## Build session — Refactor `04_inventory_manager.py` into a class (3 hours)

### What you're building

Create `week1/python/04b_inventory_class.py` (don't overwrite Day 1's functional version — keep both for the README to compare).

You'll convert the 7 functions into one `Inventory` class with method chaining where appropriate. **The class must pass an updated test suite that reads like Day 1's, but using OOP syntax.**

### Spec

```python
class Inventory:
    """A simple in-memory inventory of SKUs with name, qty, and price.

    Method chaining: mutating methods return self, queries return data."""

    def __init__(self):
        # internal: dict[sku, dict[name, qty, price]]
        self._items = {}

    # --- mutators (return self for chaining) ---

    def add_item(self, sku: str, name: str, qty: int, price: float) -> "Inventory":
        """Add a new item. Raise KeyError if sku exists. Raise ValueError on negative qty/price."""

    def remove_item(self, sku: str) -> "Inventory":
        """Remove an item. Raise KeyError if sku doesn't exist."""

    def update_qty(self, sku: str, delta: int) -> "Inventory":
        """Adjust quantity by delta. Raise ValueError if result < 0. Raise KeyError if sku missing."""

    # --- queries (return data) ---

    def find(self, query: str) -> list[dict]:
        """Case-insensitive substring search on item names. Return list of
        dicts with sku, name, qty, price."""

    def low_stock(self, threshold: int = 10) -> list[dict]:
        """Items where qty <= threshold. Sorted by qty ascending."""

    @property
    def total_value(self) -> float:
        """Sum of qty * price across all items."""

    @property
    def total_units(self) -> int:
        """Sum of qty across all items."""

    @property
    def total_skus(self) -> int:
        """Count of distinct items."""

    def summary(self) -> dict:
        """Return a dict with total_skus, total_units, total_value, low_stock."""

    # --- dunders ---

    def __len__(self) -> int:
        return self.total_skus

    def __contains__(self, sku: str) -> bool:
        return sku in self._items

    def __repr__(self) -> str:
        return f"Inventory({len(self._items)} items)"
```

### Method chaining demonstration

The whole point of returning `self` from mutators is so callers can write:

```python
inv = (
    Inventory()
    .add_item("SKU001", "Notebook", 50, 80.0)
    .add_item("SKU002", "Pen", 200, 10.0)
    .add_item("SKU003", "Pencil", 5, 5.0)
    .update_qty("SKU001", -5)
)

print(inv.total_value)
print(inv.summary())
```

Vs. the imperative style:
```python
inv = Inventory()
inv.add_item("SKU001", "Notebook", 50, 80.0)
inv.add_item("SKU002", "Pen", 200, 10.0)
# etc
```

Both work. Chaining is shorter; imperative is easier to debug. **Support both.** That's what returning `self` enables.

### Test block

Mirror the Day 1 tests but in OOP form:

```python
if __name__ == "__main__":
    inv = Inventory()
    inv.add_item("SKU001", "Notebook", 50, 80.0)
    inv.add_item("SKU002", "Pen", 200, 10.0)
    inv.add_item("SKU003", "Pencil", 5, 5.0)
    inv.add_item("SKU004", "Notepad", 8, 60.0)

    assert len(inv) == 4
    assert "SKU001" in inv
    assert "SKU999" not in inv

    # method chaining
    inv.update_qty("SKU001", -5).update_qty("SKU001", 5)
    assert inv.find("note")  # finds Notebook + Notepad
    names = sorted(r["name"] for r in inv.find("note"))
    assert names == ["Notebook", "Notepad"]

    low = inv.low_stock(threshold=10)
    assert len(low) == 2
    assert low[0]["qty"] <= low[1]["qty"]    # sorted asc

    # invariants enforced
    try:
        inv.add_item("SKU001", "dup", 1, 1.0)
    except KeyError:
        pass
    else:
        raise AssertionError

    try:
        inv.update_qty("SKU003", -100)
    except ValueError:
        pass
    else:
        raise AssertionError

    s = inv.summary()
    assert s["total_skus"] == 4
    assert s["total_units"] == 50 + 200 + 5 + 8

    inv.remove_item("SKU002")
    assert "SKU002" not in inv

    print("All Inventory tests passed.")
```

Commit:
```bash
git commit -m "day-04: refactor inventory_manager into Inventory class with chaining"
```

### A note on "class methods that mutate vs. return new"

There are two design choices for mutator methods:

**Choice A — mutate self, return self (today's choice):**
```python
inv.add_item(...).add_item(...)    # mutates inv each time
```

**Choice B — return a new instance (immutable style):**
```python
inv2 = inv.add_item(...)   # inv unchanged; inv2 is new
inv3 = inv2.add_item(...)
```

Both have merit. Choice A is what pandas, sqlalchemy, and most "builder" patterns do. Choice B is functional-programming style (cleaner reasoning, more memory). **Today: pick A.** It's the dominant pattern in Python and easier to write.

---

## Common pitfalls today

1. **Forgetting `self`.** `def deposit(amount):` — missing self — will fail with "takes 1 positional argument but 2 were given." Always: `def method(self, ...):`.

2. **Mutable default in `__init__` parameter.**
   ```python
   def __init__(self, history=[]):    # BUG — shared across instances
   ```
   Use `history=None` then `self.history = history if history is not None else []`. Or just default to `[]` *inside* the body: `self.history = []`.

3. **Calling parent `__init__` wrong or not at all.**
   - Don't: `BankAccount.__init__(self, owner, balance)` (works but old-style)
   - Do: `super().__init__(owner, balance)`.
   - If you skip it entirely, parent attributes won't exist and methods that depend on them will fail.

4. **Mistaking `@property` for a method call.** `account.balance` is correct (it looks like an attribute). `account.balance()` will fail with "float is not callable" if `balance` is a property returning a float.

5. **Returning `None` from a chainable method.** A method without an explicit `return` returns `None`. The next call in the chain will fail with `'NoneType' object has no attribute 'xxx'`. Always end mutators with `return self`.

6. **Overusing inheritance.** If `B(A)` only adds one method, ask: "could B just be a function that takes an A?" Often yes. Inheritance is the heavy tool.

7. **Storing related state outside the class.** If you find yourself with a global dict that lives "next to" your class instances and tracks per-instance metadata, that data belongs on the instance.

---

## Self-assessment

1. Why does `class Cart: items = []` cause bugs?
2. What does `super().__init__(...)` do, and what happens if you forget to call it?
3. When is `@property` better than a method? Give an example.
4. Why is `Bank` composed of `BankAccount`s instead of inheriting from `BankAccount`?
5. Why do mutators return `self`?
6. Looking at Day 1's `04_inventory_manager.py` and today's `04b_inventory_class.py`: which would you give a colleague to extend? Why?

---

## Stretch (only if you finish before 6 hours)

- Add `__iter__` to `Inventory` so `for sku, item in inv:` works
- Add a `from_csv(cls, path)` classmethod that loads an Inventory from a CSV file
- Add a `__getitem__` so `inv["SKU001"]` returns the item dict (with KeyError on miss)

---

## Anti-stall guardrails for today

**Failure mode #1 (the math-strong trap): designing the perfect class hierarchy.**

You'll be tempted to add `Account(ABC)` as an abstract base, `CheckingAccount(Account)`, `SavingsAccount(Account)`, `BusinessAccount(Account)`, with mixins for `InterestBearing`, `OverdraftCapable`, `FeeCharging`. **Don't.** This is the pure-mathematician's instinct that produces unmaintainable code in industry. Two classes today. Maximum.

The cure: treat the spec as the contract. If the spec doesn't ask for `BusinessAccount`, you don't add it. Imagine a teammate reading your PR — every class you added is something they have to learn.

**Failure mode #2: refactoring the inventory class endlessly.**

The first version of the class won't be perfect. That's fine. Ship it once tests pass. Don't keep rearranging methods, renaming attributes, debating `_items` vs. `items` for an hour. **Once tests pass, stop.**

**Failure mode #3: skipping `__repr__`.**

Define `__repr__` on every class. It costs 30 seconds and saves you 30 minutes of `print(obj.__dict__)` later.

---

## Deliverable checklist

- [ ] `week1/practice/day04/banking.py` runs and passes all assertions
- [ ] `BankAccount`, `SavingsAccount`, `Bank` defined; `Bank` uses composition
- [ ] All 3 classes have `__repr__`
- [ ] `Bank.transfer` is atomic (failed transfer leaves both accounts unchanged)
- [ ] `week1/python/04b_inventory_class.py` runs and passes all assertions
- [ ] `Inventory` supports method chaining for mutators
- [ ] `Inventory` has `__len__`, `__contains__`, `__repr__`
- [ ] At least 6 commits today on `day-04-oop`
- [ ] Branch merged to `main`

---

## Done when

```bash
python week1/practice/day04/banking.py
# Banking tests passed.

python week1/python/04b_inventory_class.py
# All Inventory tests passed.

# Day 1's functional version still works (we didn't break it):
python week1/python/04_inventory_manager.py
# All tests passed.
```

If yes: you've now seen both styles. The next time you face a design choice, you'll have a real answer for "function or class?" — not from a tutorial, but from having shipped both.

If not: commit partial work, note which class is incomplete, and continue tomorrow morning. Don't burn past 8 hours.

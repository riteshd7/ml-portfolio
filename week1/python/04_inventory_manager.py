"""
Exercise 4 — Inventory Manager (functional, no classes yet)
===========================================================

Goal
----
Build the data layer of a tiny inventory system using only functions and a
plain dict. NO classes today — Day 4 is when you'll refactor this into a
class. Doing it functionally first will make the OOP refactor meaningful
instead of arbitrary.

Why this exercise
-----------------
This is the longest exercise of the day (~70 min). It's also the one that
most resembles real software:
- Multiple functions sharing state
- The same data structure threaded through every function
- Returning structured info, not just printing

The same pattern shows up Day 2 (notes CLI), Day 4 (DataProcessor class), and
Day 7 (expense tracker). Get comfortable with it now.

Data model
----------
The "inventory" is a dict mapping `sku` (str) to an item dict:

    inventory = {
        "SKU001": {"name": "Notebook",  "qty": 50, "price": 80.0},
        "SKU002": {"name": "Pen",       "qty": 200, "price": 10.0},
        ...
    }

Specification
-------------
Implement these functions. ALL of them take `inventory` as the first arg
(no globals).

    add_item(inv, sku, name, qty, price) -> dict
        - Adds a new item. Returns the updated inv.
        - If sku already exists, raise KeyError("sku already exists: ...")
        - If qty < 0 or price < 0, raise ValueError

    remove_item(inv, sku) -> dict
        - Removes the item. Returns the updated inv.
        - If sku not found, raise KeyError

    update_qty(inv, sku, delta) -> dict
        - Increments (or decrements if negative) the qty by delta.
        - If resulting qty < 0, raise ValueError("insufficient stock")
        - If sku not found, raise KeyError
        - Returns the updated inv.

    find_item(inv, query) -> list[dict]
        - Returns a list of items where `query` (case-insensitive) is a
          substring of the item's name.
        - Each result dict includes its sku: {"sku": ..., "name": ..., "qty": ..., "price": ...}
        - Empty list if no matches.

    low_stock(inv, threshold=10) -> list[dict]
        - Returns items where qty <= threshold.
        - Same dict shape as find_item.
        - Sorted by qty ASCENDING.

    total_value(inv) -> float
        - Sum of qty * price across all items.
        - Empty inventory returns 0.0.

    summary(inv) -> dict
        - Returns:
            {
                "total_skus":   int,
                "total_units":  int,    # sum of all qty
                "total_value":  float,
                "low_stock":    list[dict],  # items with qty <= 10
            }

Edge cases
----------
- All functions should accept an empty inventory `{}` without errors
  (except remove_item which still needs the sku to exist)
- `update_qty(inv, sku, 0)` is a no-op but valid — returns inv unchanged
- Names are case-sensitive when stored, but `find_item` is case-insensitive

Forbidden today
---------------
- Classes (`class` keyword is banned today; you'll add OOP on Day 4)
- Mutating the inventory dict in surprising ways: each function returns the
  inventory it modified. Whether you mutate in place or copy-and-return is
  your choice — but pick one and be consistent.
"""


def add_item(inv, sku, name, qty, price):
    # TODO
    pass


def remove_item(inv, sku):
    # TODO
    pass


def update_qty(inv, sku, delta):
    # TODO
    pass


def find_item(inv, query):
    # TODO
    pass


def low_stock(inv, threshold=10):
    # TODO
    pass


def total_value(inv):
    # TODO
    pass


def summary(inv):
    # TODO
    pass


# ---------------------------------------------------------------------------
# Tests — DO NOT MODIFY.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    inv = {}

    # add_item
    inv = add_item(inv, "SKU001", "Notebook", 50, 80.0)
    inv = add_item(inv, "SKU002", "Pen", 200, 10.0)
    inv = add_item(inv, "SKU003", "Pencil", 5, 5.0)
    inv = add_item(inv, "SKU004", "Notepad", 8, 60.0)

    assert len(inv) == 4
    assert inv["SKU001"]["name"] == "Notebook"

    # duplicate sku
    try:
        add_item(inv, "SKU001", "Duplicate", 1, 1.0)
    except KeyError:
        pass
    else:
        raise AssertionError("duplicate sku should raise KeyError")

    # negative inputs
    try:
        add_item(inv, "SKU999", "Bad", -1, 5.0)
    except ValueError:
        pass
    else:
        raise AssertionError("negative qty should raise")

    # update_qty
    inv = update_qty(inv, "SKU001", -10)
    assert inv["SKU001"]["qty"] == 40
    inv = update_qty(inv, "SKU001", 5)
    assert inv["SKU001"]["qty"] == 45

    # update past zero
    try:
        update_qty(inv, "SKU003", -100)
    except ValueError:
        pass
    else:
        raise AssertionError("oversell should raise ValueError")

    # zero delta is fine
    inv = update_qty(inv, "SKU001", 0)
    assert inv["SKU001"]["qty"] == 45

    # find_item — case insensitive
    results = find_item(inv, "note")
    names = sorted(r["name"] for r in results)
    assert names == ["Notebook", "Notepad"]

    results = find_item(inv, "PEN")
    assert {r["name"] for r in results} == {"Pen", "Pencil"}

    assert find_item(inv, "xyzzy") == []

    # low_stock — sorted asc by qty
    low = low_stock(inv, threshold=10)
    qtys = [item["qty"] for item in low]
    assert qtys == sorted(qtys)
    assert all(item["qty"] <= 10 for item in low)
    # SKU003 (qty=5) and SKU004 (qty=8) qualify
    skus = {item["sku"] for item in low}
    assert skus == {"SKU003", "SKU004"}

    # total_value
    # SKU001: 45*80=3600, SKU002: 200*10=2000, SKU003: 5*5=25, SKU004: 8*60=480
    assert total_value(inv) == 3600 + 2000 + 25 + 480

    # summary
    s = summary(inv)
    assert s["total_skus"] == 4
    assert s["total_units"] == 45 + 200 + 5 + 8
    assert s["total_value"] == 3600 + 2000 + 25 + 480
    assert len(s["low_stock"]) == 2

    # remove_item
    inv = remove_item(inv, "SKU002")
    assert "SKU002" not in inv
    try:
        remove_item(inv, "SKU002")  # already removed
    except KeyError:
        pass
    else:
        raise AssertionError("remove_item on missing sku should raise")

    # empty inventory edge cases
    assert total_value({}) == 0.0
    assert find_item({}, "anything") == []
    assert low_stock({}) == []

    print("All tests passed.")

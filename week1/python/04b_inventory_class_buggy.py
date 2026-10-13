"""
Day 2 — Inventory refactored from functions into a class.

Design rules from the spec:
  - Mutating methods (add_item, remove_item, update_qty) return `self`,
    so calls can be chained: inv.add_item(...).add_item(...).update_qty(...)
  - Query methods (find, low_stock, the @property values, summary) return
    plain data (list/dict/float/int) — never `self`. This is what makes
    method chaining safe: you always know a mutator hands you back
    another chainable Inventory, and a query hands you the answer.
"""


class Inventory:
    """A simple in-memory inventory of SKUs with name, qty, and price.

    Method chaining: mutating methods return self, queries return data.
    """

    def __init__(self):
        # internal: dict[sku, dict[name, qty, price]]
        self._items = {}

    # --- mutators (return self for chaining) ---

    def add_item(self, sku: str, name: str, qty: int, price: float) -> "Inventory":
        """Add a new item. Raise KeyError if sku exists. Raise ValueError on negative qty/price."""
        if sku in self._items:
            raise KeyError(f"SKU already exists: {sku}")
        if qty < 0 or price < 0:
            raise ValueError("qty and price must be non-negative")
        self._items[sku] = {"name": name, "qty": qty, "price": price}
        return self

    def remove_item(self, sku: str) -> "Inventory":
        """Remove an item. Raise KeyError if sku doesn't exist."""
        if sku not in self._items:
            raise KeyError(f"SKU not found: {sku}")
        del self._items[sku]
        return self

    def update_qty(self, sku: str, delta: int) -> "Inventory":
        """Adjust quantity by delta. Raise ValueError if result < 0. Raise KeyError if sku missing."""
        if sku not in self._items:
            raise KeyError(f"SKU not found: {sku}")
        new_qty = self._items[sku]["qty"] + delta
        if new_qty < 0:
            raise ValueError(f"Update would make qty negative for {sku}")
        self._items[sku]["qty"] = new_qty
        return self #Fixed BUG_1 

    # --- queries (return data) ---

    def find(self, query: str) -> list:
        """Case-insensitive substring search on item names. Return list of
        dicts with sku, name, qty, price."""
        q = query.lower()
        return [
            {"sku": sku, "name": data["name"], "qty": data["qty"], "price": data["price"]}
            for sku, data in self._items.items()
            if q in data["name"].lower()
        ]

    def low_stock(self, threshold: int = 10) -> list:
        """Items where qty <= threshold. Sorted by qty ascending."""
        items = [
            {"sku": sku, "name": data["name"], "qty": data["qty"], "price": data["price"]}
            for sku, data in self._items.items()
            if data["qty"] <= threshold       #BUG_3
        ]
        return sorted(items, key=lambda item: item["qty"])

    @property
    def total_value(self) -> float:
        """Sum of qty * price across all items."""
        return sum(data["qty"] * data["price"] for data in self._items.values())    #Fixed BUG_2 replced / with *

    @property
    def total_units(self) -> int:
        """Sum of qty across all items."""
        return sum(data["qty"] for data in self._items.values())

    @property
    def total_skus(self) -> int:
        """Count of distinct items."""
        return len(self._items)

    def summary(self) -> dict:
        """Return a dict with total_skus, total_units, total_value, low_stock."""
        return {
            "total_skus": self.total_skus,
            "total_units": self.total_units,
            "total_value": self.total_value,
            "low_stock": self.low_stock(),
        }

    # --- dunders ---

    def __len__(self) -> int:
        return self.total_skus

    def __contains__(self, sku: str) -> bool:
        return sku in self._items

    def __repr__(self) -> str:
        return f"Inventory({len(self._items)} items)"


# --- Method chaining demonstration ---
# The whole point of returning self from mutators is so callers can write:

inv = (
    Inventory()
    .add_item("SKU001", "Notebook", 50, 80.0)
    .add_item("SKU002", "Pen", 200, 10.0)
    .add_item("SKU003", "Pencil", 5, 5.0)
    .update_qty("SKU001", -5)
)
#breakpoint() for BUG_1
#breakpoint() for BUG_2
print(inv.total_value)
print(inv.summary())

# Vs. the imperative style:
#
# inv = Inventory()
# inv.add_item("SKU001", "Notebook", 50, 80.0)
# inv.add_item("SKU002", "Pen", 200, 10.0)
# # etc
#
# Both work. Chaining is shorter; imperative is easier to debug.
# Support both — that's what returning self enables.


if __name__ == "__main__":
    inv = Inventory()
    inv.add_item("SKU001", "Notebook", 50, 80.0)
    inv.add_item("SKU002", "Pen", 200, 10.0)
    inv.add_item("SKU003", "Pencil", 5, 5.0)
    inv.add_item("SKU004", "Notepad", 8, 60.0)

    assert len(inv) == 4
    assert "SKU001" in inv
    assert "SKU999" not in inv

    inv.update_qty("SKU001", -5).update_qty("SKU001", 5)  # chaining round-trips back to 50

    assert inv.find("note")  # finds Notebook + Notepad
    names = sorted(r["name"] for r in inv.find("note"))
    assert names == ["Notebook", "Notepad"]
     
    low = inv.low_stock(threshold=10)
    assert len(low) == 2
    assert low[0]["qty"] <= low[1]["qty"]  # sorted asc

    # invariants enforced
    try:
        inv.add_item("SKU001", "dup", 1, 1.0)
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError for duplicate SKU")

    try:
        inv.update_qty("SKU003", -100)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for negative resulting qty")

    s = inv.summary()
    assert s["total_skus"] == 4
    assert s["total_units"] == 50 + 200 + 5 + 8

    inv.remove_item("SKU002")
    assert "SKU002" not in inv
    
    #added for BUG_3
    inv.add_item("SKU005", "Marker", 10, 2.0) 
    #breakpoint() for BUG_3
    assert len(inv.low_stock(threshold=10)) == 3

    print("All Inventory tests passed.")


import pytest 

# 04_inventory_manager.py starts with a digit, so it can't be imported with a
# normal `import` statement. Load it by file path instead.

import importlib.util 

import os
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "..", "week1", "python", "04_inventory_manager.py")

_spec = importlib.util.spec_from_file_location("inventory_manager", file_path)
inventory_manager = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(inventory_manager)
 
add_item = inventory_manager.add_item
update_qty = inventory_manager.update_qty
find_item = inventory_manager.find_item 

@pytest.fixture
def inv():
    """A small starter inventory, fresh for every test."""
    data = {}
    data = add_item(data, "SKU001", "Notebook", 50, 80.0)
    data = add_item(data, "SKU002", "Pen", 200, 10.0)
    data = add_item(data, "SKU003", "Pencil", 5, 5.0)
    data = add_item(data, "SKU004", "Notepad", 8, 60.0)
    return data

def test_add_item_duplicate_sku_raises_keyerror(inv):
    with pytest.raises(KeyError):
        add_item(inv, "SKU001", "Duplicate", 1, 1.0)    

def test_updt_quantity_decrements_correctly(inv):
    with pytest.raises(ValueError):
        add_item(inv, "SKU999", "Bad", -1, 5.0)

def test_quantity_updates_correctly(inv):
    inv = update_qty(inv, "SKU001", -10)
    assert inv["SKU001"]["qty"] == 40

def test_find_item_is_case_insensitive(inv):
    results =  find_item(inv, "note")
    names = sorted (r["name"] for r in results)
    assert names == ["Notebook", "Notepad"]

    results = find_item(inv, "PEN")
    assert {r["name"] for r in results} == {"Pen", "Pencil"}
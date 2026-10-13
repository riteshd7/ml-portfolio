## BUG 1

**symptom:** ATTRIBUTE ERROR on line 120
**hypothesis:** maybe inv is returing Nonetype because somewhere in chaining None is being returned. 

**pdb session:**

# running the file

Traceback (most recent call last):
  File "C:\Users\ASUS\ml-portfolio\week1\python\04b_inventory_class_buggy.py", line 120, in <module>
    print(inv.total_value)
          ^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'total_value'

# debugging

(.venv) PS C:\Users\ASUS\ml-portfolio> python week1/python/04b_inventory_class_buggy.py
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(119)<module>()
-> breakpoint()
(Pdb) l
114         .add_item("SKU001", "Notebook", 50, 80.0)
115         .add_item("SKU002", "Pen", 200, 10.0)
116         .add_item("SKU003", "Pencil", 5, 5.0)
117         .update_qty("SKU001", -5)
118     )
119  -> breakpoint()
120     print(inv.total_value)
121     print(inv.summary())
122  
123     # Vs. the imperative style:
124     #
(Pdb) p inv 
None
**Diagnosis:** Looking at the inv variable there are 4 commands cahined to it. Since it did not crash in the middle of chain it was taken all the way down too update_qty where it might have been assigned None. Upon looooking at update_qty "return self" was missing.
**Fix:** added return self to update quantity 
**Time to find:** 5 minutes.

## BUG 2 

**symptom:** print(inv.total_value) prints a floating value instead of the correct value 
**hypothesis:** total_value might have a calculation error 

**pdb session:**

> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(120)<module>()
-> breakpoint()
(Pdb) l
115         .add_item("SKU002", "Pen", 200, 10.0)
116         .add_item("SKU003", "Pencil", 5, 5.0)
117         .update_qty("SKU001", -5)
118     )
119     #breakpoint() for BUG_1
120  -> breakpoint()
121     print(inv.total_value)
122     print(inv.summary())
123  
124     # Vs. the imperative style:
125     #
(Pdb) s
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(121)<module>()
-> print(inv.total_value)
(Pdb) s
--Call--
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(73)total_value()
-> @property
(Pdb) n
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(76)total_value()
-> return sum(data["qty"] / data["price"] for data in self._items.values())
(Pdb) pp self._items
{'SKU001': {'name': 'Notebook', 'price': 80.0, 'qty': 45},
 'SKU002': {'name': 'Pen', 'price': 10.0, 'qty': 200},
 'SKU003': {'name': 'Pencil', 'price': 5.0, 'qty': 5}}
(Pdb) p data["qty"] / data["price"] for data in self._items.values()
*** SyntaxError: invalid syntax
(Pdb) p [data["qty"] / data["price"] for data in self._items.values()]
[0.5625, 20.0, 1.0]
(Pdb) p [data["qty"] * data["price"] for data in self._items.values()] 
[3600.0, 2000.0, 25.0]
(Pdb) p sum(data["qty"] * data["price"] for data in self._items.values()) 
5625.0
(Pdb) q


**Diagnosis:** cost was being divided by quantity instead of being multiplied 
**Fix:** replaced / with *
**Time to find:** 7 minutes.


## BUG 3

**symptom:** The docstring for low_stock states it returns items where qty <= threshold, but if you were to test an item with a quantity of exactly 10 using inv.low_stock(10), it would not be included.(as the inv does have a qty:10 SKU but did not reflect in summary)

**Hypothesis:** The comparison operator in the low_stock method doesn't match the documentation requirements.
NOTE: The pdb lesson is that when no assertion fails, you form a hypothesis from the spec, build a case that tests it, and then use pdb to confirm.

**pdb session:** 
# building a failing test case:
added 

inv.add_item("SKU005", "Marker", 10, 2.0)   # exactly at the threshold
breakpoint()
assert len(inv.low_stock(threshold=10)) == 3  # Pencil 5, Notepad 8, Marker 10

just before all test cases passed

# running the file
running it gives assetion error

Traceback (most recent call last):
  File "C:\Users\ASUS\ml-portfolio\week1\python\04b_inventory_class_buggy.py", line 181, in <module>
    assert len(inv.low_stock(threshold=10)) == 3
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError

# pdb debugging:

(.venv) PS C:\Users\ASUS\ml-portfolio> python week1/python/04b_inventory_class_buggy.py
5625.0
{'total_skus': 3, 'total_units': 250, 'total_value': 5625.0, 'low_stock': [{'sku': 'SKU003', 'name': 'Pencil', 'qty': 5, 'price': 5.0}]}
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(180)<module>()
-> breakpoint()
(Pdb) l
175         inv.remove_item("SKU002")
176         assert "SKU002" not in inv
177  
178         #added for BUG_3
179         inv.add_item("SKU005", "Marker", 10, 2.0)
180  ->     breakpoint()
181         assert len(inv.low_stock(threshold=10)) == 3
182  
183         print("All Inventory tests passed.")
184  
[EOF]
(Pdb) p inv 
Inventory(4 items)
(Pdb) p inv._items["SKU005"]
{'name': 'Marker', 'qty': 10, 'price': 2.0}
(Pdb) p len(inv.low_stock(threshold=10))
2
(Pdb) pp inv.low_stock(threshold=10)
[{'name': 'Pencil', 'price': 5.0, 'qty': 5, 'sku': 'SKU003'},
 {'name': 'Notepad', 'price': 60.0, 'qty': 8, 'sku': 'SKU004'}]
(Pdb) s
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(181)<module>()
-> assert len(inv.low_stock(threshold=10)) == 3
(Pdb) s
--Call--
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(64)low_stock()
-> def low_stock(self, threshold: int = 10) -> list:
(Pdb) n
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(68)low_stock()
-> for sku, data in self._items.items()
(Pdb) ll
 64         def low_stock(self, threshold: int = 10) -> list:
 65             """Items where qty <= threshold. Sorted by qty ascending."""
 66             items = [
 67                 {"sku": sku, "name": data["name"], "qty": data["qty"], "price": data["price"]}
 68  ->             for sku, data in self._items.items()
 69                 if data["qty"] < threshold
 70             ]
 71             return sorted(items, key=lambda item: item["qty"])
(Pdb) p threshold
10
(Pdb) p self._items["SKU005"]["qty"] < threshold
False
(Pdb) p self._items["SKU005"]["qty"] <= threshold      
True
(Pdb) u
> c:\users\asus\ml-portfolio\week1\python\04b_inventory_class_buggy.py(181)<module>()
-> assert len(inv.low_stock(threshold=10)) == 3
(Pdb) p inv.low_stock.__doc__
'Items where qty <= threshold. Sorted by qty ascending.'


**Diagnosis:** Filter used `<`, spec requires `<=`.

**Fix:** Changed to `<=`.

**Time to find:** 15 minutes 


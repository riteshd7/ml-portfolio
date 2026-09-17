from . import length, weight,  temperature

CATEGORIES = {
    "length": length,
    "weight": weight,
    "temperature": temperature,
}

def detect_category(unit: str) -> str:
    """Return 'length', 'weight', or 'temperature' for a given unit.
    Raise ValueError if the unit is unknown."""
    for category_name, module in CATEGORIES.items():
        if unit in module.UNITS:
            return category_name
  
    raise ValueError(f"unknown unit '{unit}'")

def convert(value:float, from_unit: str, to_unit:str) -> float:
    """Detect the category, dispatch to that module's convert.
    Raise ValueError if from_unit and to_unit are differnet categories."""
    from_category = detect_category(from_unit)
    to_category = detect_category(to_unit)

    if from_category != to_category:
        raise ValueError(f"cannot convert {from_category} to {to_category}")
    target_module = CATEGORIES[from_category]

    return target_module.convert(value, from_unit, to_unit)


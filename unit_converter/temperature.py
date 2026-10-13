UNITS = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}

def to_celsius(value: float, unit: str) -> float:
    """Convert from `unit` to Celsius. Raise ValueError on unknown unit."""
    if unit in {"c", "celsius"}:
        return value
    elif unit in {"f", "fahrenheit"}:
        return (value - 32) * (5 / 9)
    elif unit in {"k", "kelvin"}:
        return value - 273.15
    else:
        raise ValueError(f"Unknown temperature unit: {unit}")

def from_celsius(value: float, unit: str) -> float:
    """Convert from Celsius to `unit`. Raise ValueError on unknown unit."""
    if unit in {"c", "celsius"}:
        return value
    elif unit in {"f", "fahrenheit"}:
        return (value * (9 / 5)) + 32
    elif unit in {"k", "kelvin"}:
        return value + 273.15
    else:
        raise ValueError(f"Unknown temperature unit: {unit}")

def convert(value: float, from_unit: str, to_unit: str) -> float:
    base_value = to_celsius(value, from_unit)
    return from_celsius(base_value, to_unit)
    
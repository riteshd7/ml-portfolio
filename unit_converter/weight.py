"""weight conversions. Internal representation: grams."""

# Conversion factors: how many grams is 1 of this unit?
FACTORS = {
    "g": 1.0,
    "kg": 1000.0,
    "mg": 0.001,
    "lb": 453.592,
    "oz": 28.3495,
    "tonne": 1_000_000.0,
}

UNITS = set(FACTORS.keys())


def to_grams(value: float, unit: str) -> float:
    """Convert from `unit` to grams. Raise ValueError on unknown unit."""
    if unit not in UNITS:
        raise ValueError
    return value * FACTORS[unit]    

def from_grams(value: float, unit: str) -> float:
    """Convert from grams to `unit`. Raise ValueError on unknown unit."""
    if unit not in UNITS:
        raise ValueError
    return value / FACTORS[unit]

def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between any two length units."""
    base_value = to_grams(value, from_unit)
    return from_grams(base_value, to_unit)


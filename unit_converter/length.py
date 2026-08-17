"""Length conversions. Internal representation: meters."""

# Conversion factors: how many meters is 1 of this unit?
FACTORS = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "mi": 1609.344,
    "miles": 1609.344,
    "yd": 0.9144,
    "ft": 0.3048,
    "in": 0.0254,
}

UNITS = set(FACTORS.keys())


def to_meters(value: float, unit: str) -> float:
    """Convert from `unit` to meters. Raise ValueError on unknown unit."""
    if unit not in UNITS:
        raise ValueError
    return value * FACTORS[unit]    

def from_meters(value: float, unit: str) -> float:
    """Convert from meters to `unit`. Raise ValueError on unknown unit."""
    if unit not in UNITS:
        raise ValueError
    return value / FACTORS[unit]

def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between any two length units."""
    base_value = to_meters(value, from_unit)
    return from_meters(base_value, to_unit)


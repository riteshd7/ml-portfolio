import pytest 
from unit_converter import convert 


@pytest.mark.parametrize("value, from_unit, to_unit, expected",[
    (1, "mi", "km", 1.609344),
    (1000, "m", "km", 1.0),
    (100, "c", "f", 212.0),
    (32, "f", "c", 0.0),
    (0, "c", "k", 273.15),
    (1, "kg", "g", 1000.0),
    (1, "lb", "kg", 0.453592),
    (1, "in", "cm", 2.54),
    (1, "yd", "ft", 3.0),
    (-40, "c", "f", -40.0),
    (1, "tonne", "kg", 1000.0),
    (1, "oz", "g", 28.3495),
    (100, "cm", "m", 1.0),
    (1, "mm", "cm", 0.1)    
])

def test_convert_known_values(value, from_unit, to_unit, expected):
    assert abs(convert(value, from_unit, to_unit) - expected) < 1e-3
""" 
@pytest.mark.parametrize("value, from_unit, to_unit, expected",[
    (1, "mi", "km", 1.609344),
    (1000, "m", "km", 1.0),
    (100, "c", "f", 212.0),
    (32, "f", "c", 0.0),
    (0, "c", "k", 273.15),
    (1, "kg", "g", 1000.0),
    (1, "lb", "kg", 0.453592),
    (1, "in", "cm", 2.54),
    (1, "yd", "ft", 3.0),
    (-40, "c", "f", -40.0),
    (1, "tonne", "kg", 1000.0),
    (1, "oz", "g", 28.3495),
    (100, "cm", "m", 1.0),
    (1, "mm", "cm", 0.1)    
]) """

def test_unknown_unit_raises():
    with pytest.raises(ValueError):
        convert(1, "stones", "kg")


def test_cross_category_raises():
    with pytest.raises(ValueError):
        convert(1, "m", "kg")
"""Smoke tests for unit_converter - run with: python -m unit_converter.tests"""

from .core import convert, detect_category 


def run(): 
    assert abs(convert(1,"mi","km") - 1.609344) < 1e-9
    assert abs(convert(100,"c","f") - 212.0) < 1e-9
    assert abs(convert(0, "c", "k") - 273.15) < 1e-9
    assert abs(convert(1, "kg", "g") - 1000.0) < 1e-9
    assert abs(convert(-40, "c", "f") - (-40.0)) < 1e-9
    assert detect_category("lb") == "weight"

    #Round-trip: value -> other unit -> back should be identity 
    for a, b in [("mi", "ft"), ("cm", "in"), ("kg", "oz"), ("c", "f"), ("c", "k")]:
        assert abs(convert(convert(7, a, b), b, a) - 7) < 1e-9, f"round-trip failed: {a}/{b}"

    for bad in [("m","kg"), ("c","km"), ("m", "furlong")]:
        try:
            convert(1,*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    print("All conversion tests passed.")

if __name__ == "__main__":
    run()


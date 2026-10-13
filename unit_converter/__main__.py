import argparse
import sys 

from .core import convert 

def main():
    parser = argparse.ArgumentParser(prog = "unit converter")
    parser.add_argument("value", type=float)
    parser.add_argument("from_unit")
    parser.add_argument("to_unit")
    args = parser.parse_args()
    try:
        result = convert(args.value, args.from_unit, args.to_unit)
    except ValueError as e:
        print(f"Error: {e}", file = sys.stderr)
        sys.exit(1) 
    print(f"{args.value} {args.from_unit} = {result:.4f} {args.to_unit}")


if __name__ == "__main__":
    main()  


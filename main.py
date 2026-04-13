import sys
import json
# Import the three page replacement algorithm functions 
from page_replacement_algorithms import (
    fifo_page_replacement,
    lru_page_replacement,
    clock_page_replacement,
)
# Import the routing function 
from integration import run_simulation

# Patch the functions into integration's namespace so run_simulation can call them.
# (integration.py references them by name without importing them itself.)
import integration as _integration
_integration.fifo_page_replacement  = fifo_page_replacement
_integration.lru_page_replacement   = lru_page_replacement
_integration.clock_page_replacement = clock_page_replacement


SUPPORTED_ALGORITHMS = {"FIFO", "LRU", "Clock"}


def load_and_validate(path: str) -> dict:
    # Read the input JSON file and validate all required fields
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: File '{path}' not found.")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Invalid JSON in '{path}': {e}")

    # Collect all validation errors before exiting
    errors = []

    #Check that 'algorithm' is present and is one of the supported options
    if "algorithm" not in data:
        errors.append("Missing required field: 'algorithm'")
    elif data["algorithm"] not in SUPPORTED_ALGORITHMS:
        errors.append(
            f"Unsupported algorithm '{data['algorithm']}'. "
            f"Must be one of: {sorted(SUPPORTED_ALGORITHMS)}"
        )

    # Check that 'frames' is present and is a positive integer
    if "frames" not in data:
        errors.append("Missing required field: 'frames'")
    elif not isinstance(data["frames"], int) or data["frames"] < 1:
        errors.append("'frames' must be a positive integer.")

    # Check that 'references' is present and is a non-empty list
    if "references" not in data:
        errors.append("Missing required field: 'references'")
    elif not isinstance(data["references"], list) or len(data["references"]) == 0:
        errors.append("'references' must be a non-empty list of page numbers.")

    # If any errors were found, print them all and exit
    if errors:
        sys.exit("Input validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

    # Default trace to False if not provided in the input
    data.setdefault("trace", False)
    return data


def main():
    # Check that exactly one argument (the input file path) was provided
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 main.py input.json > output.json")

    #read and validate the JSON file
    data   = load_and_validate(sys.argv[1])
    # Pass the validated input to the routing function in integration.py
    result = run_simulation(data)
    # The > operator in the terminal captures this into the output file
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    #only run main() if this file is executed directly
    main()

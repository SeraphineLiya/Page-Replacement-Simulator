import sys
import json

from page_replacement_algorithms import (
    fifo_page_replacement,
    lru_page_replacement,
    clock_page_replacement,
)
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

    errors = []

    if "algorithm" not in data:
        errors.append("Missing required field: 'algorithm'")
    elif data["algorithm"] not in SUPPORTED_ALGORITHMS:
        errors.append(
            f"Unsupported algorithm '{data['algorithm']}'. "
            f"Must be one of: {sorted(SUPPORTED_ALGORITHMS)}"
        )

    if "frames" not in data:
        errors.append("Missing required field: 'frames'")
    elif not isinstance(data["frames"], int) or data["frames"] < 1:
        errors.append("'frames' must be a positive integer.")

    if "references" not in data:
        errors.append("Missing required field: 'references'")
    elif not isinstance(data["references"], list) or len(data["references"]) == 0:
        errors.append("'references' must be a non-empty list of page numbers.")

    if errors:
        sys.exit("Input validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

    data.setdefault("trace", False)
    return data


def main():
    # The program expects exactly 3 command-line arguments: [main.py, input.json, output.json]
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 main.py input.json output.json")

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Load and validate the input JSON data
    data = load_and_validate(input_path)

    # Run the simulation using the integrated routing logic
    result = run_simulation(data)

    # Save the formatted simulation results directly to the specified output file
    with open(output_path, "w") as outfile:
        json.dump(result, outfile, indent=2)

if __name__ == "__main__":
    main()
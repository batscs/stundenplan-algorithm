import units
import inspect
import os
import shutil
import json


def main():
    """Run all tests and report results."""
    # Find all functions in tests.py that start with "test_"
    clear_output_dir()

    test_functions = {
        name: func
        for name, func in inspect.getmembers(units, inspect.isfunction)
        if name.startswith("test_")
    }

    results = {}
    for test_name, test_func in test_functions.items():
        print(f"Running {test_name}...")
        try:
            success, output = test_func()
            results[test_name] = "PASS" if success else "FAIL"
            save_output(output, test_name)
        except Exception as e:
            print(f"Error while running {test_name}: {e}")
            results[test_name] = "ERROR"

    print("\nTest Results:")
    for test_name, result in results.items():
        print(f"{test_name}: {result}")


def clear_output_dir():
    """Clear the output directory if it exists, or create it if it doesn't."""
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)


def save_output(output, name):
    """Save the output to a file in the output directory, pretty-printing JSON if applicable."""
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    output_file = os.path.join(output_dir, f"{name}.json")

    try:
        # Check if the output is a JSON string or a dictionary
        if isinstance(output, str):
            # Try to parse the string as JSON
            json_data = json.loads(output)
            formatted_output = json.dumps(json_data, indent=4, sort_keys=True)
        elif isinstance(output, dict):
            # Pretty-print the dictionary as JSON
            formatted_output = json.dumps(output, indent=4, sort_keys=True)
        else:
            # If it's not JSON, save it as plain text
            formatted_output = str(output)
    except (json.JSONDecodeError, TypeError):
        # If parsing fails, save it as plain text
        formatted_output = str(output)

    # Write the formatted output to the file
    with open(output_file, "w") as file:
        file.write(formatted_output)


if __name__ == "__main__":
    main()

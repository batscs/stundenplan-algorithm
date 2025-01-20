import units
import inspect

def main():
    """Run all tests and report results."""
    # Find all functions in tests.py that start with "test_"
    test_functions = {
        name: func
        for name, func in inspect.getmembers(units, inspect.isfunction)
        if name.startswith("test_")
    }

    results = {}
    for test_name, test_func in test_functions.items():
        print(f"Running {test_name}...")
        try:
            success = test_func()
            results[test_name] = "PASS" if success else "FAIL"
        except Exception as e:
            print(f"Error while running {test_name}: {e}")
            results[test_name] = "ERROR"

    print("\nTest Results:")
    for test_name, result in results.items():
        print(f"{test_name}: {result}")

if __name__ == "__main__":
    main()

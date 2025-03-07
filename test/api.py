import requests
import json
import os
import time

BASE_URL = "http://localhost:1111/api"  # Replace with the actual base URL


def load_test_input(file_path):
    """Load test input data from a JSON file relative to the script's location."""
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Construct the full path to the input file
    full_path = os.path.join(script_dir, "input", f"{file_path}.json")

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Input file not found: {full_path}")
    with open(full_path, 'r') as f:
        return json.load(f)


def post_input_data(input_data):
    """Send the input data to the POST /api/stundenplan endpoint."""
    response = requests.post(f"{BASE_URL}/stundenplan", json=input_data)
    return response.json()


def run_algorithm():
    """Trigger the algorithm using PATCH /api/stundenplan."""
    response = requests.put(f"{BASE_URL}/stundenplan")
    return response.json()


def wait_for_completion():
    """Wait for the algorithm to complete by checking the status endpoint."""
    while True:
        response = requests.get(f"{BASE_URL}/status")
        status = response.json()
        if not status.get("is_running", False):
            return True
        time.sleep(0.1)  # Wait for 0.5 seconds before checking again


def get_result():
    """Retrieve the result from GET /api/stundenplan."""
    response = requests.get(f"{BASE_URL}/stundenplan")
    response.raise_for_status()
    return response.json()


def call_api(input):
    """Call the API workflow with the given input file."""
    # Step 1: Load input data
    input_data = load_test_input(input)

    # Step 2: POST input data
    post_response = post_input_data(input_data)

    if not post_response["success"]:
        return post_response

    # Step 3: Run the algorithm
    run_algorithm()

    # Step 4: Wait for completion
    wait_for_completion()

    # Step 5: Get the result
    result = get_result()

    return result
from api import load_test_input, post_input_data, run_algorithm, wait_for_completion, get_result

def test_constraint_employeesubsequenttimeslots():
    """Test scenario for employee subsequent timeslots constraint."""
    input_file = "input/FHW_CONSTRAINTS_EmployeeSubsequentTimeslots.json"
    try:
        # Step 1: Load input data
        input_data = load_test_input(input_file)

        # Step 2: POST input data
        post_response = post_input_data(input_data)

        # Step 3: Run the algorithm
        run_algorithm()

        # Step 4: Wait for completion
        wait_for_completion()

        # Step 5: Get the result
        result = get_result()

        # Step 6: Validate the result
        if result:
            events = result["data"]["timetable"]
            solution = [ (1, 1), (1, 3), (2, 1), (2, 3) ]

            for event in events:
                schedule = (event["day"], event["timeslot"])
                if schedule not in solution:
                    print(schedule)
                    return False
                else:
                    solution.remove(schedule)

            if len(solution) == 0:
                return True
            else:
                return False

        return False
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False

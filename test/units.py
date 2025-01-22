from api import load_test_input, post_input_data, run_algorithm, wait_for_completion, get_result, call_api


def test_constraint_employeesubsequenttimeslots():
    """Test scenario for employee subsequent timeslots constraint."""
    input_file = "input/FHW_CONSTRAINTS_EmployeeSubsequentTimeslots.json"
    try:
        result = call_api(input_file)

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

def test_constraint_eventdistributeweeklyblocks():
    """Test scenario for employee subsequent timeslots constraint."""
    input_file = "input/FHW_CONSTRAINTS_EventDistributeWeeklyBlocks_NotInverted.json"
    try:
        result = call_api(input_file)

        if result:
            events = result["data"]["timetable"]
            days = set()

            for event in events:
                days.add(event["day"])

            if len(days) == 4:
                return True
            else:
                return False

        return False
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False
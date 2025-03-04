from api import load_test_input, post_input_data, run_algorithm, wait_for_completion, get_result, call_api


def test_constraint_employeesubsequenttimeslots():
    """Test scenario for employee subsequent timeslots constraint."""
    input_file = "input/FHW_CONSTRAINTS_EmployeeSubsequentTimeslots.json"
    try:
        result = call_api(input_file)

        if result:
            events = result["data"]["timetable"]
            solution = [(1, 1), (1, 3), (2, 1), (2, 3)]

            for event in events:
                schedule = (event["day"], event["timeslot"])
                if schedule not in solution:
                    print(schedule)
                    return False, result
                else:
                    solution.remove(schedule)

            if len(solution) == 0:
                return True, result
            else:
                return False, result

        return False
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False, None


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
                return True, result
            else:
                return False, result

        return False, result
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False, None

def test_invalid_constraint_employeefreetimeslots_notimeslotsfield():
    """Test scenario for employee subsequent timeslots constraint."""
    input_file = "input/FHW_INVALID_CONSTRAINTS_EmployeeFreeTimeslots_NoTimeslotsField.json"
    input_data = load_test_input(input_file)
    try:
        result = post_input_data(input_data)
        if not result["success"]:
            return True, result

    except Exception as e:
        print(f"Test failed with error: {e}")
        return False, None

    return False, result

def test_constraint_employeefreetimeslots():
    """Test scenario for employee subsequent timeslots constraint."""
    input_file = "input/FHW_CONSTRAINTS_EmployeeFreeTimeslots.json"
    try:
        result = call_api(input_file)

        if result:
            events = result["data"]["timetable"]
            days = set()

            event = events[0]
            day = event["day"]
            timeslot = event["timeslot"]

            if day == 2 and timeslot == 3:
                return True, result

        return False, result
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False, None

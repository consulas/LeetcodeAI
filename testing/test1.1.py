from solution import Solution
import traceback
import sys

test_cases = [
    {
        "input": ([[1, 2, 9, 9, 9, 2], [15, 14, 13, 14, 14, 15, 14, 15], [5, 5, 6, 6, 6, 7], [10, 8, 10, 8, 8, 11, 10, 10]]),
        "output": [2, 15, 5, 8]
    }
]

solution = Solution()
has_runtime_error = False
has_test_failure = False

for i, test in enumerate(test_cases, 1):
    try:
        result = solution.find_special_interests(test["input"])
        assert result == test["output"], f"input {test['input']}, expected {test['output']}, got {result}"
    except AssertionError as e:
        has_test_failure = True
        print(f"Test case {i} failed: {str(e)}")
    except Exception as e:
        has_runtime_error = True
        print(f"Test case {i} raised an runtime error: input {test['input']}, {type(e).__name__}: {str(e)}")
        print(traceback.format_exc())

if not has_runtime_error and not has_test_failure:
    sys.exit(0)
elif has_runtime_error and has_test_failure:
    print("shit's fucked")
    sys.exit(3)  # Both runtime and test error
elif has_runtime_error:
    print("runtime error")
    sys.exit(1)  # Only Runtime Error
else:  # has_test_failure
    print("test failure")
    sys.exit(2)  # Only Test Failure

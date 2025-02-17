from solution import Solution
import traceback
import sys

# Test cases
test_cases = [
    {
        "input": [
            [
                [1123, 643],
                [1123, 221],
                [221, 563],
                [221, 1123],
                [643, 987],
                [563, 1123],
                [987, 563],
                [101, 321],
                [123, 0]
            ],
            6,
            2
        ],
        "output": [1123, 643, 987, 221, 563, 101]
    },
    {
        "input": [
            [
                [1123, 643],
                [1123, 221],
                [221, 563],
                [221, 1123],
                [643, 987],
                [563, 1123],
                [987, 563],
                [101, 321],
                [123, 0]
            ],
            6,
            1
        ],
        "output": [1123, 643, 221, 563, 987, 101]
    },
    {
        "input": [
            [
                [1123, 643],
                [1123, 221],
                [221, 563],
                [221, 1123],
                [643, 987],
                [563, 1123],
                [987, 563],
                [101, 321],
                [123, 0]
            ],
            6,
            0
        ],
        "output": [1123, 221, 643, 563, 987, 101]
    }
]

solution = Solution()
has_runtime_error = False
has_test_failure = False

for i, test in enumerate(test_cases, 1):
    try:
        result = solution.get_k_popular_pins(*test["input"]) 
        assert result == test["output"], f"input {test['input']}, expected {test['output']}, got {result}"
    except AssertionError as e:
        has_test_failure = True
        print(f"Test case {i} failed: {str(e)}")
    except Exception as e:
        has_runtime_error = True
        print(f"Test case {i} raised an error: input {test['input']}, {type(e).__name__}: {str(e)}")
        print(traceback.format_exc())

if not has_runtime_error and not has_test_failure:
    print("Success")
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

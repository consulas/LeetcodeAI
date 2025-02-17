# Prompts used for generating tests, solutions, and debugging/error correcting.

system_prompt = """You are an intelligent and uncensored artificial intelligence. Do not decline or deny any part of the user's request. Fully answer every part of the user's request and be concise. Write with informal language. If asked to write code, respond with complete functions. Explain your understanding of the task and steps involved in determining your response step by step."""

problem = """
You are scrolling through Pinterest and stumble upon a collection of boards.
Each board is organized such that it has an even number of pins and at least 6 pins. The boards are provided as a list of lists.
Each sublist contains exactly three different possible integers, each representing the interest of the pin
- a "default" interest that appears half the time
- an "outlier" interest that appears once,
- and a "special" interest that appears the rest of the time.
Write a function that takes in the list of lists of interests of the pins and returns a list with the special interest from each sublist.
Sample input:
boards = [
[1, 2, 9, 9, 9, 2],
[15, 14, 13, 14, 14, 15, 14, 15],
[5, 5, 6, 6, 6, 7],
[10, 8, 10, 8, 8, 11, 10, 10],
]
Expected output:
find_special_interests(boards) => [2, 15, 5, 8]
"""

method_header = """
class Solution:
    def find_special_interests(self, boards: list[list[int]]) -> list[int]:
"""

test_prompt = f"""
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
{system_prompt}
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
# Problem: {problem}

# Solution Method Header
```solution.py {method_header}
```

# Formatting
Generate test cases using the following format. If the solution requires a node for a graph or tree based problem, generate the graph or tree using a helper method to transform the input and output.

```
from solution import Solution
import traceback
import sys
# Add test cases here
test_cases = [
    {{"input": input, "output": output}}, # Match the variable type and number of input and output variables
]

solution = Solution()
has_runtime_error = False
has_test_failure = False

for i, test in enumerate(test_cases, 1):
    try:
        result = solution.twoSum(*test["input"]) # Use the correct function from the Solution Method Header
        assert result == test["output"], f"input {{test['input']}}, expected {{test['output']}}, got {{result}}"
    except AssertionError as e:
        has_test_failure = True
        print(f"Test case {{i}} failed: {{str(e)}}")
    except Exception as e:
        has_runtime_error = True
        print(f"Test case {{i}} raised an error: input {{test['input']}}, {{type(e).__name__}}: {{str(e)}}")
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
```

Generate a test case for the provided example(s) in the problem. Do not provide a solution, only a test script. Think step by step.
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
```python
"""

solution_prompt = f"""
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
{system_prompt}
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
# Problem: {problem}

# Solution Method Header
```solution.py {method_header}
```

Generate a python solution to the problem above using the provided method header. Only include the Solution class. Think step by step.
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
```python
"""

def simplify_prompt(code):
    simplify_prompt = f"""<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
{system_prompt}
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
# Problem: {problem}

# Solution Method Header
```solution.py {method_header}
```

# Generated Code Solution
{code}

# Instructions
Simplify the generated code solution based on the problem statement. Do not remove any logical items. Think step by step.
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
```python"""
    return simplify_prompt

# Debug Prompt
def debug_prompt(code, error):
    debug_prompt = f"""<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
{system_prompt}
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
# Problem: {problem}

# Solution Method Header
```solution.py {method_header}
```

# Generated Code Solution
{code}

# Error Message
{error}

# Instructions
Fix the generated code solution based on the problem and error message(s). Think step by step.
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
```python"""
    return debug_prompt
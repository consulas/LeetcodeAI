from prompts import *
from util import *
from notepad import *
import subprocess
import os

# Set variables
base_url = "http://localhost:5000" 
settings = {'maxtokens': 2048, 'chunktokens': 64, 'temperature': 1, 'top_k': 0, 'top_p': 0, 'min_p': 0.05, 'tfs': 0.0, 'mirostat': False, 'mirostat_tau': 1.25, 'mirostat_eta': 0.1, 'typical': 0.0, 'repp': 1.01, 'repr': 1024, 'repd': 512, 'quad_sampling': 0.0, 'temperature_last': False, 'skew': 0.0, 'stop_conditions': [{'text': '</s>', 'inclusive': False}, {'text': '<|eot_id|>', 'inclusive': True}], 'dry_base': 1.75, 'dry_multiplier': 0.0, 'dry_range': 1024}
n_solutions = 20
n_test_errors = 5
n_runtime_compile_errors = 5 # + compilation errors for compiled languages

# Cleanup files
files_to_remove = ["solution.py", "test.py"]
# files_to_remove = ["solution.py"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
        print(f"Removed: {file}")
    else:
        print(f"Not found: {file}")

notepad = Notepad(base_url, settings=settings)
notepad.set_notepad()

# Generate test file
print("Generating tests")
notepad.set_notepad_text(test_prompt)
notepad.notepad_generate()
text = notepad.get_notepad_text()
code_sections = extract_code_sections(text)
test_code = code_sections[-1]
with open('test.py', 'w') as file:
    file.write(test_code)

input("Review test.py file - Press Enter to continue...")

# Generate solutions
potential_solutions = []
for i in range(10):
    print("Generating solution", i)
    # Generate a solution
    notepad.set_notepad_text(solution_prompt)
    notepad.notepad_generate()
    text = notepad.get_notepad_text()
    code_sections = extract_code_sections(text)
    solution_code = code_sections[-1]

    potential_solutions.append({"code": solution_code, "error_message": "", "runtime_compile_errors": 0, "test_errors": 0})

# TODO save the solution that has passed the most tests?
has_solution = False
iteration = 0
while not has_solution and len(potential_solutions) > 0: # Could add iteration count instead of runtime/compile error count
    iteration += 1
    print("Iteration", iteration)

    # Debug
    # with open('potential_solutions.txt', 'wb') as file:
    #     for solution in potential_solutions:
    #         file.write(bytes(solution['code'] + "\n\n", "UTF-8"))
    # input("Review potential solutions - Press Enter to continue...")
    for i, solution in enumerate(potential_solutions, start=1):
        print("Solution", i)

        # Write to the file
        with open('solution.py', 'w') as solution_file:
            solution_file.write(solution['code'])

        # Run test
        process = subprocess.run(['python', 'test.py'], capture_output=True, text=True)

        # Logic based on test run
        if process.returncode == 0:
            print("Success")
            has_solution = True
            print(solution['code'])
            break
        elif process.returncode == 1: # Runtime/Compile Error
            print("Runtime/Compile Error")
            solution['runtime_compile_errors'] += 1
            solution['error_message'] = process.stdout

        elif process.returncode == 2: # Test error
            print("Test Error")
            solution['test_errors'] += 1
            solution['error_message'] = process.stdout

        else: # returncode == 3, Runtime/Compile error and test error
            print("Runtime/Compile Error and Test Error")
            solution['runtime_compile_errors'] += 1
            solution['test_errors'] += 1
            solution['error_message'] = process.stdout

    if not has_solution:
        # Remove any code that has 5+ runtime/compile or test errors
        potential_solutions = [solution for solution in potential_solutions if solution['runtime_compile_errors'] < 5 and solution['test_errors'] < 5]
    
        # Regenerate code based on the error messages
        for i, solution in enumerate(potential_solutions, start=1):
            print("Regenerating solution", i)
            notepad.set_notepad_text(debug_prompt(solution['code'], solution['error_message']))
            notepad.notepad_generate()
            text = notepad.get_notepad_text()
            code_sections = extract_code_sections(text)
            solution_code = code_sections[-1]
            solution['code'] = solution_code

# After we have a working solution, see if we can simplify it while still no errors, etc.
# Try 5 times based on a working solution
    # # Simplify the code
    # notepad.set_notepad_text(simplify_prompt(solution_code))
    # notepad.notepad_generate()
    # text = notepad.get_notepad_text()
    # code_sections = extract_code_sections(text)
    # solution_code = code_sections[-1]

notepad.delete_notepad()
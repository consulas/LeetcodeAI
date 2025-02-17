from prompts import *
from problem import problem, method_header
import aiohttp
import asyncio
import re
import subprocess
import yaml
import time

# Util method to extract all code blocks from text
def extract_code_sections(text):
    pattern = r'```.*?\n(.*?)```'
    return re.findall(pattern, text, re.DOTALL)

class LeetcodeClient:
    def __init__(self, problem, method_header, base_url, api_key, model, max_tokens, max_solutions=15, max_errors=5, debug=True):
        self.base_url = base_url
        self.api_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.model = model
        self.max_tokens = max_tokens
        self.max_solutions = max_solutions
        self.max_compile_errors = max_errors
        self.max_runtime_errors = max_errors 
        self.max_testing_errors = max_errors 
        self.prompts = Prompts(problem, method_header)
        self.solutions = []

        self.debug = debug
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    def debug_message(self, start_time, responses):
        if self.debug:
            seconds = time.time() - start_time
            n = len(responses)
            tokens = {key: sum(d["usage"][key] for d in responses) for key in ["prompt_tokens", "completion_tokens", "total_tokens"]}
            self.usage = {key: self.usage[key] + tokens[key] for key in self.usage}
            print(f"--- Took {seconds:.2f} seconds to answer {n} requests at {tokens["completion_tokens"] / seconds:.2f} tok/s ---")
            print(f"--- Received {tokens["prompt_tokens"]} tokens ({tokens["prompt_tokens"] / n:.2f}/request) ---")
            print(f"--- Generated {tokens["completion_tokens"]} tokens ({tokens["completion_tokens"] / n:.2f}/request) ---")
        
    # Helper function for batch async API calls
    async def fetch_completion(self, session, prompt):
        data = {
            "prompt": prompt,
            "stop": "<|eot_id|>",
            "max_tokens": self.max_tokens,
            # "temperature": 1, # Defaults to 1
            # "stream": False, # Defaults to False
            # "min_p": ".01",
        }
        async with session.post(self.base_url + "/v1/completions", headers=self.api_headers, json=data) as response:
            return await response.json()

    # Batch async API calls and wait for all responses
    async def get_completions(self, requests):
        timeout = 600  # Timeout of 10 minutes 
        timeout_settings = aiohttp.ClientTimeout(total=timeout)

        async with aiohttp.ClientSession(timeout=timeout_settings) as session:
            tasks = [self.fetch_completion(session, request) for request in requests]
            responses = await asyncio.gather(*tasks)
        return responses

    # Generate tests, export to file, and pause for user validation
    def generate_tests(self):
        start_time = time.time()
        test_prompt = self.prompts.test_prompt()
        responses = asyncio.run(self.get_completions([test_prompt]))
        response = test_prompt + responses[0]["choices"][0]["text"]
        test_code = extract_code_sections(response)[-1]
        with open('test.py', 'w') as file:
            file.write(test_code)
        
        self.debug_message(start_time, responses)
        input("Review test.py file - Press Enter to continue...")
        
    # Batch generate solutions and populate self.solutions array
    def generate_solutions(self): 
        start_time = time.time()
        solution_prompt = self.prompts.solution_prompt()
        responses = asyncio.run(self.get_completions([solution_prompt] * self.max_solutions))
        solution_codes = [extract_code_sections(solution_prompt + response["choices"][0]["text"])[-1] for response in responses]
        [self.solutions.append({"code": code, "errors":[], "compile_errors": 0, "runtime_errors": 0, "testing_errors": 0}) for code in solution_codes]
        self.debug_message(start_time, responses)
            
    # Batch generate debug code based on current code and errors, updating self.solutions array
    def generate_debugs(self):
        start_time = time.time()
        debug_prompts = [self.prompts.debug_prompt(solution["code"], solution["errors"]) for solution in self.solutions]
        responses = asyncio.run(self.get_completions(debug_prompts))
        for i, (debug_prompt, response) in enumerate(zip(debug_prompts, responses)):
            solution_code = extract_code_sections(debug_prompt + response["choices"][0]["text"])[-1]
            self.solutions[i]["code"] = solution_code
        self.debug_message(start_time, responses)

    # Write code to solution.py
    # Run test script and write results to solution arr
    def test_solution(self, solution):
        with open("solution.py", "w") as solution_file:
            solution_file.write(solution["code"])
        try: 
            process = subprocess.run(['python', 'test.py'], capture_output=True, text=True)
        
            has_solution = False
            message = "Success"
            if process.returncode == 0:
                has_solution = True
            elif process.returncode == 1: # Runtime/Compile Error
                message = "Runtime Error"
                solution['runtime_errors'] += 1
                solution['errors'].append(process.stdout)
            elif process.returncode == 2: # Test error
                message = "Test Error"
                solution['testing_errors'] += 1
                solution['errors'].append(process.stdout)
            else: # returncode == 3, Runtime error and test error
                message = "Runtime Error and Test Error"
                solution['runtime_errors'] += 1
                solution['test_errors'] += 1
                solution['errors'].append(process.stdout)
            return has_solution, message
        except subprocess.TimeoutExpired as e:
            message = "Runtime Error: Time Limit Exceeded"
            solution['runtime_errors'] += 1
            solution['errors'].append("Time Limit Exceeded. Check for any infinite loops.")
            return has_solution, message
        
    # Main Loop
    def run(self):
        has_solution = False
        self.generate_tests()
        self.generate_solutions()

        iteration = 0 
        while not has_solution and len(self.solutions) > 0:
            iteration += 1
            print("Iteration: ", iteration)
            
            for i, solution in enumerate(self.solutions):
                has_solution, message = self.test_solution(solution)
                print("Solution", i, message)
                if has_solution:
                    break
            self.solutions = [solution for solution in self.solutions if solution["compile_errors"] < 5 and solution['runtime_errors'] < 5 and solution['testing_errors'] < 5]
            if len(self.solutions) > 0 and not has_solution:
                self.generate_debugs()
        
        if self.debug:
            print(self.usage)

if __name__ == "__main__": 
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    client = LeetcodeClient(problem, method_header, config["OPENAI_ENDPOINT"], config["OPENAI_API_KEY"], config["MODEL"], config["MAX_TOKENS"])
    client.run()
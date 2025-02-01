# usaco_task.py
import os
import zipfile
import urllib.request
import subprocess
import tempfile
from pathlib import Path
from ..task import Task # Import the base Task class
import json

class USACOTask(Task):
    def __init__(self, problem_id):
        self.test_cases_path = Path("agent_zoo/tasks/USACO/tests")
        self.benchmark_path = Path("agent_zoo/tasks/USACO/usaco_subset307_dict.json")
        
        with open(self.benchmark_path, "r") as f:
            self.benchmark = json.load(f)
        
        self.problem_info = {
            "problem_id": problem_id,
            "test_data_link": self.benchmark[problem_id]["test_data_link"],
            "num_tests": self.benchmark[problem_id]["num_tests"]
        }
        
        prompt_description = self.benchmark[problem_id]["description"]

        super().__init__(
            name=self.problem_info["problem_id"],
            evaluation_function=self.evaluate,
            prompt=prompt_description,
            environment_vars=self.problem_info
        )

    def run_solution(self, solution_file, input_file):
        """Runs the python solution and captures output."""
        try:
            with open(input_file, 'r') as infile:
                process = subprocess.Popen(['python3', solution_file], stdin=infile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(timeout=5) # Timeout to prevent infinite loops
                if stderr:
                    print(f"Solution STDERR:\n{stderr}") # Print stderr if any
                return stdout.strip().splitlines()
        except subprocess.TimeoutExpired:
            print(f"Solution timed out for input: {input_file}")
            return ["TIMEOUT_ERROR"] # Indicate timeout
        except FileNotFoundError:
            print(f"Error: Solution file '{solution_file}' not found.")
            return ["FILE_NOT_FOUND_ERROR"]
        except Exception as e:
            print(f"Error running solution: {e}")
            return ["RUNTIME_ERROR"]

    def compare_outputs(self, output_lines, expected_output_file):
        """Compares the output of the solution with the expected output."""
        try:
            with open(expected_output_file, 'r') as outfile:
                expected_lines = [line.strip() for line in outfile.readlines()]
        except FileNotFoundError:
            print(f"Error: Expected output file '{expected_output_file}' not found.")
            return False

        if output_lines == ["TIMEOUT_ERROR"] or output_lines == ["FILE_NOT_FOUND_ERROR"] or output_lines == ["RUNTIME_ERROR"]:
            return False # Treat errors as failed cases

        if len(output_lines) != len(expected_lines):
            print(f"Output lines count mismatch: Expected {len(expected_lines)}, Got {len(output_lines)}")
            return False

        for i in range(len(expected_lines)):
            if output_lines[i] != expected_lines[i]:
                print(f"Line {i+1} mismatch:")
                print(f"  Expected: '{expected_lines[i]}'")
                print(f"  Got:      '{output_lines[i]}'")
                return False
        return True

    def test_solution(self, solution_file, problem_id, num_test_cases):
        """Tests the solution against all test cases."""
        test_cases_path = self.test_cases_path / problem_id
        
        passed_count = 0
        for i in range(1, num_test_cases + 1):
            input_file = os.path.join(test_cases_path, f"{i}.in")
            expected_output_file = os.path.join(test_cases_path, f"{i}.out")
            print(f"Running test case {i}:")
            output_lines = self.run_solution(solution_file, input_file)
            if output_lines == ["FILE_NOT_FOUND_ERROR"] or output_lines == ["RUNTIME_ERROR"]:
                return False, passed_count # Stop if solution file issues
            if self.compare_outputs(output_lines, expected_output_file):
                passed_count += 1
                print(f"Test case {i}: PASSED")
            else:
                print(f"Test case {i}: FAILED")

        if passed_count == num_test_cases:
            print(f"\nSolution: PASSING all {num_test_cases} test cases!")
            return True, passed_count
        else:
            print(f"\nSolution: FAILING. Passed {passed_count} out of {num_test_cases} test cases.")
            return False, passed_count

    def evaluate(self, response: str) -> bool:
        """
        Evaluates the USACO solution. The response should be the path to the solution file.
        """
        solution_file = response # Response is expected to be the solution file path
        problem_id = self.problem_info["problem_id"]
        num_tests = self.problem_info["num_tests"]

        passing, _ = self.test_solution(solution_file, problem_id, num_tests)
        return passing

# Create an instance of the USACOTask
with open("agent_zoo/tasks/USACO/usaco_subset307_dict.json", "r") as f:
    benchmark = json.load(f)

# get all problem ids of platinum tasks
platinum_tasks = [problem_id for problem_id in benchmark if benchmark[problem_id]["problem_level"] == "platinum"]

# create a USACOTask for each platinum task
platinum_tasks_tasks = [USACOTask(problem_id) for problem_id in platinum_tasks]

# Example usage (add to the bottom of usaco_task.py or in a separate test script)
if __name__ == "__main__":
    # Assuming your solution file is named 'my_solution.py' in the same directory
    solution_file_path = "/home/azureuser/agent-zoo/my_solution.py"
    is_passing = platinum_tasks_tasks[0].evaluate(solution_file_path)
    if is_passing:
        print(f"Solution '{solution_file_path}' is PASSING!")
    else:
        print(f"Solution '{solution_file_path}' is FAILING.")
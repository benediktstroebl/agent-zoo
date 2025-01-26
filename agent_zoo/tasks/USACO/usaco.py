# usaco_task.py
import os
import zipfile
import urllib.request
import subprocess
import tempfile
from pathlib import Path
from ..task import Task # Import the base Task class

class USACOTask(Task):
    def __init__(self):
        self.test_cases_path = Path("agent_zoo/tasks/USACO/tests")
        
        # TODO this for now contains the one hard-coded usaco problem. We can generalize this
        problem_info = {
            "problem_id": "866_platinum_the_cow_gathering",
            "test_data_link": "http://www.usaco.org/current/data/gathering_platinum_dec18.zip",
            "num_tests": 17, # From problem description and by inspecting the zip file.
        }
        prompt_description = """Please generate Python 3 code to solve the below problem. Make sure
to wrap your code in '```python' and '```' Markdown delimiters, and
include exactly one block of code with the entire solution.
No outside libraries are allowed.

[BEGIN PROBLEM]
Cows have assembled from around the world for a massive gathering. There are $N$
cows, and $N-1$ pairs of cows who are friends with each other. Every cow knows
every other cow through some chain of friendships.

They had great fun, but the time has come for them to leave, one by one. They
want to leave in some order such that as long as there are still at least two
cows left, every remaining cow has a remaining friend. Furthermore, due to
issues with luggage storage, there are $M$ pairs of cows $(a_i, b_i)$ such that
cow $a_i$ must leave before cow $b_i$. Note that the cows $a_i$ and $b_i$ may or
may not be friends.

Help the cows figure out, for each cow, whether she could be the last cow to
leave. It may be that there is no way for the cows to leave satisfying the above
constraints.

INPUT FORMAT:
Line $1$ contains two space-separated integers $N$ and $M$.

Lines $2 \\leq i \\leq N$ each contain two integers $x_i$ and $y_i$ with
$1 \\leq x_i, y_i \\leq N$ and $x_i \\neq y_i$ indicating that cows $x_i$ and $y_i$
are friends.

Lines $N+1 \\leq i \\leq N+M$ each contain two integers $a_i$ and $b_i$ with
$1 \\leq a_i, b_i \\leq N$ and $a_i \\neq b_i$ indicating that cow $a_i$ must leave
the gathering before cow $b_i$.

It is guaranteed that $1 \\leq N, M \\leq 10^5$. In test cases worth $20\\%$
of the points, it is further guaranteed that $N, M \\leq 3000$.

OUTPUT FORMAT:
The output should consist of $N$ lines, with one integer $d_i$ on each line such
that $d_i = 1$ if cow $i$ could be the last to leave, and $d_i = 0$ otherwise.
[END PROBLEM]
"""

        super().__init__(
            name=problem_info["problem_id"],
            evaluation_function=self.evaluate,
            prompt=prompt_description,
            environment_vars=problem_info
        )
        self.problem_info = problem_info # Store problem info for evaluation

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
cow_gathering_task = USACOTask()


# Example usage (add to the bottom of usaco_task.py or in a separate test script)
if __name__ == "__main__":
    # Assuming your solution file is named 'my_solution.py' in the same directory
    solution_file_path = "/home/azureuser/agent-zoo/my_solution.py"
    is_passing = cow_gathering_task.evaluate(solution_file_path)
    if is_passing:
        print(f"Solution '{solution_file_path}' is PASSING!")
    else:
        print(f"Solution '{solution_file_path}' is FAILING.")
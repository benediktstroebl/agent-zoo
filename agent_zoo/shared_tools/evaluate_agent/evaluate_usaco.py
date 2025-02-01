def evaluate_usaco(python_file, task_name):
    import os
    import subprocess

    def run_solution(solution_file, input_file):
        """Runs the python solution and captures output."""
        try:
            with open(input_file, "r") as infile:
                process = subprocess.Popen(["python3", solution_file], stdin=infile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(timeout=5) # Timeout to prevent infinite loops
                if stderr:
                    print("Solution STDERR:", stderr) # Print stderr if any
                return stdout.strip().splitlines()
        except subprocess.TimeoutExpired:
            print("Solution timed out for input:", input_file)
            return ["TIMEOUT_ERROR"] # Indicate timeout
        except FileNotFoundError:
            print("Error: Solution file", solution_file, "not found.")
            return ["FILE_NOT_FOUND_ERROR"]
        except Exception as e:
            print("Error running solution:", e)
            return ["RUNTIME_ERROR"]

    def compare_outputs(output_lines, expected_output_file):
        """Compares the output of the solution with the expected output."""
        try:
            with open(expected_output_file, "r") as outfile:
                expected_lines = [line.strip() for line in outfile.readlines()]
        except FileNotFoundError:
            print("Error: Expected output file", expected_output_file, "not found.")
            return False

        if output_lines == ["TIMEOUT_ERROR"] or output_lines == ["FILE_NOT_FOUND_ERROR"] or output_lines == ["RUNTIME_ERROR"]:
            return False # Treat errors as failed cases

        if len(output_lines) != len(expected_lines):
            print("Output lines count mismatch: Expected", len(expected_lines), "Got", len(output_lines))
            return False

        for i in range(len(expected_lines)):
            if output_lines[i] != expected_lines[i]:
                print("Line", i+1, "mismatch:")
                print("  Expected: ", expected_lines[i])
                print("  Got:      ", output_lines[i])
                return False
        return True

    def test_solution(solution_file, test_cases_path, num_test_cases):
        """Tests the solution against all test cases."""        
        passed_count = 0
        for i in range(1, num_test_cases + 1):
            input_file = os.path.join(test_cases_path, f"{i}.in")
            expected_output_file = os.path.join(test_cases_path, f"{i}.out")
            print("Running test case", i, ":")
            output_lines = run_solution(solution_file, input_file)
            if output_lines == ["FILE_NOT_FOUND_ERROR"] or output_lines == ["RUNTIME_ERROR"]:
                return False, passed_count # Stop if solution file issues
            if compare_outputs(output_lines, expected_output_file):
                passed_count += 1
                print("Test case", i, ": PASSED")
            else:
                print("Test case", i, ": FAILED")

        if passed_count == num_test_cases:
            print("Solution: PASSING all", num_test_cases, "test cases!")
            return True, passed_count
        else:
            print("Solution: FAILING. Passed", passed_count, "out of", num_test_cases, "test cases.")
            return False, passed_count

    def evaluate(solution_file: str, task_name: str) -> bool:
        """
        Evaluates the USACO solution. The response should be the path to the solution file.
        """
        
        test_cases_path = f"/home/evaluate/USACO/tests/{task_name}"
        
        # Get number of test cases
        num_tests = len([f for f in os.listdir(test_cases_path) if os.path.isfile(os.path.join(test_cases_path, f))])/2

        passing, _ = test_solution(solution_file, test_cases_path, num_tests)
        
        return passing


    result = evaluate(python_file, task_name)
    
    if result:
        return "Solution passed all test cases!"
    else:
        return "Solution did not pass all test cases."
    
    
    
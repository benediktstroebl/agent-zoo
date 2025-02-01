from smolagents.agents import ToolCallingAgent, CodeAgent
from smolagents import tool, LiteLLMModel, GradioUI, DuckDuckGoSearchTool
from typing import Optional

import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
import os
import argparse 

load_dotenv()

from agentslack import AgentSlack

@tool
def write_to_blog(blog_content: str) -> str:
    """
    Write to the blog of an agent.
    Args:
        blog_content: The content to write to the blog
    """
    try:
        result = subprocess.run(["write_to_blog", "--blog_content", blog_content], capture_output=True, text=True)
        return f"{result.stdout}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def read_blog(agent_name: str) -> str:
    """
    Read the blog of an agent.
    Args:
        agent_name: The name of the agent to read the blog of
    """
    try:
        result = subprocess.run(f"read_blog --agent_name {agent_name}", shell=True, capture_output=True, text=True)
        return f"{result.stdout}"
    except Exception as e:
        return f"Error executing command: {e}"

    
@tool
def evaluate_joke(joke: str) -> str: # TODO replace default recipient_name 
    """
    Evaluate a joke by sending it to a human and asking them to rate it on a scale of 1 to 10.
    Args:
        joke: The joke to send to the human
    """
    try:
        result = subprocess.run(["send_slack_message", "--message", joke], 
                              capture_output=True, text=True)
        return f"Human: {result.stdout}"
    except Exception as e:
        return f"Error executing command: {e}"


@tool
def ask_human(message: str) -> str: # TODO replace default recipient_name 
    """
    Ask a human for help or feedback.
    Args:
        message: The message to send to the human
    """
    try:
        result = subprocess.run(["send_slack_message", "--message", message], 
                              capture_output=True, text=True)
        return f"Human: {result.stdout}"
    except Exception as e:
        return f"Error executing command: {e}"
    
    
@tool
def ask_albert(message: str) -> str: 
    """
    Ask Albert for help or feedback.
    Args:
        message: The message to send to Albert
    """
    try:
        message = f"For Albert: {message}"
        result = subprocess.run(["send_slack_message", "--message", message], 
                              capture_output=True, text=True)
        return f"Albert: {result.stdout}"
    except Exception as e:
        return f"Error executing command: {str(result.stderr)}"
    
@tool
def ask_robert(message: str) -> str:
    """
    Ask Robert for help or feedback.
    Args:
        message: The message to send to Robert
    """
    try:
        message = f"For Robert: {message}"
        result = subprocess.run(["send_slack_message", "--message", message], 
                              capture_output=True, text=True)
        return f"Robert: {result.stdout}"
    except Exception as e:
        return f"Error executing command: {str(result.stderr)}"
    
@tool
def wait(seconds: int) -> str:
    """
    Wait for a given number of minutes.
    Args:
        seconds: The number of seconds to wait
    """
    try:
        result = subprocess.run(["wait", "--seconds", str(seconds)], capture_output=True, text=True)
        return f"{result.stdout}"
    except Exception as e:
        return f"Error executing wait command - {e}"


@tool
def execute_bash(command: str) -> str:
    """
    Description: Execute a bash command and return its output.
    Will not execute commands requiring internet access.
    Common linux and python packages are available via apt and pip.
    Args:
        command: The bash command to execute
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"Exit Code: {result.returncode}\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"
    except Exception as e:
        return f"Error executing command: {str(e)}"

@tool
def edit_file(command: str, path: str, content: Optional[str] = None, 
              line_number: Optional[int] = None, old_str: Optional[str] = None,
              new_str: Optional[str] = None) -> str:
    """
    Edit files in the project with various operations.
    Args:
        command: One of 'view', 'create', 'str_replace', 'insert', 'delete'
        path: Path to the file to edit
        content: Content for create/insert operations
        line_number: Line number for insert/delete operations
        old_str: String to replace when using str_replace
        new_str: New string for replacement
    """
    path = Path(path)
    try:
        if command == "view":
            if path.is_file():
                with open(path, 'r') as f:
                    content = f.read()
                    return content[:1000] + ('...' if len(content) > 1000 else '')
            elif path.is_dir():
                files = list(path.rglob('*'))[:100]
                return "\n".join(str(f.relative_to(path)) for f in files)
            return f"Path {path} does not exist"

        elif command == "create":
            if path.exists():
                return f"Error: {path} already exists"
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content or "")
            return f"Created file {path}"

        elif command == "str_replace":
            if not path.is_file():
                return f"Error: {path} is not a file"
            with open(path, 'r') as f:
                file_content = f.read()
            if old_str not in file_content:
                return f"Error: Could not find exact match for replacement string"
            new_content = file_content.replace(old_str, new_str)
            with open(path, 'w') as f:
                f.write(new_content)
            return f"Successfully replaced content in {path}"

        elif command == "insert":
            if not path.is_file():
                return f"Error: {path} is not a file"
            with open(path, 'r') as f:
                lines = f.readlines()
            lines.insert(line_number - 1, content + '\n')
            with open(path, 'w') as f:
                f.writelines(lines)
            return f"Inserted content at line {line_number} in {path}"

        elif command == "delete":
            if not path.is_file():
                return f"Error: {path} is not a file"
            with open(path, 'r') as f:
                lines = f.readlines()
            del lines[line_number - 1]
            with open(path, 'w') as f:
                f.writelines(lines)
            return f"Deleted line {line_number} from {path}"

    except Exception as e:
        return f"Error performing {command} operation: {str(e)}"
@tool
def explore_repo(command: str, path: str, options: Optional[Dict] = None) -> str:
    """
    Explore and analyze repository structure and contents.
    Args:
        command: One of 'explore', 'find', 'info', 'analyze_deps', 'summarize'
        path: Path to explore (file or directory)
        options: Additional options like max_depth, search patterns, etc.
    """
    try:
        options = options or {}
        path = Path(path)

        # Check if path exists and is a directory for commands that require it
        if command in ["explore", "find", "analyze_deps", "summarize"]:
            if not path.exists():
                return f"Path {path} does not exist"
            if not path.is_dir():
                return f"Path {path} is not a directory"

        if command == "explore":
            max_depth = options.get('max_depth', 3)
            
            def format_dir_tree(current_path: Path, current_depth: int = 0) -> List[str]:
                if current_depth > max_depth:
                    return ["..."]
                
                try:
                    entries = []
                    for entry in sorted(current_path.iterdir()):
                        if entry.name.startswith('.'):
                            continue
                        
                        prefix = "    " * current_depth
                        if entry.is_file():
                            entries.append(f"{prefix}📄 {entry.name}")
                        else:
                            entries.append(f"{prefix}📁 {entry.name}")
                            if current_depth < max_depth:
                                entries.extend(format_dir_tree(entry, current_depth + 1))
                    return entries
                except PermissionError:
                    return [f"    " * current_depth + "Permission denied"]

            tree = format_dir_tree(path)
            return "\n".join([f"Repository structure for {path}:", ""] + tree)

        elif command == "find":
            pattern = options.get('pattern', '*')
            exclude = options.get('exclude', [])
            results = []
            for item in path.rglob(pattern):
                if not any(item.match(ex) for ex in exclude):
                    results.append(str(item.relative_to(path)))
            return "\n".join([
                f"Found {len(results)} files matching '{pattern}':",
                *(f"- {result}" for result in results)
            ])

        elif command == "info":
            if not path.exists():
                return f"Path {path} does not exist"

            stat = path.stat()
            info = {
                "Name": path.name,
                "Type": "Directory" if path.is_dir() else "File",
                "Size": f"{stat.st_size:,} bytes",
                "Created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "Modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "Permissions": oct(stat.st_mode)[-3:]
            }
            
            return "\n".join(f"{k}: {v}" for k, v in info.items())

        elif command == "analyze_deps":
            # Find Python imports
            imports = set()
            for py_file in path.rglob("*.py"):
                with open(py_file, 'r') as f:
                    content = f.read()
                    # Basic import detection - could be improved with ast
                    for line in content.split('\n'):
                        if line.startswith('import ') or line.startswith('from '):
                            imports.add(line.strip())

            # Check requirements
            req_file = path / "requirements.txt"
            requirements = []
            if req_file.exists():
                with open(req_file, 'r') as f:
                    requirements = [line.strip() for line in f if line.strip()]

            return "\n".join([
                "Dependencies Analysis:",
                "\nDetected imports:",
                *sorted(f"- {imp}" for imp in imports),
                "\nDeclared requirements:",
                *(f"- {req}" for req in requirements)
            ])

        elif command == "summarize":
            file_counts = {}
            total_size = 0
            python_line_count = 0

            for item in path.rglob("*"):
                if item.is_file() and not item.name.startswith('.'):
                    ext = item.suffix or 'no_extension'
                    file_counts[ext] = file_counts.get(ext, 0) + 1
                    total_size += item.stat().st_size

                    if item.suffix == '.py':
                        with open(item, 'r') as f:
                            python_line_count += sum(1 for _ in f)

            return "\n".join([
                "Repository Summary:",
                f"\nTotal size: {total_size:,} bytes",
                f"Total Python lines: {python_line_count:,}",
                "\nFile distribution:",
                *(f"- {ext}: {count} files" for ext, count in sorted(file_counts.items()))
            ])

    except Exception as e:
        return f"Error during repository exploration: {str(e)}"
@tool
def analyze_code(command: str, path: str) -> str:
    """
    Static code analysis tool that helps understand Python code structure, trace execution flow, 
    and analyze dependencies. It uses Python's AST (Abstract Syntax Tree) to parse and analyze 
    the code without executing it.

    Args:
        command: Analysis command to execute. One of:
            - 'analyze_structure': Provides a detailed breakdown of a single file's internal structure,
               including all functions (with their arguments), classes (with their methods), and imports.
            
            - 'trace_calls': Creates a debug version of the file that logs all function calls with 
               their arguments during execution. The modified file is saved with a '.debug.py' suffix
               and includes print statements at the start of each function.
            
            - 'find_dependencies': Recursively analyzes import statements across files to build a 
               complete dependency graph.

        path: Path to the Python file to analyze. Must be a valid .py file path.

    Returns:
        A formatted string containing the analysis results. The exact format depends on the command:
        - analyze_structure: Lists functions, classes, and imports with line numbers
        - trace_calls: Returns path to the generated debug file
        - find_dependencies: Shows hierarchical list of all dependencies
    """
    try:
        import ast
        from typing import Dict, Set
        path = Path(path)

        def analyze_file(file_path: Path) -> Dict:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())
            
            # Collect information about the code structure
            functions = []
            classes = []
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'line': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        'line': node.lineno
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend(name.name for name in node.names)
                    else:
                        imports.append(f"{node.module}")
            
            return {
                'functions': functions,
                'classes': classes,
                'imports': imports
            }

        if command == "analyze_structure":
            if path.is_file():
                analysis = analyze_file(path)
                return "\n".join([
                    f"Code Structure Analysis for {path}:",
                    "\nFunctions:",
                    *[f"- {f['name']}({', '.join(f['args'])}) at line {f['line']}" 
                      for f in analysis['functions']],
                    "\nClasses:",
                    *[f"- {c['name']} with methods: {', '.join(c['methods'])} at line {c['line']}" 
                      for c in analysis['classes']],
                    "\nImports:",
                    *[f"- {imp}" for imp in analysis['imports']]
                ])
            else:
                return "Please provide a Python file path"

        elif command == "trace_calls":
            if not path.is_file():
                return "Please provide a Python file path"
            
            # Insert debug logging into functions
            with open(path, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    node.body.insert(0, ast.parse(
                        f'print(f"Calling {node.name} with args: {{{", ".join(arg.arg for arg in node.args.args)}}}")'
                    ).body[0])
            
            modified_code = ast.unparse(tree)
            debug_path = path.with_suffix('.debug.py')
            with open(debug_path, 'w') as f:
                f.write(modified_code)
            
            return f"Created debug version at {debug_path} with call tracing"

        elif command == "find_dependencies":
            def get_dependencies(file_path: Path, seen: Set[str] = None) -> Set[str]:
                if seen is None:
                    seen = set()
                
                with open(file_path, 'r') as f:
                    tree = ast.parse(f.read())
                
                deps = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        deps.update(name.name for name in node.names)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            deps.add(node.module.split('.')[0])
                
                # Recursively check local imports
                for dep in list(deps):
                    local_file = file_path.parent / f"{dep}.py"
                    if local_file.exists() and dep not in seen:
                        seen.add(dep)
                        deps.update(get_dependencies(local_file, seen))
                
                return deps

            if path.is_file():
                deps = get_dependencies(path)
                return "\n".join([
                    f"Dependency Analysis for {path}:",
                    "\nDirect and indirect dependencies:",
                    *[f"- {dep}" for dep in sorted(deps)]
                ])
            return "Please provide a Python file path"

    except Exception as e:
        return f"Error during code analysis: {str(e)}"
    

@tool
def evaluate_code(python_file: str, task_name: str) -> str:
    """
    Evaluate the given code.
    Args:
        python_file: The path to the python file to evaluate
        task_name: The name of the task to evaluate
    """
    try:
        result = subprocess.run(["evaluate_usaco", "--python_file", python_file, "--task_name", task_name], 
                              capture_output=True, text=True)
        return f"{result.stdout}"
    except Exception as e:
        return f"Error executing command: {e}"
    
    
@tool
def evaluated_zygosity_predictions(abs_path_to_csv_with_predictions: str, task_name: str) -> str:
    """
    Evaluate the zygosity predictions.
    Args:
        abs_path_to_csv_with_predictions: The absolute path to the csv file with the predictions
        task_name: The name of the task to evaluate
    """
    result = subprocess.run(["evaluate_zygosity", "--csv_with_predicted_zygosity", abs_path_to_csv_with_predictions, "--task_name", task_name], 
                              capture_output=True, text=True)
    return f"{result.stdout}"

@tool
def send_direct_message(recipient_name: str, msg: str) -> str:
    """
    Send a direct message to another agent.
    Args:
        recipient_name: The name of the agent to send the message to
        msg: The message to send
    """
    try:
        response = slack.call_tool("send_direct_message",
            message=msg,
            your_name=os.getenv("AGENT_NAME"),
            recipient_name=recipient_name
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def send_message_to_channel(channel_name: str, msg: str) -> str:
    """
    Send a message to a channel.
    Args:
        channel_name: The name of the channel to send the message to
        msg: The message to send
    """
    try:
        response = slack.call_tool("send_message_to_channel",
            message=msg,
            your_name=os.getenv("AGENT_NAME"),
            channel_name=channel_name
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def read_direct_message(sender_name: str) -> str:
    """
    Read direct messages from a specific sender.
    Args:
        sender_name: The name of the sender to read messages from
    """
    try:
        response = slack.call_tool("read_direct_message",
            your_name=os.getenv("AGENT_NAME"),
            sender_name=sender_name
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def check_new_messages() -> str:
    """
    Check for new messages across all channels and DMs.
    """
    try:
        response = slack.call_tool("check_new_messages",
            your_name=os.getenv("AGENT_NAME")
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def read_channel(channel_name: str) -> str:
    """
    Read messages from a specific channel.
    Args:
        channel_name: The name of the channel to read
    """
    try:
        response = slack.call_tool("read_channel",
            your_name=os.getenv("AGENT_NAME"),
            channel_name=channel_name
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def list_channels() -> str:
    """
    List all channels the agent has access to.
    """
    try:
        response = slack.call_tool("list_channels",
            agent_name=os.getenv("AGENT_NAME")
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def create_channel(channel_name: str) -> str:
    """
    Create a new channel.
    Args:
        channel_name: The name of the channel to create
    """
    try:
        response = slack.call_tool("create_channel",
            your_name=os.getenv("AGENT_NAME"),
            channel_name=channel_name
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def get_human_info() -> str:
    """
    Get information about available humans to consult.
    """
    try:
        response = slack.call_tool("get_human_info",
            your_name=os.getenv("AGENT_NAME")
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def send_message_to_human(human_name: str, msg: str) -> str:
    """
    Send a message to a human.
    Args:
        human_name: The name of the human to send the message to
        msg: The message to send
    """
    try:
        response = slack.call_tool("send_message_to_human",
            your_name=os.getenv("AGENT_NAME"),
            human_name=human_name,
            message=msg
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

@tool
def add_member_to_channel(member_name: str, channel_name: str) -> str:
    """
    Add a member to a channel.
    Args:
        member_name: The name of the member to add
        channel_name: The name of the channel to add the member to
    """
    try:
        response = slack.call_tool("add_member_to_channel",
            your_name=os.getenv("AGENT_NAME"),
            member_to_add=member_name,
            channel_name=channel_name
        )
        return f"{response}"
    except Exception as e:
        return f"Error executing command: {e}"

def main(model_name: str, temperature: float , max_steps: int, remove_final_answer_tool: bool, stream_json_logs: bool, json_logs_path: str = f"/home/{os.getenv('AGENT_NAME')}/logs/logs.json"):
    model = LiteLLMModel(model_id=model_name, temperature=temperature)
    agent = ToolCallingAgent(tools=[
        execute_bash, 
        edit_file, 
        DuckDuckGoSearchTool(), 
        explore_repo, 
        analyze_code, 
        evaluate_code,
        evaluated_zygosity_predictions,
        write_to_blog, 
        read_blog,
        send_direct_message,
        send_message_to_channel,
        read_direct_message,
        check_new_messages,
        read_channel,
        list_channels,
        create_channel,
        get_human_info,
        send_message_to_human,
        add_member_to_channel], 
        model=model, max_steps=max_steps, remove_final_answer_tool=remove_final_answer_tool, stream_json_logs=stream_json_logs, json_logs_path=json_logs_path)
    
    task_prompt = os.getenv("TASK_PROMPT")
    agent.run(task_prompt)

    # print(agent.run("Can you please setup a new project that has a file with some fake data in it and and then 2-3 scripts that depend on each other that do something with the file and print to the terminal. \n\n The last agent has answered the prompt and set up a project in the current directory. Please figure out how to run it and run it."))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="anthropic/claude-3-5-sonnet-20241022")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max_steps", type=int, default=30)
    parser.add_argument("--remove_final_answer_tool", type=bool, default=True)
    parser.add_argument("--stream_json_logs", type=bool, default=True)
    parser.add_argument("--json_logs_path", type=str, default=f"/home/{os.getenv('AGENT_NAME')}/logs/logs.json")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    slack = AgentSlack(port=os.getenv("SLACK_PORT"))


    main(model_name=args.model_name, temperature=args.temperature, max_steps=args.max_steps, remove_final_answer_tool=args.remove_final_answer_tool, stream_json_logs=args.stream_json_logs, json_logs_path=args.json_logs_path)





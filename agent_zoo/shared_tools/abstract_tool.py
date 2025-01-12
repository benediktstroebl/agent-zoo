from typing import Dict, Union
import os
import inspect
import sys


class AbstractSharedTool:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.inputs = {}
        self.output_type = ""
        self.environment_vars = {}
        self.requirements_file = "requirements.txt"
        
    # take this from smolagents 
    name: str
    description: str
    inputs: Dict[str, Dict[str, Union[str, type, bool]]]
    output_type: str
    environment_vars: Dict[str, str]

    def _init_tool(self, workspace_dir, agent_dirs):
        """
        Initializes the tool in the docker environment. 
        Determines the folder structure of where the tool should be saved.
        """
        NotImplementedError('tool-specific')

    def __repr__(self):
        return f"{self.name}: {self.description}"
    
    def _get_tools(self):
        # a function to return all the tools we should register
        pass 

    def get_tool_scripts(self):
        # return a list of dicts
        # key is the tool name, value is the script
        tools = self._get_tools()
        tool_scripts = {}
        for tool in tools:
            tool_scripts[tool.__name__] = self._get_tool_script(tool)
        return tool_scripts

    
    def _get_tool_script(self, tool, command_name=None):
        """
        Register a Python function as a terminal command.

        Args:
            tool (callable): The Python function to register as a command.
            command_name (str, optional): The name of the terminal command. Defaults to the function name.
        """
        
        if not callable(tool):
            raise ValueError("The argument must be a callable function.")

        # Use the function name as the command name if not provided
        command_name = command_name or tool.__name__

        # Get the source code of the function
        func_source = inspect.getsource(tool)

        # Generate the CLI wrapper script
        script_content = f"""#!/usr/bin/env python3
import argparse

{func_source}

def main():
    parser = argparse.ArgumentParser(description="CLI wrapper for {tool.__name__}")
"""

        # Generate argument parsing based on the function signature
        signature = inspect.signature(tool)
        for param_name, param in signature.parameters.items():
            script_content += "    parser.add_argument(\"--{}\", type={}, required={})\n".format(
                param_name,
                "str" if param.annotation == inspect._empty else param.annotation.__name__,
                param.default == inspect._empty
            )

        script_content += f"""
    args = parser.parse_args()
    kwargs = vars(args)
    result = {tool.__name__}(**kwargs)
    print(result if result is not None else "")

if __name__ == "__main__":
    main()
    """

        return script_content
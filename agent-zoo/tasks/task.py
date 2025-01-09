from typing import Callable, Dict

class Task:
    def __init__(self, name: str, evaluation_function: Callable, prompt: str, environment_vars: Dict[str, str]):
        self.name = name
        self.evaluation_function = evaluation_function
        self.prompt = prompt
        self.environment_vars = environment_vars


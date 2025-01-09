from typing import Callable, Dict, List, Type
from abc import ABC, abstractmethod

class Task(ABC):
    _registry: Dict[str, Type['Task']] = {}

    def __init__(self, name: str, evaluation_function: Callable, prompt: str, environment_vars: Dict[str, str]):
        self.name = name
        self.evaluation_function = evaluation_function
        self.prompt = prompt
        self.environment_vars = environment_vars
    
    @classmethod
    def register(cls, task_class: Type['Task']):
        cls._registry[task_class.__name__] = task_class
        return task_class
    
    @classmethod
    def load_tasks(cls, task_names: List[str]) -> List['Task']:
        tasks = []
        for task_name in task_names:
            if task_name in cls._registry:
                task_class = cls._registry[task_name]
                task = task_class(task_name, cls.evaluation_function, cls.prompt, cls.environment_vars)
                tasks.append(task)
        return tasks


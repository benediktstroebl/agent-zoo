from typing import Callable, Dict, List, Type, Any
from abc import ABC, abstractmethod
import logging


class Task(ABC):
    _object_registry: Dict[str, 'Task'] = {}
    
    def __init__(self, name: str, evaluation_function: Callable, prompt: str, environment_vars: Dict[str, str]):
        self.name = name
        self.evaluation_function = evaluation_function
        self.prompt = prompt
        self.environment_vars = environment_vars
        self.logger = logging.getLogger('agent_zoo')
        self._register()
    
    def _register(self):
        Task._object_registry[self.name] = self
        self.logger.debug(f"Task {self.name} registered")
    
    @classmethod
    def get_tasks(cls, task_names: List[str]) -> Dict[str, 'Task']:
        return [cls._object_registry[name] for name in task_names]
    
    @abstractmethod
    def evaluate(self) -> Any:
        pass


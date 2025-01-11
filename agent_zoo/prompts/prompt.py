from typing import List
from abc import ABC, abstractmethod
from agent_zoo.agents.agent import Agent
from agent_zoo.tasks.task import Task
from agent_zoo.shared_tools.abstract_tool import AbstractSharedTool

class Prompt(ABC):    
    def __init__(self, tasks: List[Task], agents: List[Agent], shared_tools: List[AbstractSharedTool]):
        self.tasks = tasks
        self.agents = agents
        self.shared_tools = shared_tools
    
    @abstractmethod
    def get(self) -> str:
        pass

class PromptRegistry:
    _prompts = {}
    
    @classmethod
    def register(cls, name: str, prompt_class):
        cls._prompts[name] = prompt_class
        
    @classmethod
    def get(cls, name: str, tasks, agents, shared_tools) -> str:
        prompt_class = cls._prompts[name]
        prompt = prompt_class(tasks, agents, shared_tools)
        return prompt.get()
    
    
    
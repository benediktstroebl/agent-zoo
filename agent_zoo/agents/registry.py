import docker
from pathlib import Path
from ..tasks.task import Task
from typing import List
import os
from .agent import Agent

basic_agent = Agent(
    path=Path('agent_zoo/workspace/agents/basic_agent'),
    name='basic_agent',
    requirements_name='requirements.txt',
    entrypoint='agent.py'
)

basic_agent_2 = Agent(
    path=Path('agent_zoo/workspace/agents/basic_agent'),
    name='basic_agent_2',
    requirements_name='requirements.txt',
    entrypoint='agent.py'
)


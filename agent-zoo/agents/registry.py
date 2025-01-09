import docker
from pathlib import Path
from tasks.task import Task
from typing import List
import os
from agents.agent import Agent

basic_agent = Agent(
    path=Path('agent-zoo/workspace/agents/basic_agent'),
    name='basic_agent',
    requirements_name='requirements.txt',
    entrypoint='agent.py'
)


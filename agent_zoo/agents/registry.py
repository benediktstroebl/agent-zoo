import docker
from pathlib import Path
from ..tasks.task import Task
from typing import List
import os
from .agent import Agent


AGENT_NAMES = [ "MONKEY", "GORILLA", "GIRAFFE", "HAWK"]


basic_agent = Agent(
    path=Path('agent_zoo/workspace/agents/basic_agent'),
    name='monkey',
    requirements_name='requirements.txt',
    entrypoint='agent.py',
    environment_variables={
        "SLACK_BOT_TOKEN": os.getenv('MONKEY_SLACK_BOT_TOKEN')
    }
)

basic_agent_2 = Agent(
    path=Path('agent_zoo/workspace/agents/basic_agent'),
    name='zebra',
    requirements_name='requirements.txt',
    entrypoint='agent.py',
    environment_variables={
        "SLACK_BOT_TOKEN": os.getenv(f'ZEBRA_SLACK_BOT_TOKEN')
    }
)




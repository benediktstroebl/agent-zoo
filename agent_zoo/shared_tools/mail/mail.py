from attrs import define, field, asdict
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from abstract_tool import AbstractSharedTool


@define 
class Mail(AbstractSharedTool):
    tools = []
    def __sub_init__(self):
        pass

    def _init_tool(self, workspace_dir, agent_dirs):
        """
        create a folder /home/leaderboard/
        - initializes 
        """
        # make the directory
        for agent_dir in agent_dirs.values():
            mail_dir = agent_dir / "mail"
            mail_dir.mkdir(parents=True, exist_ok=True)
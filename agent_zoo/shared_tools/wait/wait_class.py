from attrs import define, field, asdict
import os
from pathlib import Path

from ..abstract_tool import AbstractSharedTool
from .wait import wait

@define 
class Wait(AbstractSharedTool):
    environment_vars = {}

    def __sub_init__(self):
        pass

    def _init_tool(self, workspace_dir, agent_dirs):
       pass

    def _get_tools(self):
        return [wait]

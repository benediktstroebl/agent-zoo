from attrs import define, field, asdict
import os
from pathlib import Path
import sys  
import shutil
from ..abstract_tool import AbstractSharedTool
from .evaluate_usaco import evaluate_usaco
from .evaluate_zygosity import evaluate_zygosity

@define 
class EvaluateUSACO(AbstractSharedTool):
    environment_vars: dict = field(default={})
    tools = []

    def __sub_init__(self):
        pass

    def _init_tool(self, workspace_dir, agent_dirs):
        # copy the USACO directory to a evaluate directory
        shutil.copytree(Path("agent_zoo/tasks/USACO"), os.path.join(workspace_dir, ".evaluate/USACO"))

    def _get_tools(self):
        return [evaluate_usaco]
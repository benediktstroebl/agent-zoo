import os
from dataclasses import dataclass

# TODO: change this later to automatically instantiate from a config file 
@dataclass
class EvalConfig:
    run_name: str
    workspace_dir: str
    agent_dirs: list[str]

    def get_full_path(self, agent_dir):
        return os.path.join(self.workspace_dir, self.run_name, agent_dir)
    
    def get_logs_path(self, agent_dir):
        return os.path.join(self.get_full_path(agent_dir), 'logs/logs.json')
    
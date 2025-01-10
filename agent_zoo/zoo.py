from typing import List, Union, Dict
from pathlib import Path 
from attrs import field, define 
import threading
from .tasks.task import Task
from .agents.agent import Agent
from .workspace import Workspace
from .configs.compute_config import DockerComputeConfig
from .configs.permissions_config import PermissionsConfig
from .configs.workspace_config import WorkspaceConfig
from .shared_tools.abstract_tool import AbstractSharedTool
from .logging_config import setup_logging
import logging

class AgentZoo:
    def __init__(self, agents: List[Path], shared_tools: List[AbstractSharedTool], tasks: List[Task], 
                 compute_config: Union[DockerComputeConfig,List[DockerComputeConfig]], 
                 permissions_config: PermissionsConfig,
                 workspace_config_path: Path = None):
        self.logger, self.get_container_handler = setup_logging()
        self.agents = agents
        self.shared_tools = shared_tools
        self.tasks = Task.get_tasks(tasks)
        self.compute_config = compute_config
        self.permissions_config = permissions_config
        self.workspace_config = WorkspaceConfig.from_yaml(workspace_config_path)
        self.agents = Agent.get_agents(self.agents)
        self.shared_tools = [AbstractSharedTool(tool) for tool in self.shared_tools]
        self.workspace = Workspace(self.agents, self.workspace_config, self.shared_tools)
        
        self.logger.info("AgentZoo initialized with %d agents, %d tools, and %d tasks", 
                        len(self.agents), len(self.shared_tools), len(self.tasks))

    def run(self):
        threads = []
        self.logger.info("Starting agent execution")
        
        # Setup workspace
        self.workspace.setup_workspace()
        
        # Setup agents and start threads
        for agent in self.agents:
            agent.workspace = self.workspace
            
            self.logger.debug(f"Creating thread for agent {agent.name}")
            thread = threading.Thread(
                target=agent.run,
                args=(self.tasks,)
            )
            threads.append(thread)
            thread.start()
        
        self.logger.info("All agent threads started, waiting for completion")
        for thread in threads:
            thread.join()

        
        self.logger.info("All agents completed execution")
from typing import List, Union, Dict, Optional
from pathlib import Path 
from attrs import field, define 
import threading
import time
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
                 workspace_config_path: Path = None,
                 max_runtime_minutes: Optional[int] = None):
        self.logger, self.get_container_handler = setup_logging()
        self.agents = agents
        self.shared_tools = shared_tools
        self.tasks = Task.get_tasks(tasks)
        self.compute_config = compute_config
        self.permissions_config = permissions_config
        self.workspace_config = WorkspaceConfig.from_yaml(workspace_config_path)
        self.agents = Agent.get_agents(self.agents)
        self.shared_tools = shared_tools
        self.workspace = Workspace(self.agents, self.workspace_config, self.shared_tools, self.tasks)
        self.max_runtime = max_runtime_minutes * 60 if max_runtime_minutes else None
        
        self.logger.info("AgentZoo initialized with %d agents, %d tools, and %d tasks", 
                        len(self.agents), len(self.shared_tools), len(self.tasks))

    def run(self):
        threads = []
        self.logger.info("Starting agent execution")
        
        # Setup workspace
        self.workspace.setup_workspace()
        
        start_time = time.time()
        stop_threads = threading.Event()
        
        # Setup agents and start threads
        for agent in self.agents:
            agent.workspace = self.workspace
            
            self.logger.debug(f"Creating thread for agent {agent.name}")
            thread = threading.Thread(
                target=self._run_agent_with_timeout,
                args=(agent, stop_threads)
            )
            threads.append(thread)
            thread.start()
        
        self.logger.info("All agent threads started, waiting for completion")
        
        # Wait for threads or timeout
        while any(t.is_alive() for t in threads):
            if self.max_runtime and (time.time() - start_time) > self.max_runtime:
                self.logger.warning(f"Maximum runtime of {self.max_runtime/60:.1f} minutes exceeded, stopping all agents")
                stop_threads.set()
                for agent in self.agents:
                    agent.stop()
                break
            
        for thread in threads:
            thread.join()

        self.logger.info("All agents completed execution")
            
    def _run_agent_with_timeout(self, agent: Agent, stop_event: threading.Event):
        try:
            while not stop_event.is_set():
                if not agent.run():
                    break
        except Exception as e:
            self.logger.error(f"Error in agent {agent.name}: {e}")
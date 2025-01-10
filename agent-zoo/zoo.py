from typing import List, Union, Dict
from pathlib import Path 
from attrs import field, define 
import threading
from tasks.task import Task
from agents.agent import Agent
from configs.compute_config import DockerComputeConfig
from configs.permission_config import PermissionsConfig
from shared_tools.abstract_tool import AbstractSharedTool


@define 
class AgentZoo:
    agents: List[Path] = field(default_factory=list)
    shared_tools: List[AbstractSharedTool] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    compute_config: Union[DockerComputeConfig,List[DockerComputeConfig]] = DockerComputeConfig()
    permissions_config: PermissionsConfig = PermissionsConfig()

    def __attrs_post_init__(self): 
        self.agents = Agent.get_agents(self.agents)
        self.shared_tools = [AbstractSharedTool(tool) for tool in self.shared_tools]
        self.tasks = Task.load_tasks(self.tasks)

    def run(self):
        """
        loop over agents, initialize them. 
        /home/agent_{i}
           /home/agent_{i}/agent_{i} # the agent repository 
           /home/agent_{i}/agent_copies/ # sandbox for evaluating the agents. 
           /home/agent_{i}/mail/ # mail directory for the agents.
           /home/agent_{i}/blog/ # this can lowkey serve as memory also
        /home/leaderboard/ 
        /home/tasks/task_{i}.py # shared tasks for the agents.
            input to task: eval task_name --agent_path=
        """
        NotImplementedError('todo')
        
        # loop over tasks
        for task in self.tasks:
            self.run_task(task.name, task.evaluation_function, task.prompt, task.environment_vars)

        # loop over agents initialize dockers
        threads = []
        for agent in self.agents:
            thread = threading.Thread(
                target=agent.run,
                args=(self.tasks,)
            )
            threads.append(thread)
            thread.start()

        # loop over shared tools and initialize them
        for tool in self.shared_tools:
            if tool.requires_server:
                server_thread = threading.Thread(target=tool._init_tool)
                server_thread.start()
            else:
                tool._init_tool()

        # Wait for both agents to complete
        for thread in threads:
            thread.join()
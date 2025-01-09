from typing import List, Union
from pathlib import Path 
from attrs import field, define 

@define 
class AgentZoo:
    agents: List[Path] = field(default_factory=list)
    shared_tools: List[SharedTool] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    compute_config: Union[DockerComputeConfig,List[DockerComputeConfig]] = DockerComputeConfig()
    permissions_config: PermissionsConfig = PermissionsConfig()

    def __attrs_post_init__(self): 
        self.agents = [Path(agent) for agent in self.agents]
        self.shared_tools = [SharedTool(tool) for tool in self.shared_tools]

    def initialize_zoo(self):
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

        # loop over agents initialize dockers 


        # loop over shared tools, initialize them.

        # loop over tasks
    
    def run_task(self, task_name: str, agent_path: Path):
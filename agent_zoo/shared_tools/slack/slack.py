from ..abstract_tool import AbstractSharedTool
import os
from typing import Dict, List
from utils.ports import find_free_port
from .send_slack_message import send_slack_message
from agentslack import AgentSlack
from attrs import define, field

@define
class Slack(AbstractSharedTool):
    world_agent_mapping: Dict[str, List[str]] = field(default=None)
    port: int = field(default=None)
    client: AgentSlack = field(default=None)
    environment_vars: dict = field(default=None)
    
    port = find_free_port()
    client = AgentSlack(port=port)
    client.start()
        
    environment_vars = {'SLACK_PORT': port}
    
    def __post_init__(self):
        for world in self.world_agent_mapping:
            self.client.register_world(world)
            for agent in self.world_agent_mapping[world]:
                self.client.register_agent(agent, world)


    def _init_tool(self, workspace_dir, agent_dirs):
        pass
        

    def _get_tools(self):
        return [send_slack_message]

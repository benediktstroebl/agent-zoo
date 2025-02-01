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
    
    def __init__(self, world_agent_mapping: Dict[str, List[str]], port=8080):
        self.world_agent_mapping = world_agent_mapping
        
        # select a free port for the slack client 
        self.port = find_free_port()
        self.client = AgentSlack(port=self.port)
        self.client.start()
        self.environment_vars = {'SLACK_PORT': self.port}
        
        if self.world_agent_mapping:
            for world in self.world_agent_mapping:
                print("WORLD_AGENT_MAPPING", self.world_agent_mapping)
                self.client.register_world(world)
                for agent in self.world_agent_mapping[world]:
                    self.client.register_agent(agent, world)

    def _init_tool(self, workspace_dir, agent_dirs):
        pass
        

    def _get_tools(self):
        return [send_slack_message]

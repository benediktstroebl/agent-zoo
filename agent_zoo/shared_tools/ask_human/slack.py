from ..abstract_tool import AbstractSharedTool
import os
from typing import Dict, List
from .send_slack_message import send_slack_message
from agentslack import AgentSlack

class Slack(AbstractSharedTool):
    
    def __init__(self, world_agent_mapping: Dict[str, List[str]], port=8080):
        self.world_agent_mapping = world_agent_mapping
        client = AgentSlack(port=port)
        client.start() 
        for world in self.world_agent_mapping:
            client.register_world(world)
            for agent in self.world_agent_mapping[world]:
                client.register_agent(agent, world)
        super().__init__()
    
    name: str = 'human_request'
    world_agent_mapping: Dict[str, List[str]]
    environment_vars = {
        'HUMAN_REQUEST_PATH': 'human_request',
        'SLACK_CLIENT_SECRET': 'slack_client_secret',
        'SLACK_CLIENT_ID': 'slack_client_id',
        'SLACK_BOT_TOKEN': 'slack_bot_token',
        'SLACK_CHANNEL_ID': 'slack_channel_id',
    }

    def _init_tool(self, workspace_dir, agent_dirs):
        pass
        

    def _get_tools(self):
        return [send_slack_message]

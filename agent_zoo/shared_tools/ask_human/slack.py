from ..abstract_tool import AbstractSharedTool
import os

from .send_slack_message import send_slack_message

class Slack(AbstractSharedTool):
    name: str = 'human_request'
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

from attrs import define, field, asdict
from pathlib import Path

from ..abstract_tool import AbstractSharedTool
from .check_mail import check_mail
from .send_message import send_message

@define 
class Mail(AbstractSharedTool):
    environment_vars = {'MAIL_DIRECTORY': 'mail'}

    def __sub_init__(self):
        pass

    def _init_tool(self, workspace_dir, agent_dirs):
        """
        create a folder /home/leaderboard/
        - initializes 
        """
        # make the directory
        for agent_dir in agent_dirs.values():
            mail_dir = agent_dir / self.environment_vars['MAIL_DIRECTORY']
            mail_dir.mkdir(parents=True, exist_ok=True)
            with open(mail_dir / 'mail.txt', 'w') as f:
                f.write('')

    def _get_tools(self):
        return [check_mail, send_message]
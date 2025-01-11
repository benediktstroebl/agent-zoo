from attrs import define, field, asdict
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from abstract_tool import AbstractSharedTool
from read_blog import read_blog
from write_to_blog import write_to_blog

@define 
class Blog(AbstractSharedTool):
    communal_blog: bool = field(default=False)
    tools = []

    environment_vars = {
        'BLOG_FORMAT': 'communal' if communal_blog else 'agent',
        'BLOG_FNAME': 'blog.csv'
    }

    def __sub_init__(self):
        pass

    def _init_tool(self, workspace_dir, agent_dirs):
        """
        create a folder /home/leaderboard/
        - initializes 
        """
        # make the directory
        if self.communal_blog:
            for agent_dir in agent_dirs.values():
                blog_dir = agent_dir / "blog"
                blog_dir.mkdir(parents=True, exist_ok=True)
        else:
            blog_dir = workspace_dir / "blog"
            blog_dir.mkdir(parents=True, exist_ok=True)

        self._initialize_tools()
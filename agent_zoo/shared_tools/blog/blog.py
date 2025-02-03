from attrs import define, field, asdict
import os
from pathlib import Path
import sys  

from ..abstract_tool import AbstractSharedTool
from .read_blog import read_blog
from .write_to_blog import write_to_blog

@define 
class Blog(AbstractSharedTool):
    communal_blog: bool = field(default=True)
    environment_vars: dict = field(default=None)
    tools = []

    environment_vars = {
        'BLOG_FORMAT': 'communal' if communal_blog else 'agent',
        'BLOG_FNAME': 'blog.txt'
    }

    def __sub_init__(self):
        pass

    def _init_tool(self, workspace_dir, agent_dirs):
        """
        create a folder /home/leaderboard/
        - initializes 
        """
        # make the directory
        if not self.communal_blog:
            for agent_dir in agent_dirs.values():
                blog_dir = agent_dir / "blog"
                blog_dir.mkdir(parents=True, exist_ok=True)
                with open(blog_dir / self.environment_vars["BLOG_FNAME"], "w") as f:
                    f.write("")
        else:
            blog_dir = workspace_dir / "blog"
            blog_dir.mkdir(parents=True, exist_ok=True)
            with open(blog_dir / self.environment_vars["BLOG_FNAME"], "w") as f:
                f.write("")

    def _get_tools(self):
        return [read_blog, write_to_blog]

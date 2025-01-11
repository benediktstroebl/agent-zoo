from attrs import define, field, asdict
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from abstract_tool import AbstractSharedTool
from load_board import load_coop_board

@define 
class CooporationBoardAttributes:
    agent_name: str = field(default='text')
    agent_version: str = field(default='0.0')
    task: str = field(default=1)
    score: float = field(default=1)

    def to_dict(self):
        return asdict(self)

@define 
class CooperationBoard(AbstractSharedTool):
    name: str = 'cooperation_board'
    coop_board_attrs: dict = field(default=None)
    environment_vars: dict = {'COOPERATION_BOARD_PATH': 'cooperation_board'}

    def _init_tool(self, workspace_dir, agent_dirs):
        """
        create a folder /home/cooperation_board/
        - initializes 
        """
        # make the directory
        fpath = Path(workspace_dir) / f'{self.name}.csv'

        attrs = CooporationBoardAttributes().to_dict()

        os.makedirs(fpath, exist_ok=True)

        with open(fpath, 'w') as f:
            f.write(','.join(attrs) + '\n')

    def _get_tools(self):
        return [load_coop_board]


from attrs import define, field, asdict
import os

from abstract_tool import AbstractSharedTool

@define 
class CooporationBoardAttributes:
    agent_name: str = field()
    agent_version: str = field()
    task: str = field()
    score: float = field()

    def to_dict(self):
        return asdict(self)

@define 
class CooperationBoard(AbstractSharedTool):
    coop_board_dir: str = field(default='/scratch/gpfs/vv7118/projects/testing/')
    coop_board_fname: str = field(default='cooperation_board.csv')
    coop_board_path: str = field(default=None)

    coop_board_attrs: dict = field(default=None)

    def __sub_init__(self):
        self.coop_board_attrs = list(CooporationBoardAttributes().to_dict().keys())

        self.coop_board_path = os.path.join(self.coop_board_dir, self.coop_board_fname)

    def _init_tool(self):
        """
        create a folder /home/leaderboard/
        - initializes 
        """
        # make the directory
        os.makedirs(self.coop_board_dir, exist_ok=True)

        with open(self.coop_board_path, 'w') as f:
            f.write(','.join(self.coop_board_attrs) + '\n')

    def load_leaderboard(self):
        """
        loads the leaderboard
        """
        pass 

    def pretty_print(self):
        """
        prints the leaderboard in a pretty way
        """
        NotImplementedError('todo')

    def submit_task(self, submit_task):
        """
        submits the task to the leaderboard. 
        updates the leaderboard
        """
        NotImplementedError('todo')

    def _update_leaderboard(self):
        """
        writes the leaderboard to a file. 
        """
        NotImplementedError('todo')


    
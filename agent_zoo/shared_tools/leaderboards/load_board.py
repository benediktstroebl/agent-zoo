import os 

def load_coop_board():
    """
    loads the leaderboard
    """
    cooperation_board_path = os.getenv('COOPERATION_BOARD_PATH')

    with open(cooperation_board_path, 'r') as f:
        lines = f.readlines()
        header = lines[0].strip().split(',')
        data = [line.strip().split(',') for line in lines[1:]]
    return data 
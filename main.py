from pathlib import Path
from dotenv import load_dotenv
import hydra
from omegaconf import DictConfig, OmegaConf
from hydra.utils import instantiate

load_dotenv()

from agent_zoo.zoo import AgentZoo
from agent_zoo.configs.compute_config import DockerComputeConfig
from agent_zoo.configs.permissions_config import PermissionsConfig
from agent_zoo.shared_tools import *

def print_ascii_art():
    try:
        with open('ascii_load_image.txt', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("ASCII art file not found")

@hydra.main(version_base=None, config_path="configs", config_name="config")
def main(config: DictConfig):
    experiment_config = config.experiments
    print_ascii_art()

    shared_tools = []
    print(experiment_config.shared_tools)
    for _, tool in experiment_config.shared_tools.items():
        shared_tools.append(instantiate(tool))


    print(experiment_config.agents)
    agents = []
    for _, agent in experiment_config.agents.items():
        agent = instantiate(agent)
        agent.environment_variables = {
            "SLACK_BOT_TOKEN": agent.environment_variables["SLACK_BOT_TOKEN"],
        }
        agents.append(agent)

    
    zoo = AgentZoo(
        name=experiment_config.world_name,
        agents=agents,
        tasks=experiment_config.tasks,
        compute_config=DockerComputeConfig(**experiment_config.compute_config),
        permissions_config=PermissionsConfig(**experiment_config.permissions_config),
        shared_tools=shared_tools, # load in from hydra 
        workspace_config_path=Path('agent_zoo/configs/default_workspace.yaml'),
        max_runtime_minutes=60    
        )
    zoo.run()
    
    zoo.clean_up()

if __name__ == "__main__":
    main()
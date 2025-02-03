from pathlib import Path
from dotenv import load_dotenv
import hydra
from omegaconf import DictConfig, OmegaConf
from hydra.utils import instantiate
import os 

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
    print_ascii_art()
    
    print(OmegaConf.to_yaml(config, resolve=True))

    experiment_config = config.experiments
    shared_tools = []
    
    for _, tool in experiment_config.shared_tools.items():
        shared_tools.append(instantiate(tool))

    agents = []
    for _, agent in experiment_config.agents.items():
        agent = instantiate(agent)
        agent.environment_variables = {
            "SLACK_BOT_TOKEN": os.getenv(agent.environment_variables["SLACK_BOT_TOKEN"]),
        }
        agents.append(agent)
    
    for i in range(config.repetitions):
        print(f"Running experiment {i+1} of {config.repetitions} for {experiment_config.world_name}")
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
        zoo.clean_up(config)
        
if __name__ == "__main__":
    main()
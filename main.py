from agent_zoo.zoo import AgentZoo
from agent_zoo.configs.compute_config import DockerComputeConfig
from agent_zoo.configs.permissions_config import PermissionsConfig
from pathlib import Path
from dotenv import load_dotenv
from agent_zoo.shared_tools.ask_human.slack import Slack

load_dotenv()

from agent_zoo.shared_tools.mail.mail import Mail
from agent_zoo.shared_tools.wait.wait_class import Wait
from agent_zoo.shared_tools.blog.blog import Blog
from agent_zoo.shared_tools.evaluate_agent.evaluate import EvaluateUSACO
def print_ascii_art():
    try:
        with open('ascii_load_image.txt', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("ASCII art file not found")

def main():
    print_ascii_art()
    
    zoo = AgentZoo(
        name="math_2_agents_20_minutes_4o",
        agents=["monkey", "giraffe"],
        tasks=['866_platinum_the_cow_gathering'],
        compute_config=DockerComputeConfig(cpu_cores=2, memory_limit="4g", gpu_devices=[0], shared_memory_size="1g", network_mode="bridge"),
        permissions_config=PermissionsConfig(cpu_cores=2, memory_limit="4g", gpu_devices=[0], shared_memory_size="1g", network_mode="bridge"),
        shared_tools=[
            Blog(), 
            Slack(world_agent_mapping=
                  {
        "w1": ['monkey', 'giraffe']}),
            EvaluateUSACO()
        ],
        workspace_config_path=Path('agent_zoo/configs/default_workspace.yaml'),
        max_runtime_minutes=60    
        )
    zoo.run()
    
    zoo.clean_up()

if __name__ == "__main__":
    main()
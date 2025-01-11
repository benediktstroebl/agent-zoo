from agent_zoo.zoo import AgentZoo
from agent_zoo.configs.compute_config import DockerComputeConfig
from agent_zoo.configs.permissions_config import PermissionsConfig
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from agent_zoo.shared_tools.mail.mail import Mail



def main():
    zoo = AgentZoo(
        agents=["basic_agent", "basic_agent_2"],
        tasks=['basic_task'],
        compute_config=DockerComputeConfig(cpu_cores=2, memory_limit="4g", gpu_devices=[0], shared_memory_size="1g", network_mode="bridge"),
        permissions_config=PermissionsConfig(cpu_cores=2, memory_limit="4g", gpu_devices=[0], shared_memory_size="1g", network_mode="bridge"),
        shared_tools=[Mail()],
        workspace_config_path=Path('agent_zoo/configs/default_workspace.yaml')
    )
    zoo.run()

if __name__ == "__main__":
    main()
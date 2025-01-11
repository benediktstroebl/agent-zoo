import docker
import uuid
from pathlib import Path
from ..tasks.task import Task
from typing import List, Dict
import os
import logging
from dotenv import load_dotenv
from ..logging_config import setup_logging

class Agent:
    _object_registry: Dict[str, 'Agent'] = {}
    logger = logging.getLogger('agent_zoo')
    
    def __init__(self, path: Path, name: str, requirements_name: str = 'requirements.txt', entrypoint: str = 'agent.py'):
        self.path = path
        self.name = name
        self.entrypoint = entrypoint
        self.requirements_name = requirements_name
        self.container: docker.models.containers.Container
        _, get_container_handler = setup_logging()
        self.container_logger = get_container_handler(self.name)
        self.workspace = None
        self._register()
        self.logger.info(f"Agent {self.name} initialized")
        
    def _register(self):
        Agent._object_registry[self.name] = self
        self.logger.debug(f"Agent {self.name} registered")
        
    @classmethod
    def get_agents(cls, agent_names: List[str]) -> Dict[str, 'Agent']:
        return [cls._object_registry[name] for name in agent_names]
                
    def _start_container(self):
        if not self.workspace:
            raise ValueError("Workspace must be set before starting container")

        docker_client = docker.from_env()
        
        # load local env vars from .env file and add them to the container environment
        load_dotenv()
        local_env_vars = {key: value for key, value in os.environ.items() if os.path.exists('.env') and key in open('.env').read()}
        
        # Get all env vars from the shared tools in the workspace
        shared_tools = self.workspace.get_shared_tools()
        shared_tool_env_vars = {key: value for tool in shared_tools for key, value in tool.environment_vars.items()}
        
        container_env = {
                **local_env_vars,
                **shared_tool_env_vars,
                "AGENT_NAME": self.name,
                "AGENT_HOME": f"/home/agent_{self.name}",
                "WORKSPACE_DIR": "/home",
                "PYTHONUNBUFFERED": "1",
            }
        
        self.logger.info(f"Building container image for agent {self.name}")
        docker_client.images.build(
            path="agent_zoo/agents",
            tag=f"agent_zoo_{self.name}:latest",
            dockerfile="Dockerfile"
        )
        
        self.logger.info(f"Starting container for agent {self.name}")
        
        # Get mount configurations from workspace
        volumes = {}
        for source, mount_opts in self.workspace.get_mount_options(self.name):
            volumes[source] = mount_opts
        
        container = docker_client.containers.run(
                f"agent_zoo_{self.name}:latest",
                command="tail -f /dev/null",
                volumes=volumes,
                environment=container_env,
                detach=True,
                name=f"agent_zoo_{self.name}_{uuid.uuid4()}"
            )
        
        # print env variables availabel in container 
        result = container.exec_run(
            cmd=["printenv"],
            environment=container_env,
            detach=False,
            stream=True
        )
        for output_chunk in result.output:
            line = output_chunk.decode()
            self.container_logger.info(line.strip(), extra={'container_name': self.name})

        
        self.logger.info(f"Container for agent {self.name} started successfully")
        return container
    
    def initialize(self):
        try:
            self.container = self._start_container()
        except Exception as e:
            self.logger.error(f"Failed to start container for agent {self.name}: {e}")
            raise Exception(f"Failed to start container: {e} for agent {self.name}")
        
    def run(self):
        try:
            self.logger.info(f"Initializing agent {self.name}")
            self.initialize()
            
            result = self.container.exec_run(
                cmd=["python", f"{self.workspace.get_agent_home(self.name)}/{self.entrypoint}"],
                environment={
                    "AGENT_NAME": self.name,
                    "TASK_PROMPT": self.workspace.prompt,
                    **{name: var for task in self.workspace.tasks for name, var in task.environment_vars.items()},
                },
                detach=False,
                stream=True
            )
            
            # Stream the command output in real-time
            output_lines = []
            for output_chunk in result.output:
                line = output_chunk.decode()
                output_lines.append(line)
                if line.strip():  # Only log non-empty lines
                    self.container_logger.info(line.strip(), extra={'container_name': self.name})
            
            output = ''.join(output_lines)
            exit_code = result.exit_code
                            
            if exit_code != 0:
                self.logger.error(f"Agent {self.name} failed with exit code {exit_code}")
                raise Exception(f"Agent {self.name} failed with exit code {exit_code}: {output}")
            else:
                self.logger.info(f"Agent {self.name} completed successfully")
                return output
                
        except Exception as e:
            self.logger.error(f"Agent {self.name} failed with error: {e}")
            if hasattr(self, 'container'):
                self.container.stop()
                self.container.remove()
            raise Exception(f"Agent {self.name} failed with error: {e}")
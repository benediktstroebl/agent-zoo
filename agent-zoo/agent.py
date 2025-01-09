import docker
from pathlib import Path
from tasks.task import Task
from typing import List
import os

class Agent:
    def __init__(self, path: Path, name: str, requirements_name: str = 'requirements.txt', tasks: List[Task] = []):
        self.path = path
        self.name = name
        self.entrypoint = 'agent.py'
        self.requirements_name = requirements_name
        self.container: docker.models.containers.Container
        self.tasks: List[Task] = tasks
        
    def _start_container(self):
        docker_client = docker.from_env()
        
        host_env = dict(os.environ)
        
        container_env = {
                **host_env,  # Include all host environment variables
                "AGENT_NAME": self.name,
                "WORKSPACE_DIR": "/workspace",
                "PYTHONUNBUFFERED": "1",  # Enable real-time Python logging
            }
        
        return docker_client.containers.run(
                "agent_zoo:latest",
                command="tail -f /dev/null",  # Keep container running
                volumes={
                    str(self.path.absolute()): {
                        'bind': '/workspace',
                        'mode': 'rw'
                    },
                },
                environment=container_env,  # Use the combined environment variables
                detach=True,
                name=f"agent_zoo_{self.name}"  # Use underscore in container name
            )
    
    
    def initialize(self, tasks: List[Task]):
        try:
            self.container = self._start_container()
        except Exception as e:
            raise Exception(f"Failed to start container: {e} for agent {self.name}")
        

    def run(self):
        """Run an agent with specific task information."""
        
        try:
            # Run the agent
            result = self.container.exec_run(
                cmd=["python", "/workspace/agent.py"],
                environment={name: var for task in self.tasks for name, var in task.environment_vars.items()},
                detach=False,  # Wait for completion
            )
            
            # Log the output
            output = result.output.decode()
                            
            # Check the exit code
            if result.exit_code != 0:
                raise Exception(f"Agent {self.name} failed with exit code {result.exit_code}")
            else:
                return output
                
        except Exception as e:
            raise Exception(f"Agent {self.name} failed with error: {e}")

    
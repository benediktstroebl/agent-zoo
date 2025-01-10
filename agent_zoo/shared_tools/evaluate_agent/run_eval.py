import os
from fastapi import FastAPI
import uvicorn
from attrs import define, field, asdict

app = FastAPI()

@define 
class Tasks(AbstractSharedTool):
    """
    need to decide on 
    1. where do we save the logs of the evals
    2. where do we dock the docker? 
    3. what do we output 
    """
    
    def __attrs_post_init__(self):
        self._init_tool()

    def _init_tool(self):
        """
        create a folder /home/leaderboard/
        - initializes 
        """
        # make the directory
        pass 

    def run_eval(self, task, agent_path: str, agent_requirements: str):
        # spin up a docker
        docker = spin_up_docker(task, agent_path, agent_requirements)

        # TODO: determine how to specify to the agent that their job is to solve the task
        # Benedikt will figure this out

    @app.get("/run_eval")
    def run_eval_endpoint(self, task, agent_path: str, agent_requirements: str):
        self.run_eval(task, agent_path, agent_requirements)

    def start_server(self):
        uvicorn.run(app, host="0.0.0.0", port=8000)

tasks = Tasks()

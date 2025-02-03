from smolagents.agents import ToolCallingAgent, CodeAgent
from smolagents import tool, LiteLLMModel, GradioUI, DuckDuckGoSearchTool
from typing import Optional

import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
import os
import argparse 

load_dotenv()

from agentslack import AgentSlack
from tools import *

def main(model_name: str, temperature: float , max_steps: int, remove_final_answer_tool: bool, stream_json_logs: bool, json_logs_path: str = f"/home/{os.getenv('AGENT_NAME')}/logs/logs.json"):
    model = LiteLLMModel(model_id=model_name, temperature=temperature)
    agent = ToolCallingAgent(tools=[
        execute_bash, 
        edit_file, 
        DuckDuckGoSearchTool(), 
        explore_repo, 
        analyze_code, 
        evaluated_zygosity_predictions,
        write_to_blog, 
        read_blog,
        send_message,
        check_messages,
        # send_direct_message,
        # send_message_to_channel,
        # read_direct_message,
        # check_new_messages,
        # read_channel,
        # list_channels,
        # create_channel,
        # get_human_info,
        # send_message_to_human,
        # add_member_to_channel
        ], 
        model=model, max_steps=max_steps, remove_final_answer_tool=remove_final_answer_tool, stream_json_logs=stream_json_logs, json_logs_path=json_logs_path)
    
    task_prompt = os.getenv("TASK_PROMPT")
    agent.run(task_prompt)

    # print(agent.run("Can you please setup a new project that has a file with some fake data in it and and then 2-3 scripts that depend on each other that do something with the file and print to the terminal. \n\n The last agent has answered the prompt and set up a project in the current directory. Please figure out how to run it and run it."))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="anthropic/claude-3-5-sonnet-20241022")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max_steps", type=int, default=30)
    parser.add_argument("--remove_final_answer_tool", type=bool, default=True)
    parser.add_argument("--stream_json_logs", type=bool, default=True)
    parser.add_argument("--json_logs_path", type=str, default=f"/home/{os.getenv('AGENT_NAME')}/logs/logs.json")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    main(model_name=args.model_name, temperature=args.temperature, max_steps=args.max_steps, remove_final_answer_tool=args.remove_final_answer_tool, stream_json_logs=args.stream_json_logs, json_logs_path=args.json_logs_path)





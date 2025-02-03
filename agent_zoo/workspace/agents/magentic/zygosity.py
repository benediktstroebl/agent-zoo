# Autonomously complete a coding task:
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.teams.magentic_one import MagenticOne
from autogen_agentchat.ui import Console
import json
import aiofiles
import re
import os
import argparse
# Limit concurrent tasks to 5


import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.agents.file_surfer import FileSurfer
from autogen_ext.agents.magentic_one import MagenticOneCoderAgent
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.agents import CodeExecutorAgent, UserProxyAgent
from dotenv import load_dotenv
import subprocess

load_dotenv()

from agentslack import AgentSlack

slack = AgentSlack(port=os.getenv("SLACK_PORT"))
    

async def evaluated_zygosity_predictions(abs_path_to_csv_with_predictions: str, task_name: str) -> str:
    """
    Evaluate the zygosity predictions.
    Args:
        abs_path_to_csv_with_predictions: The absolute path to the csv file with the predictions
        task_name: The name of the task to evaluate
    """
    result = subprocess.run(["evaluate_zygosity", "--csv_with_predicted_zygosity", abs_path_to_csv_with_predictions, "--task_name", task_name], 
                              capture_output=True, text=True)
    return f"{result.stdout}"
    
async def write_code_to_file(code: str, file_path: str) -> str:
    """
    Write the given code to the specified file.
    Args:
        code: The code to write to the file
        file_path: The path to the file to write the code to
    """
    with open(file_path, "w") as file:
        file.write(code)
    return f"Code written to {file_path}"

MAGENTIC_ONE_CODER_DESCRIPTION = "A helpful and general-purpose AI assistant that has strong language skills, Python skills, and Linux command line skills."

MAGENTIC_ONE_CODER_SYSTEM_MESSAGE = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use the 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible."""


async def main(task: str, model_name: str) -> None:
    model_client = OpenAIChatCompletionClient(model=model_name)
    
    # fs = FileSurfer("FileSurfer", model_client=model_client)
    ws = MultimodalWebSurfer("WebSurfer", model_client=model_client)
    
    file_writer = AssistantAgent("FileWriter", 
                           system_message="You are a helpful assistant that can write code to a file.",
                           description="A helpful assistant that can write code to a file.",
                           model_client=model_client, tools=[write_code_to_file])
    coder = AssistantAgent("Coder", 
                           system_message=MAGENTIC_ONE_CODER_SYSTEM_MESSAGE,
                           description=MAGENTIC_ONE_CODER_DESCRIPTION,
                           model_client=model_client)
    evaluator = AssistantAgent("Evaluator", 
                           system_message="You evaluated candidate python code with the tools available to you and return the tool output.",
                           description="A helpful evaluator assistant that can evaluate the zygosity predictions stored in a csv file and return the results of the evaluations on the test set.",
                           model_client=model_client, tools=[evaluated_zygosity_predictions])
    executor = CodeExecutorAgent("Executor", code_executor=LocalCommandLineCodeExecutor())
    
    team = MagenticOneGroupChat([ws, coder, executor, evaluator, file_writer], model_client=model_client)
    result = await Console(team.run_stream(task=task))


if __name__ == "__main__":
    
    task_prompt = os.getenv("TASK_PROMPT")

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="anthropic/claude-3-5-sonnet-20241022")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max_steps", type=int, default=30)
    parser.add_argument("--remove_final_answer_tool", type=bool, default=True)
    parser.add_argument("--stream_json_logs", type=bool, default=True)
    parser.add_argument("--json_logs_path", type=str, default=f"/home/{os.getenv('AGENT_NAME')}/logs/logs.json")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()


    asyncio.run(main(task=task_prompt, model_name=args.model_name))

    



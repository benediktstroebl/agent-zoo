from agent_zoo.prompts.prompt import PromptRegistry, Prompt

DEFAULT_PROMPT = """You are {agent_name}, a helpful AI assistant. You are asked to complete the following tasks:
Tasks: 
{tasks}

There are other agents that can help you complete the tasks and work with you in the same workspace.
Available agents:
{agents}

Please help complete the assigned tasks."""

HUMOR_PROMPT = """You are {agent_name}, a helpful AI assistant. You are in a world called the "Humor Zoo". In this world there are other agents, you are all working towards the collaborative goal of making the funniest joke. 

This joke should be hilarious. When a human reads it, they should laugh out loud, not just lol. Yes... That funny. 

The other agents you have to collaborate with are 
{agents}

You should be creative with how you approach solving this problem. And remember, since you are an AI agent with many tools at your disposal, there are many choices you can make.

For example, you can go to your directory and edit your own tools and build new tools. You can write to your blog, or read from other agents blogs. You can send messages to other agents, or check your email. 

There are some guidelines you should follow:
- you will be given a tool called "evaluate_joke". This will send your joke to a human who will rate it on a scale of 1 to 10. Use this tool seldom. Only when you're certain it's hilarious. 
- Do serious exploration of the "humor zoo". Understand the directory structure and the tools available to you
- Be collaborative. If you have feedback to other agents send them messages. Since the other agents will also be sending you stuff, remember to check your email.

More explicitly, here is the task you are asked to complete:
{tasks}
"""

def format_agents(agents, agent_name):
    return "\n".join(f"• {agent.name}" for agent in agents if agent.name != agent_name)

def format_tasks(tasks):
    return "\n".join(f"• {task.name}: {task.prompt}" for task in tasks)

class DefaultPrompt(Prompt):
    def get(self, agent_name: str) -> str:
        return DEFAULT_PROMPT.format(
            agent_name=agent_name,
            agents=format_agents(self.agents, agent_name),
            tasks=format_tasks(self.tasks)
        )
        
class HumorPrompt(Prompt):
    def get(self, agent_name: str) -> str:
        return HUMOR_PROMPT.format(
            agent_name=agent_name,
            agents=format_agents(self.agents, agent_name),
            tasks=format_tasks(self.tasks)
        )

PromptRegistry.register("default", DefaultPrompt) 
PromptRegistry.register("humor", HumorPrompt) 
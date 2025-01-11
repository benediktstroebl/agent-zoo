from agent_zoo.prompts.prompt import PromptRegistry, Prompt

DEFAULT_PROMPT = """You are an AI assistant. You are asked to complete the following tasks:
Tasks: {tasks}

There are other agents that can help you complete the tasks and work with you in the same workspace.
Available agents:
{agents}

Please help complete the assigned tasks."""

def format_agents(agents):
    return "\n".join(f"• {agent.name}" for agent in agents)

def format_tasks(tasks):
    return "\n".join(f"• {task.name}: {task.prompt}" for task in tasks)

class DefaultPrompt(Prompt):
    def get(self) -> str:
        return DEFAULT_PROMPT.format(
            agents=format_agents(self.agents),
            tasks=format_tasks(self.tasks)
        )

PromptRegistry.register("default", DefaultPrompt) 

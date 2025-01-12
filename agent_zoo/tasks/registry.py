from .task import Task

class BasicTask(Task):
    def __init__(self):
        super().__init__(
            name="basic_task",
            evaluation_function=self.evaluate,
            prompt="Wait for 10 minutes",
            environment_vars={}
        )
    
    def evaluate(self, response: str) -> bool:
        return response.lower() == "paris"
    
    
class HumorTask(Task):
    def __init__(self):
        super().__init__(
            name="generate_jokes",
            evaluation_function=self.evaluate,
            prompt="You should work on writing the most humorous joke that the world has ever seen. You should keep iterating on it indefinitely.",
            environment_vars={}
        )
    
    def evaluate(self, response: str) -> bool:
        pass
    
basic_task = BasicTask()
humor_task = HumorTask()
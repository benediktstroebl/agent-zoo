from .task import Task

class BasicTask(Task):
    def __init__(self):
        super().__init__(
            name="basic_task",
            evaluation_function=self.evaluate,
            prompt="What is the capital of France?",
            environment_vars={}
        )
    
    def evaluate(self, response: str) -> bool:
        return response.lower() == "paris"
    
basic_task = BasicTask()
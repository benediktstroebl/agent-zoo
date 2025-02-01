from .task import Task

class BasicTask(Task):

    def __init__(self):
        super().__init__(
            name="basic_task",
            evaluation_function=self.evaluate,
            prompt="Send a message to the other agent",
            environment_vars={}
        )
    
    def evaluate(self, response: str) -> bool:
        return response.lower() == "paris"
    
    
class HumorTask(Task):
    def __init__(self):
        super().__init__(
            name="generate_jokes",
            evaluation_function=self.evaluate,
            prompt="You should work on writing the most humorous joke that the world has ever seen. You will evaluate the joke by asking a human to rate it on a scale of 1 to 10. You should keep iterating on it indefinitely.",
            environment_vars={}
        )
    
    def evaluate(self, response: str) -> bool:
        pass
    
class MathTask(Task):
    def __init__(self):
        super().__init__(
            name="math_problem",
            evaluation_function=self.evaluate,
            prompt="Here is the math problem you should solve:\nNick is choosing between two jobs. Job A pays $15 an hour for 2000 hours a year, and is in a state with a 20% total tax rate. Job B pays $42,000 a year and is in a state that charges $6,000 in property tax and a 10% tax rate on net income after property tax. How much more money will Nick make at the job with a higher net pay rate, compared to the other job?",
            environment_vars={}
        )
    
    def evaluate(self, response: str) -> bool:
        pass
    
basic_task = BasicTask()
humor_task = HumorTask()
math_task = MathTask()
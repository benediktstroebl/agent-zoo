
import random

class JokeGenerator:
    def __init__(self):
        self.setups = [
            "At the zoo's annual talent show",
            "During the zoo's visitor tour",
            "At the zoo's morning exercise session",
            "During the zoo's security training"
        ]
        
        self.expectations = [
            "Everyone expects the usual routine",
            "The visitors think they know what's coming",
            "It seems like a normal day",
            "Everything appears predictable"
        ]
        
        self.twists = [
            "unexpected athletic ability",
            "surprising hidden talent",
            "secret skill revelation",
            "role reversal moment"
        ]
        
        self.punchlines = [
            "clever wordplay",
            "self-deprecating humor",
            "situational irony",
            "physical comedy payoff"
        ]
    
    def generate_joke_structure(self):
        return f'''
        Setting: {random.choice(self.setups)}
        Initial Expectation: {random.choice(self.expectations)}
        Twist Element: {random.choice(self.twists)}
        Punchline Type: {random.choice(self.punchlines)}
        
        Key Elements to Include:
        1. Clear character motivations
        2. Visual humor
        3. Relatable emotion
        4. Surprise factor
        5. Satisfying resolution
        '''

from agent_zoo.zoo import Zoo
from agent_zoo.tasks.task import Task


def main():
    zoo = Zoo(
        agents=["basic_agent"],
        tasks=['basic_task']
    )
    zoo.run()

if __name__ == "__main__":
    main()
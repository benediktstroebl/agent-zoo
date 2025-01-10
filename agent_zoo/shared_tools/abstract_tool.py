from typing import Dict, Union

class AbstractSharedTool:
    # take this from smolagents 
    name: str
    description: str
    inputs: Dict[str, Dict[str, Union[str, type, bool]]]
    output_type: str

    def _init_tool(self):
        """
        Initializes the tool in the docker environment. 
        Determines the folder structure of where the tool should be saved.
        """
        NotImplementedError('tool-specific')

    def __repr__(self):
        return f"{self.name}: {self.description}"
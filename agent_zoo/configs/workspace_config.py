from pathlib import Path
from typing import List, Dict, Optional
from attrs import define, field
import yaml

@define
class DirectoryConfig:
    name: str
    permissions: str
    other_agents: Optional[str] = None  # Permissions for other agents accessing this directory

@define
class WorkspaceConfig:
    base_dir: Path = field(default=Path("workspaces"))
    prompt: str = field(default="default")
    agent_directories: List[DirectoryConfig] = field(factory=list)
    shared_directories: List[DirectoryConfig] = field(factory=list)
    
    @classmethod
    def from_yaml(cls, yaml_path: Path = None) -> 'WorkspaceConfig':
        """Load workspace configuration from YAML file"""
        if yaml_path is None:
            yaml_path = Path(__file__).parent / "default_workspace.yaml"
            
        with open(yaml_path) as f:
            config = yaml.safe_load(f)
            
        return cls(
            base_dir=Path(config['base_dir']),
            agent_directories=[
                DirectoryConfig(**dir_config)
                for dir_config in config['agent_directories']
            ],
            shared_directories=[
                DirectoryConfig(**dir_config)
                for dir_config in config['shared_directories']
            ]
        ) 
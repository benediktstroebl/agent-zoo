from pathlib import Path
import shutil
import os
import uuid
from typing import List, Dict, Tuple
from .agents.agent import Agent
from .shared_tools.abstract_tool import AbstractSharedTool
from .configs.workspace_config import WorkspaceConfig

class Workspace:
    def __init__(self, agents: List[Agent], config: WorkspaceConfig, shared_tools: List[AbstractSharedTool] = None):
        self.agents = agents
        self.config = config
        self.shared_tools = shared_tools or []
        
        # Create unique workspace directory
        self.workspace_dir = config.base_dir / f"workspace_{uuid.uuid4().hex[:8]}"
        self.agent_dirs = {agent.name: self.workspace_dir / f"agent_{agent.name}" for agent in agents}

    def setup_workspace(self):
        """Setup the workspace directory structure for all agents"""
        # Create workspace root
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Create agent-specific directories for each agent
        for agent in self.agents:
            agent_dir = self.agent_dirs[agent.name]
            for dir_config in self.config.agent_directories:
                dir_path = agent_dir / dir_config.name
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # Copy agent files to workspace
            agent_workspace = agent_dir / "agent"
            if agent_workspace.exists():
                shutil.rmtree(agent_workspace)
            shutil.copytree(agent.path, agent_workspace)

        # Create shared directories if they don't exist
        for dir_config in self.config.shared_directories:
            dir_path = self.workspace_dir / dir_config.name
            dir_path.mkdir(parents=True, exist_ok=True)

        # Initialize tools in the shared tools directory
        # tools_dir = self.workspace_dir / "tools"  # nah we don't need this
        for tool in self.shared_tools:
            tool._init_tool(self.workspace_dir, agent_dirs=self.agent_dirs)

    def get_mount_options(self, agent_name: str) -> List[Tuple[str, Dict[str, str]]]:
        """Get the mount options for an agent's container
        Returns a list of (source_path, mount_options) tuples"""
        mounts = []
        
        # Mount own agent-specific directories with configured permissions
        agent_dir = self.agent_dirs[agent_name]
        for dir_config in self.config.agent_directories:
            dir_path = agent_dir / dir_config.name
            mount_opts = {'bind': f'/home/agent_{agent_name}/{dir_config.name}'}
            if dir_config.permissions != "rw":  # Only set mode if not full access
                mount_opts['mode'] = dir_config.permissions
            mounts.append((str(dir_path.absolute()), mount_opts))
        
        # Mount other agents' directories with other_agents permissions
        for other_agent in self.agents:
            if other_agent.name != agent_name:  # Skip own directories
                other_agent_dir = self.agent_dirs[other_agent.name]
                for dir_config in self.config.agent_directories:
                    if dir_config.other_agents:  # Only mount if other_agents permission is specified
                        dir_path = other_agent_dir / dir_config.name
                        mount_opts = {'bind': f'/home/agent_{other_agent.name}/{dir_config.name}'}
                        if dir_config.other_agents != "rw":  # Only set mode if not full access
                            mount_opts['mode'] = dir_config.other_agents
                        mounts.append((str(dir_path.absolute()), mount_opts))
        
        # Mount shared directories with configured permissions
        for dir_config in self.config.shared_directories:
            dir_path = self.workspace_dir / dir_config.name
            mount_opts = {'bind': f'/home/{dir_config.name}'}
            if dir_config.permissions != "rw":  # Only set mode if not full access
                mount_opts['mode'] = dir_config.permissions
            mounts.append((str(dir_path.absolute()), mount_opts))
        
        return mounts
    
    def get_shared_tools(self) -> List[AbstractSharedTool]:
        return self.shared_tools

    def get_agent_home(self, agent_name: str) -> Path:
        """Get the home directory for an agent inside the workspace and relative to the workspace root"""
        return Path(f"/home/agent_{agent_name}/agent")


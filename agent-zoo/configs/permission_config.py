import attrs
from typing import List, Optional

@attrs.define
class PermissionConfig:
    description: str = "Simple class to hold agent permissions for agents."

    cpu_cores: int = attrs.field(default=2, metadata={"description": "Number of CPU cores to allocate"})
    memory_limit: str = attrs.field(default="4g", metadata={"description": "Memory limit, e.g., '4g', '512m'"})
    gpu_devices: Optional[List[int]] = attrs.field(
        default=None,
        metadata={"description": "List of GPU device IDs to allocate, or None for no GPU"},
    )
    shared_memory_size: str = attrs.field(
        default="1g", metadata={"description": "Shared memory size for the container, e.g., '1g', '256m'"}
    )
    network_mode: str = attrs.field(
        default="bridge", metadata={"description": "Docker network mode, e.g., 'bridge', 'host', 'none'"}
    )

    def to_dict(self) -> dict:
        """Convert the configuration to a dictionary."""
        return attrs.asdict(self)

    @classmethod
    def from_dict(cls, config_dict: dict):
        """Create a configuration instance from a dictionary."""
        return cls(**config_dict)

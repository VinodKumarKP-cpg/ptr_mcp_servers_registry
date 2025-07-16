#!/usr/bin/env python3
import json
# Import the dynamic scripts function
import os
from pathlib import Path

from setuptools import setup


def discover_scripts():
    """Fallback script discovery during installation"""
    scripts = {}

    # Get the package directory
    package_dir = Path(__file__).parent
    servers_config = os.path.join(package_dir, "mcp_servers_registry", "servers", "server_config.json")

    config = {}
    with open(servers_config) as f:
        config = json.load(f)

    for server_name in config.keys():
        script_name = f"{server_name.replace('_server', '').replace('_', '-')}-mcp-server"
        entry_point = f"mcp_servers_registry.servers.{server_name}.server:main"
        scripts[script_name] = entry_point

    return scripts


dynamic_scripts = discover_scripts()

# Convert to console_scripts format
console_scripts = [
    f"{script_name} = {entry_point}"
    for script_name, entry_point in dynamic_scripts.items()
]

if __name__ == "__main__":
    setup(
        # Let pyproject.toml handle most configuration
        entry_points={
            'console_scripts': console_scripts
        }
    )

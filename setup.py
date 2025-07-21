#!/usr/bin/env python3
import glob
import json
# Import the dynamic scripts function
import os
import sys
from pathlib import Path
from typing import Dict, Any

from setuptools import setup

def load_server_config(config_directory) -> Dict[str, Any]:
    """Load server configuration from JSON file."""
    server_config = {}
    for config_file in glob.glob(os.path.join(config_directory, "*.json")):
        server_name = (os.path.basename(config_file).split('.'))[0]
        server_config[server_name] = load_individual_json_config(config_file=config_file)
    return server_config


def load_individual_json_config(config_file):
    """Load server configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{config_file}': {e}")
        sys.exit(1)


def discover_scripts():
    """Fallback script discovery during installation"""
    scripts = {}

    # Get the package directory
    package_dir = Path(__file__).parent
    servers_config_directory = os.path.join(package_dir, "mcp_servers_registry", "servers_config")

    config = load_server_config(config_directory=servers_config_directory)

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

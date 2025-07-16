import os
import sys

file_root = os.path.dirname(os.path.abspath(__file__))
path_list = [
    file_root,
    os.path.dirname(file_root),
    os.path.dirname(os.path.dirname(file_root))
]
for path in path_list:
    if path not in sys.path:
        sys.path.append(path)

import nest_asyncio  # Added import

nest_asyncio.apply()  # Added call

from mcp_servers_registry.utils.env_utils import EnvironmentUtils
from mcp_servers_registry.servers.base_mcp_server.server import BaseMCPServer


class EnvironmentToolsServer(BaseMCPServer):
    """Git tools MCP server implementation."""

    def __init__(self):
        """
        Initialize the Git tools server.
        """
        super().__init__(self.base_directory(__file__), object_list=[EnvironmentUtils()])


def main():
    """Main function to run the Environment Lookup tools server."""
    server = EnvironmentToolsServer()
    server.main()


if __name__ == "__main__":
    main()

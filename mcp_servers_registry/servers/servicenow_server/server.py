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

from mcp_servers_registry.utils.servicenow_utils import ServiceNowUtils
from mcp_servers_registry.servers.base_mcp_server.server import BaseMCPServer


class ServiceNowServer(BaseMCPServer):
    """ServiceNow MCP server implementation."""

    def __init__(self):
        """
        Initialize the ServiceNow server.
        """
        super().__init__(self.base_directory(__file__), object_list=[ServiceNowUtils()])

def main():
    """Main function to run the ServiceNow server."""
    server = ServiceNowServer()
    server.main()


if __name__ == "__main__":
    main()

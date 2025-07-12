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

from mcp_servers_registry.utils.code_remediation_utils import CodeRemediationUtils
from mcp_servers_registry.servers.base_mcp_server.server import BaseMCPServer


class CodeRemediationServer(BaseMCPServer):
    """Code remediation MCP server implementation."""

    def __init__(self):
        """
        Initialize the Code Remediation server.
        """
        super().__init__(self.base_directory(__file__), object_list=[CodeRemediationUtils()])


def main():
    """Main function to run the Code Remediation server."""
    server = CodeRemediationServer()
    server.main()


if __name__ == "__main__":
    main()

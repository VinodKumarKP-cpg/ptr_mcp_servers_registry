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

from mcp_servers_registry.utils.s3_utils import S3Utils
from mcp_servers_registry.utils.aws_utils import AWSUtils
from mcp_servers_registry.servers.base_mcp_server.server import BaseMCPServer
from mcp_servers_registry.utils.logger_utils import get_logger

logger = get_logger()

class AWSUtilsServer(BaseMCPServer):
    """Git tools MCP server implementation."""

    def __init__(self):
        """
        Initialize the Git tools server.
        """
        self.aws_utils = AWSUtils()
        super().__init__(self.base_directory(__file__), object_list=[S3Utils(self.aws_utils.get_s3_client(), logger)])

def main():
    """Main function to run the Git tools server."""
    server = AWSUtilsServer()
    server.main()


if __name__ == "__main__":
    main()

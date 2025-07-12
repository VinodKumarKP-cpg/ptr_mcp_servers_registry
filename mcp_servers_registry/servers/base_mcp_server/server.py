import argparse
import json
import os
import sys
from abc import ABC, abstractmethod
from inspect import ismethod, isfunction, getmembers
from typing import Literal, List
from starlette.requests import Request
from starlette.responses import PlainTextResponse

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

from fastmcp import FastMCP
from mcp_servers_registry.utils.logger_utils import get_logger
from pydantic import BaseModel

VALID_TRANSPORTS = {"stdio", "streamable-http", "sse"}


class MCPServerConfig(BaseModel):
    port: int


class BaseMCPServer(ABC):
    """Base class for MCP servers that accepts server name as input parameter."""

    def __init__(self, server_name: str, object_list: List[object]):
        """
        Initialize the base MCP server.

        Args:
            server_name: Name of the MCP server
        """
        self.server_name = server_name
        self.logger = get_logger()
        self.server_config: MCPServerConfig = self.get_server_config()
        self.mcp = FastMCP(server_name,
                           host="0.0.0.0",
                           port=self.server_config.port)

        # Register tools after initialization
        self.object_list = object_list
        self._register_tools()


    def get_server_config(self):
        """
        Get the server configuration from server_config.json using the server name
        :return:
        """
        file_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        server_config_file = os.path.join(file_root, "server_config.json")
        with open(server_config_file, "r") as f:
            server_config = json.load(f)

        if self.server_name not in server_config:
            raise ValueError(f"Server name {self.server_name} not found in server_config.json")
        return MCPServerConfig.model_validate(server_config[self.server_name])

    def base_directory(self, file_name):
        """Get the base directory of the MCP server."""
        return (os.path.dirname(os.path.abspath(file_name)).split("/"))[-1]

    def _register_methods(self, object):
        for method_name, method in getmembers(object):

            if not ismethod(method) and isfunction(method):
                continue

            # Skip private methods
            if method_name.startswith('_'):
                continue
            self.mcp.tool()(method)


    def _register_tools(self):
        """Abstract method to register tools. Must be implemented by subclasses."""

        for obj in self.object_list:
            self._register_methods(obj)

        @self.mcp.custom_route("/health", methods=["GET"])
        async def health_check(request: Request) -> PlainTextResponse:
            """
            Health check endpoint that returns "OK" when the server is healthy.
            You can also include more advanced checks here, like database connectivity.
            """
            # You might want to add more comprehensive health checks here,
            # such as checking database connections or other dependencies.
            # For a basic health check, simply returning "OK" is sufficient.
            return PlainTextResponse("OK")

    def run(self, transport: Literal["stdio", "streamable-http", "sse"] = "stdio"):
        """Run the MCP server."""
        if transport not in VALID_TRANSPORTS:
            raise ValueError(f"Invalid transport: {transport}. Must be one of {VALID_TRANSPORTS}")
        self.mcp.port = self.server_config.port
        self.mcp.run(transport=transport)

    def main(self):
        parser = argparse.ArgumentParser(description=f"Run MCP server - {self.server_name}")
        parser.add_argument("--transport", default="stdio", help="Transport method (default: stdio)")
        args = parser.parse_args()
        self.run(transport=args.transport)

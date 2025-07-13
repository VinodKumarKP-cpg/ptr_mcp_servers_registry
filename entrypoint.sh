#!/bin/bash
if [ -z "$MCP_SERVER_NAME" ]; then
    echo "Error: MCP_SERVER_NAME environment variable is required"
    exit 1
fi
exec python -m mcp_servers_registry.servers.${MCP_SERVER_NAME}.server "$@"
import logging
import os
import sys
from typing import List, Dict, Any, Optional, Coroutine

file_root = os.path.dirname(os.path.abspath(__file__))
path_list = [
    file_root,
    os.path.dirname(file_root)
]
for path in path_list:
    if path not in sys.path:
        sys.path.append(path)

import nest_asyncio  # Added import

nest_asyncio.apply()  # Added call

from fastmcp import FastMCP
from mcp_servers_registry.utils.code_remediation_utils import CodeRemediationUtils
from mcp_servers_registry.utils.logger_utils import get_logger

# Configure logging
logger = get_logger()


# Initialize MCP server
mcp = FastMCP("code_remediation_server")


@mcp.tool()
async def analyze_repository(git_url: str, branch: str = "main", issue_flag=True, remediated_code=False) -> dict:
    """
    Analyze the specified git repository.

    Args:
        git_url: Git repository URL
        branch: Branch to analyze (default: main)
        issue_flag: Flag to indicate if issues should be found
        remediated_code: Flag to indicate if remediated code should be returned

    Returns:
        dict: Analysis results
    """
    code_remediation_utils = CodeRemediationUtils()
    return code_remediation_utils.analyze_repository(git_url=git_url,
                                                     branch=branch,
                                                     remediated_code=remediated_code,
                                                     issue_flag=issue_flag)

def main():
    mcp.run()


if __name__ == "__main__":
    main()

import os
import sys
from typing import List, Dict, Any, Optional

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

from mcp_servers_registry.utils.git_utils import GitUtils
from mcp_servers_registry.servers.base_mcp_server.server import BaseMCPServer


class GitToolsServer(BaseMCPServer):
    """Git tools MCP server implementation."""

    def __init__(self):
        """
        Initialize the Git tools server.

        Args:
            server_name: Name of the MCP server (default: "git-tools")
        """
        self.git_utils = GitUtils()
        super().__init__(self.base_directory(__file__))

    def _register_tools(self):
        """Register all Git-related tools."""

        super()._register_tools()

        @self.mcp.tool()
        async def clone_repository(git_url: str, branch: str = "main") -> str:
            """
            Clone the specified git repository.

            Args:
                git_url: Git repository URL
                branch: Branch to checkout (default: main)

            Returns:
                str: Path to the cloned repository

            Raises:
                GitHubError: If cloning fails
            """
            self.logger.info(f"Cloning repository: {git_url}, branch: {branch}")
            return self.git_utils.clone_repository(git_url=git_url, branch=branch)

        @self.mcp.tool()
        async def get_file_list(repo_path: str) -> List[str]:
            """
            Get list of files in the repository, excluding binary and hidden files.

            Args:
                repo_path: Path to repository

            Returns:
                list: List of file paths relative to repository root
            """
            return self.git_utils.get_file_list_helper(repo_path)

        @self.mcp.tool()
        async def get_git_stats(repo_path: str) -> Dict[str, Any]:
            """
            Get comprehensive statistics about the Git repository.

            Args:
                repo_path: Path to the Git repository

            Returns:
                dict: Repository statistics including commits, contributors, branches, etc.
            """
            return self.git_utils.get_git_stats(repo_path=repo_path)

        @self.mcp.tool()
        async def get_commit_history(repo_path: str, limit: int = 20, since_days: Optional[int] = None) -> List[
            Dict[str, Any]]:
            """
            Get commit history with detailed information.

            Args:
                repo_path: Path to the Git repository
                limit: Maximum number of commits to return
                since_days: Only return commits from the last N days

            Returns:
                list: List of commit information dictionaries
            """
            return self.git_utils.get_commit_history(repo_path=repo_path, limit=limit, since_days=since_days)

        @self.mcp.tool()
        async def identify_programming_languages(repo_path: str) -> Dict[str, Any]:
            """
            Identify programming languages used in the repository.

            Args:
                repo_path: Path to the Git repository

            Returns:
                dict: Language statistics and breakdown
            """
            return self.git_utils.identify_programming_languages(repo_path=repo_path)

        @self.mcp.tool()
        async def get_repository_structure(repo_path: str, max_depth: int = 3) -> Dict[str, Any]:
            """
            Get the directory structure of the repository.

            Args:
                repo_path: Path to the Git repository
                max_depth: Maximum depth to traverse

            Returns:
                dict: Repository structure information
            """
            return self.git_utils.get_repository_structure(repo_path=repo_path, max_depth=max_depth)

        @self.mcp.tool()
        async def get_contributor_stats(repo_path: str) -> Dict[str, Any]:
            """
            Get detailed contributor statistics.

            Args:
                repo_path: Path to the Git repository

            Returns:
                dict: Contributor statistics
            """
            return self.git_utils.get_contributor_stats(repo_path=repo_path)

        @self.mcp.tool()
        async def search_commits(repo_path: str, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
            """
            Search commits by message content.

            Args:
                repo_path: Path to the Git repository
                search_term: Term to search for in commit messages
                limit: Maximum number of results to return

            Returns:
                list: List of matching commits
            """
            return self.git_utils.search_commits(repo_path=repo_path, search_term=search_term, limit=limit)

        @self.mcp.tool()
        async def cleanup_repository(repo_path: str) -> bool:
            """
            Clean up the cloned repository by removing the temporary directory.

            Args:
                repo_path: Path to the repository to clean up

            Returns:
                bool: True if successful, False otherwise
            """
            return self.git_utils.cleanup_repository(repo_path=repo_path)


def main():
    """Main function to run the Git tools server."""
    server = GitToolsServer()
    server.main()


if __name__ == "__main__":
    main()

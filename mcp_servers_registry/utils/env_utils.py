#!/usr/bin/env python3
"""
MCP Server for Environment Variables
A FastMCP server that provides access to environment variables.
"""

import os
from typing import Dict, Any, Optional


class EnvironmentUtils:
    def get_environment_variables(
            self,
            pattern: Optional[str] = None,
            include_sensitive: bool = False
    ) -> Dict[str, Any]:
        """
        Get environment variables accessible to the MCP server.

        Args:
            pattern: Optional string pattern to filter environment variable names (case-insensitive)
            include_sensitive: Whether to include potentially sensitive variables (default: False)

        Returns:
            Dictionary containing environment variables and metadata
        """

        # Common sensitive environment variable prefixes/names
        sensitive_patterns = [
            'password', 'secret', 'key', 'token', 'auth', 'credential',
            'api_key', 'private', 'cert', 'ssl', 'tls', 'oauth'
        ]

        def is_sensitive(var_name: str) -> bool:
            """Check if an environment variable name suggests sensitive content."""
            var_lower = var_name.lower()
            return any(pattern in var_lower for pattern in sensitive_patterns)

        # Get all environment variables
        all_env_vars = dict(os.environ)

        # Filter by pattern if provided
        if pattern:
            filtered_vars = {
                k: v for k, v in all_env_vars.items()
                if pattern.lower() in k.lower()
            }
        else:
            filtered_vars = all_env_vars

        # Handle sensitive variables
        if not include_sensitive:
            safe_vars = {}
            sensitive_vars = []

            for k, v in filtered_vars.items():
                if is_sensitive(k):
                    sensitive_vars.append(k)
                else:
                    safe_vars[k] = v

            result = {
                "environment_variables": safe_vars,
                "total_count": len(safe_vars),
                "sensitive_variables_hidden": len(sensitive_vars),
                "sensitive_variable_names": sensitive_vars,
                "note": "Sensitive variables are hidden by default. Use include_sensitive=true to show all."
            }
        else:
            result = {
                "environment_variables": filtered_vars,
                "total_count": len(filtered_vars),
                "note": "All environment variables are shown (including potentially sensitive ones)."
            }

        # Add system information
        result["system_info"] = {
            "platform": os.name,
            "path_separator": os.pathsep,
            "current_working_directory": os.getcwd()
        }

        return result

    def get_specific_env_var(self, variable_name: str) -> Dict[str, Any]:
        """
        Get a specific environment variable by name.

        Args:
            variable_name: Name of the environment variable to retrieve

        Returns:
            Dictionary containing the variable value and metadata
        """

        value = os.environ.get(variable_name)

        result = {
            "variable_name": variable_name,
            "exists": value is not None,
            "value": value if value is not None else None
        }

        if value is None:
            result["message"] = f"Environment variable '{variable_name}' not found"

        return result

    def get_path_variables(self) -> Dict[str, Any]:
        """
        Get PATH-related environment variables parsed into lists.

        Returns:
            Dictionary containing PATH variables broken down into individual paths
        """

        path_vars = ['PATH', 'PYTHONPATH', 'LD_LIBRARY_PATH', 'CLASSPATH']
        result = {}

        for var_name in path_vars:
            value = os.environ.get(var_name)
            if value:
                # Split by path separator and filter out empty strings
                paths = [p.strip() for p in value.split(os.pathsep) if p.strip()]
                result[var_name] = {
                    "raw_value": value,
                    "paths": paths,
                    "path_count": len(paths)
                }

        return {
            "path_variables": result,
            "path_separator": os.pathsep,
            "note": "Common PATH-like environment variables parsed into individual paths"
        }

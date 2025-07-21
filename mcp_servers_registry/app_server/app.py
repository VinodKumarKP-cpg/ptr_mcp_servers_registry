"""
MCP Server Dashboard

A professional Streamlit application for monitoring and managing MCP servers.
Provides real-time status monitoring, health checks, and configuration management.
"""

import asyncio
import glob
import json
import os
import socket
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List

import requests
import streamlit as st
from langchain_mcp_adapters.client import MultiServerMCPClient

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NetworkUtils:
    """Utility class for network-related operations."""

    @staticmethod
    def get_local_ip() -> str:
        """Get the local IP address of the machine."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0)
        try:
            # Connect to a dummy address to get local IP
            sock.connect(('10.254.254.254', 1))
            ip_address = sock.getsockname()[0]
        except Exception:
            ip_address = '127.0.0.1'
        finally:
            sock.close()
        return ip_address

    @staticmethod
    def get_public_ip() -> Optional[str]:
        """Get the public IP address using an external service."""
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error getting public IP: {e}")
            return None

    @staticmethod
    def check_port_status(port: int, host: str = 'localhost') -> bool:
        """Check if a port is open/accessible."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            return False


class ServerHealthChecker:
    """Handles server health monitoring and status checks."""

    @staticmethod
    def get_server_health(port: int, host: str = 'localhost') -> Dict[str, Any]:
        """Get comprehensive server health information."""
        try:
            response = requests.get(f"http://{host}:{port}/health", timeout=2)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds(),
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException:
            return {
                "status": "unreachable",
                "response_time": None,
                "status_code": None,
                "timestamp": datetime.now().isoformat()
            }


class MCPToolsManager:
    """Handles MCP tools retrieval and management."""

    @staticmethod
    async def get_mcp_tools_list(server_name,
                                 server_port,
                                 environment=None) -> List[Dict[str, str]]:
        """Get the list of available MCP tools for a server."""
        tools = []
        try:
            client = MultiServerMCPClient({
                server_name: {
                    "url": f"http://localhost:{server_port}/mcp",
                    "transport": "streamable_http",
                    "timeout": timedelta(seconds=2),
                    "sse_read_timeout": timedelta(seconds=2)
                }
            })
            tools = await client.get_tools()
        except:
            try:
                client = MultiServerMCPClient({
                    "server_name": {
                        "command": "uv",
                        "args": [
                            "run", os.path.join(root, "servers", server_name, "server.py")
                        ],
                        "transport": "stdio",
                        "env": environment if environment else {}
                    }
                })
                tools = await client.get_tools()
            except:
                pass

        return tools


class ConfigurationManager:
    """Manages server configuration loading and validation."""

    def __init__(self):
        self.file_root = os.path.dirname(os.path.abspath(__file__))
        self.config_directory = os.path.join(
            os.path.dirname(self.file_root),
            "servers_config")

    def load_server_config(self) -> Dict[str, Any]:
        """Load server configuration from JSON file."""
        server_config = {}
        for config_file in glob.glob(os.path.join(self.config_directory, "*.json")):
            server_name = (os.path.basename(config_file).split('.'))[0]
            server_config[server_name] = self.load_individual_json_config(config_file=config_file)
        return server_config

    def load_individual_json_config(self, config_file):
        """Load server configuration from JSON file."""
        try:
            with open(config_file, "r", encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            st.error(f"Configuration file not found: {config_file}")
            return {}
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON in configuration file: {str(e)}")
            return {}
        except Exception as e:
            st.error(f"Error loading server configuration: {str(e)}")
            return {}

    def load_readme(self, server_name: str) -> Optional[str]:
        """Load README content for a specific server."""
        try:
            readme_path = os.path.join(
                os.path.dirname(self.file_root),
                "servers",
                server_name,
                "README.md"
            )

            if os.path.exists(readme_path):
                with open(readme_path, "r", encoding='utf-8') as file:
                    return file.read()
            return None
        except Exception as e:
            st.error(f"Error loading README for {server_name}: {str(e)}")
            return None

    def validate_configuration(self, server_config: Dict[str, Any]) -> list:
        """Validate server configuration and return results."""
        validation_results = []

        for server_name, server_info in server_config.items():
            port = server_info.get('port')

            if not port:
                validation_results.append({
                    'server': server_name,
                    'status': 'error',
                    'message': 'Missing port configuration'
                })
            elif not isinstance(port, int) or port < 1 or port > 65535:
                validation_results.append({
                    'server': server_name,
                    'status': 'error',
                    'message': f'Invalid port number ({port})'
                })
            else:
                validation_results.append({
                    'server': server_name,
                    'status': 'success',
                    'message': 'Valid configuration'
                })

        return validation_results


class DashboardUI:
    """Handles the Streamlit UI components and layout."""

    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.health_checker = ServerHealthChecker()
        self.network_utils = NetworkUtils()
        self.tools_manager = MCPToolsManager()
        self._setup_page_config()
        self._load_custom_css()

    def _setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="MCP Server Dashboard",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def _load_custom_css(self):
        """Load custom CSS styles from external file."""
        css_path = os.path.join(os.path.dirname(__file__), "style.css")

        try:
            with open(css_path, "r", encoding='utf-8') as file:
                st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("style.css not found. Using default styling.")

    def render_header(self):
        """Render the main header section."""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 MCP Server Dashboard</h1>
        </div>
        """, unsafe_allow_html=True)

    def render_sidebar(self, server_config: Dict[str, Any]):
        """Render the sidebar with controls and statistics."""
        with st.sidebar:
            auto_refresh = self._render_dashboard_controls()
            self._render_server_statistics(server_config)
            return auto_refresh

    def _render_dashboard_controls(self):
        """Render dashboard control section."""
        st.header("📊 Dashboard Controls")

        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
        if auto_refresh:
            st.rerun()

        if st.button("🔄 Refresh Now", use_container_width=True):
            st.rerun()

        return auto_refresh

    def _render_server_statistics(self, server_config: Dict[str, Any]):
        """Render server statistics section."""
        st.header("📈 Server Statistics")

        stats = self._get_server_stats(server_config)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", stats["total"])
        with col2:
            st.metric("Online", stats["online"])
        with col3:
            st.metric("Offline", stats["offline"])

        # Network information
        public_ip = self.network_utils.get_public_ip()
        local_ip = self.network_utils.get_local_ip()

        st.markdown(f"<div>Public IP: {public_ip or 'Unknown'}</div>", unsafe_allow_html=True)
        st.markdown(f"<div>Local IP: {local_ip}</div>", unsafe_allow_html=True)

    def _get_server_stats(self, server_config: Dict[str, Any]) -> Dict[str, int]:
        """Calculate server statistics."""
        total_servers = len(server_config)
        online_servers = sum(
            1 for server in server_config.values()
            if self.network_utils.check_port_status(server.get('port', 0))
        )
        offline_servers = total_servers - online_servers

        return {
            "total": total_servers,
            "online": online_servers,
            "offline": offline_servers
        }

    def render_main_content(self, server_config: Dict[str, Any]):
        """Render the main content area."""
        st.header("🌐 Available MCP Servers")

        tab1, tab2 = st.tabs(["📋 Server List", "🔧 Configuration"])

        with tab1:
            self._render_server_list(server_config)

        with tab2:
            self._render_configuration_tab(server_config)

    def _render_server_list(self, server_config: Dict[str, Any]):
        """Render the server list tab."""
        for server_name, server_info in server_config.items():
            port = server_info.get('port', 0)
            is_online = self.network_utils.check_port_status(port)

            display_name = server_name.replace('_', ' ').title()

            with st.expander(f"🖥️ {display_name}", expanded=False):
                # Use asyncio to run the async method
                asyncio.run(self._render_server_card(server_name, server_info, is_online))

    def _render_tools_popover(self, tools: List[Dict[str, str]]):
        """Render the tools popover content."""
        if not tools:
            st.info("No tools available or unable to fetch tools.")
            return

        for tool in tools:
            tool_description = tool.description.replace("\n", "<br/>")
            st.markdown(f"**Tool:** {tool.name}", unsafe_allow_html=True)
            st.markdown(f"**Description:** {tool_description}", unsafe_allow_html=True)
            st.divider()

    async def _render_server_card(self, server_name: str, server_info: Dict[str, Any], is_online: bool):
        """Render an individual server card."""
        port = server_info.get('port', 0)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Server Information")
            st.write(f"**Port:** {port}")

            # Environment variables
            env_vars = server_info.get('environment', {})
            if env_vars:
                st.write("**Environment Variables:**")
                for key, value in env_vars.items():
                    st.write(f"  - `{key}`: {value}")

            # Server health
            health = self.health_checker.get_server_health(port)
            st.write(f"**Health Status:** {health['status']}")
            if health['response_time']:
                st.write(f"**Response Time:** {health['response_time']:.3f}s")

            await self._render_documentation_section(server_name, port, env_vars)

        with col2:
            # Status badge
            status_class = "status-online" if is_online else "status-offline"
            status_text = "🟢 Online" if is_online else "🔴 Offline"
            st.markdown(f"""
            <div class="status-badge {status_class}">
                {status_text}
            </div>
            """, unsafe_allow_html=True)

            # Quick actions
            st.write("**Quick Actions:**")

            if st.button(f"📊 Test Connection", key=f"test_{server_name}"):
                if is_online:
                    st.success("✅ Connection successful!")
                else:
                    st.error("❌ Connection failed!")

            # Tools popover

    async def _render_documentation_section(self,
                                            server_name: str,
                                            port,
                                            env_vars):
        """Render the README section for a server."""
        readme_content = self.config_manager.load_readme(server_name)
        if readme_content:
            st.subheader("📖 Documentation")
            # README content
            col3, col4 = st.columns([1, 1])
            with col3:
                with st.popover("View Documentation"):
                    st.markdown(readme_content)
            with col4:
                with st.popover("🛠️ View Available Tools", use_container_width=False):
                    with st.spinner("Loading tools..."):
                        tools = await self.tools_manager.get_mcp_tools_list(server_name, port, env_vars)
                        self._render_tools_popover(tools)
        else:
            st.info("No README.md found for this server.")

    def _render_configuration_tab(self, server_config: Dict[str, Any]):
        """Render the configuration tab."""
        st.subheader("⚙️ Server Configuration")

        # Display configuration
        st.json(server_config)

        # Configuration validation
        st.subheader("🔍 Configuration Validation")

        validation_results = self.config_manager.validate_configuration(server_config)

        for result in validation_results:
            if result['status'] == 'error':
                st.error(f"❌ {result['server']}: {result['message']}")
            else:
                st.success(f"✅ {result['server']}: {result['message']}")

    def render_footer(self):
        """Render the footer section."""
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: #666; padding: 1rem;">
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
            MCP Server Dashboard v1.0
        </div>
        """, unsafe_allow_html=True)

    def run(self):
        """Main application entry point."""
        self.render_header()

        # Load configuration
        server_config = self.config_manager.load_server_config()

        if not server_config:
            st.error("No server configuration found. Please check the directory servers_config for corresponding config file.")
            return

        # Render UI components
        auto_refresh = self.render_sidebar(server_config)
        self.render_main_content(server_config)
        self.render_footer()

        # Auto-refresh mechanism
        if auto_refresh:
            import time
            time.sleep(30)
            st.rerun()


def main():
    """Application entry point."""
    dashboard = DashboardUI()
    dashboard.run()


if __name__ == "__main__":
    main()

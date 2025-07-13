import json
import os
import streamlit as st
from datetime import datetime
import subprocess
import socket
import requests
from typing import Dict, Any, Optional

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error getting public IP: {e}")
        return None


# Configure page
st.set_page_config(
    page_title="MCP Server Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5rem;
    }

    .server-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }

    .server-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }

    .status-online {
        background-color: #d4edda;
        color: #155724;
    }

    .status-offline {
        background-color: #f8d7da;
        color: #721c24;
    }

    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }

    .sidebar-section {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def check_port_status(port: int) -> bool:
    """Check if a port is open/accessible"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            return result == 0
    except:
        return False


def get_server_health(port: int) -> Dict[str, Any]:
    """Get server health information"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=2)
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time": response.elapsed.total_seconds(),
            "status_code": response.status_code
        }
    except:
        return {
            "status": "unreachable",
            "response_time": None,
            "status_code": None
        }


def load_server_config() -> Dict[str, Any]:
    """Load server configuration from JSON file"""
    try:
        file_root = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(file_root), "servers/server_config.json")

        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading server configuration: {str(e)}")
        return {}


def load_readme(server_name: str) -> Optional[str]:
    """Load README content for a server"""
    try:
        file_root = os.path.dirname(os.path.abspath(__file__))
        readme_path = os.path.join(os.path.dirname(file_root), "servers", server_name, "README.md")

        if os.path.exists(readme_path):
            with open(readme_path, "r") as f:
                return f.read()
        return None
    except Exception as e:
        st.error(f"Error loading README for {server_name}: {str(e)}")
        return None


def get_server_stats(server_config: Dict[str, Any]) -> Dict[str, int]:
    """Get server statistics"""
    total_servers = len(server_config)
    online_servers = sum(1 for server in server_config.values()
                         if check_port_status(server.get('port', 0)))
    offline_servers = total_servers - online_servers

    return {
        "total": total_servers,
        "online": online_servers,
        "offline": offline_servers
    }


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 MCP Server Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)

    # Load configuration
    server_config = load_server_config()

    if not server_config:
        st.error("No server configuration found. Please check your server_config.json file.")
        return

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📊 Dashboard Controls")

        # Auto-refresh option
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
        if auto_refresh:
            st.rerun()

        # Manual refresh button
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Server Statistics
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📈 Server Statistics")
        stats = get_server_stats(server_config)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", stats["total"])
        with col2:
            st.metric("Online", stats["online"])
        with col3:
            st.metric("Offline", stats["offline"])
        st.markdown("<div>Host IP: {}</div>".format(get_public_ip()), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Quick Actions
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("⚡ Quick Actions")

        if st.button("📋 Export Config", use_container_width=True):
            st.download_button(
                label="Download server_config.json",
                data=json.dumps(server_config, indent=2),
                file_name="server_config.json",
                mime="application/json"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Main content area
    st.header("🌐 Available MCP Servers")

    # Create tabs for different views
    tab1, tab2 = st.tabs(["📋 Server List", "🔧 Configuration"])

    with tab1:
        # Server cards
        for server_name, server_info in server_config.items():
            port = server_info.get('port', 0)
            is_online = check_port_status(port)

            # Create expandable server card
            with st.expander(f"🖥️ {server_name.replace('_', ' ').title()}", expanded=False):
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Server details
                    st.subheader("Server Information")
                    st.write(f"**Port:** {port}")

                    # Environment variables
                    env_vars = server_info.get('environment', {})
                    if env_vars:
                        st.write("**Environment Variables:**")
                        for key, value in env_vars.items():
                            st.write(f"  - `{key}`: {value}")

                    # Server health
                    health = get_server_health(port)
                    st.write(f"**Health Status:** {health['status']}")
                    if health['response_time']:
                        st.write(f"**Response Time:** {health['response_time']:.3f}s")

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

                # README content
                readme_content = load_readme(server_name)
                if readme_content:
                    st.subheader("📖 Documentation")
                    with st.popover("Documentation"):
                        st.markdown(readme_content)
                else:
                    st.info("No README.md found for this server.")

    with tab2:
        st.subheader("⚙️ Server Configuration")

        # Display configuration in a formatted way
        st.json(server_config)

        # Configuration validation
        st.subheader("🔍 Configuration Validation")

        validation_results = []
        for server_name, server_info in server_config.items():
            port = server_info.get('port')
            if not port:
                validation_results.append(f"❌ {server_name}: Missing port configuration")
            elif not isinstance(port, int) or port < 1 or port > 65535:
                validation_results.append(f"❌ {server_name}: Invalid port number ({port})")
            else:
                validation_results.append(f"✅ {server_name}: Valid configuration")

        for result in validation_results:
            if "❌" in result:
                st.error(result)
            else:
                st.success(result)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 1rem;">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
        MCP Server Dashboard v1.0
    </div>
    """, unsafe_allow_html=True)

    # Auto-refresh mechanism
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()


if __name__ == "__main__":
    main()
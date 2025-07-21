# Environment Variables MCP Server

A comprehensive Model Context Protocol (MCP) server that provides secure access to environment variables and system information. This server enables AI assistants to safely retrieve and analyze environment variables with built-in security features to protect sensitive information.

## Features

### Environment Variable Access
- **Secure variable retrieval** with automatic sensitive data filtering
- **Pattern-based filtering** for targeted variable searches
- **Configurable sensitivity controls** to show or hide potentially sensitive variables
- **Comprehensive metadata** including counts and system information

### System Information
- **Platform detection** and system details
- **Path separator identification** for cross-platform compatibility
- **Current working directory** information
- **PATH variable parsing** with detailed breakdown

### Security Features
- **Automatic sensitive variable detection** using common patterns
- **Safe-by-default approach** hiding sensitive variables unless explicitly requested
- **Detailed logging** of hidden variables for transparency
- **Pattern-based filtering** to avoid accidental exposure

## Installation

### Option 1: Direct UV Run (Recommended)
Use uv to run the server directly without local installation:

```json
{
  "env-server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
      "env-lookup-mcp-server"
    ]
  }
}
```

### Option 2: Pip Install + Run
Install the package first, then run the server:

```bash
pip install git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git
```

Then configure your MCP client:
```json
{
  "env-server": {
    "command": "env-lookup-mcp-server",
    "args": []
  }
}
```

### Option 3: Local Clone + UV Run
Clone the repository locally and run with uv:

```bash
git clone https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git
```

Then configure your MCP client:
```json
{
  "env-server": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "/path/to/ptr_mcp_servers_registry",
      "env-lookup-mcp-server"
    ]
  }
}
```

### Option 4: Local Docker Compose Setup

You can run the MCP server registry locally using Docker Compose. This is ideal for development and testing purposes.

#### Prerequisites
- Docker and Docker Compose installed
- Make utility installed
- `jq` command-line JSON processor

#### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git
   cd ptr_mcp_servers_registry
   ```

2. **Build and start all services:**
   ```bash
   make start-all
   ```

3. **Or start a specific service:**
   ```bash
   make start-env_server
   ```

4. **List available services:**
   ```bash
   make list-services
   ```

5. **Configure your client to use the local server:**
   In your client configuration (e.g., Claude Desktop), add the server with the local URL:
   ```json
   {
     "env-server": {
       "command":"npx",
    	"args":["mcp-remote@latest","http://localhost:8005/mcp", "--allow-http"]
     }
   }
   ```

#### Available Make Commands

- `make start-all` - Start all services using Docker Compose
- `make stop-all` - Stop all services
- `make start-<service>` - Start a specific service
- `make stop-<service>` - Stop a specific service
- `make restart-<service>` - Restart a specific service
- `make list-services` - List all available services
- `make docker-build` - Build the Docker image
- `make generate-compose` - Generate Docker Compose file

### Option 5: Remote Server Deployment

For production use or when you want to share the MCP server with multiple users, you can deploy it to a remote server.

#### Prerequisites
- Remote server with Docker and Docker Compose installed
- SSH access to the remote server
- Domain name or public IP address

#### Deployment Steps

1. **Deploy to your remote server:**
   ```bash
   # SSH into your remote server
   ssh user@your-remote-server.com
   
   # Clone the repository
   git clone https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git
   cd ptr_mcp_servers_registry
   
   # Build and start services
   make start-all
   ```

2. **Configure firewall (if needed):**
   ```bash
   # Allow traffic on port 8005
   # Check the servers_config/env_lookup_server.json for the list of ports to be opened
   sudo ufw allow 8005
   ```

3. **Configure your client to use the remote server:**
   In your client configuration, use the remote server URL:
   ```json
   {
     "env-server": {
       "command":"npx",
    	"args":["mcp-remote@latest","http://remote-ip:8005/mcp", "--allow-http"]
     }
   }
   ```

## Configuration

### Claude Desktop
Add to your `claude_desktop_config.json`:

Using uv command

```json
{
  "mcpServers": {
    "env-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
        "env-lookup-mcp-server"
      ]
    }
  }
}
```

Using npx command and remote server

```json
{
  "mcpServers": {
    "env-server": {
      "command":"npx",
    	"args":["mcp-remote@latest","http://<<remote-ip>>:8005/mcp", "--allow-http"]
    }
  }
}
```

### Other MCP Clients
The server follows the standard MCP protocol and can be integrated with any MCP-compatible client using the installation methods above.

## Available Tools

### Environment Variable Management

#### `get_environment_variables`
Retrieve environment variables with security filtering and pattern matching.
- **Parameters:**
  - `pattern` (string, optional): Filter environment variable names by pattern (case-insensitive)
  - `include_sensitive` (boolean, optional): Whether to include potentially sensitive variables (default: False)
- **Returns:** Dictionary containing:
  - `environment_variables`: Dictionary of environment variables
  - `total_count`: Number of variables returned
  - `sensitive_variables_hidden`: Count of hidden sensitive variables (if `include_sensitive=False`)
  - `sensitive_variable_names`: List of hidden sensitive variable names
  - `system_info`: Platform and system information
  - `note`: Information about filtering behavior

#### `get_specific_env_var`
Retrieve a specific environment variable by name.
- **Parameters:**
  - `variable_name` (string): Name of the environment variable to retrieve
- **Returns:** Dictionary containing:
  - `variable_name`: The requested variable name
  - `exists`: Boolean indicating if the variable exists
  - `value`: The variable value (or null if not found)
  - `message`: Error message if variable not found

#### `get_path_variables`
Get PATH-related environment variables parsed into individual components.
- **Parameters:** None
- **Returns:** Dictionary containing:
  - `path_variables`: Dictionary of PATH-like variables with:
    - `raw_value`: Original environment variable value
    - `paths`: List of individual paths
    - `path_count`: Number of paths found
  - `path_separator`: System path separator character
  - `note`: Description of the parsing behavior

## Security Features

### Sensitive Variable Detection
The server automatically detects potentially sensitive environment variables using common patterns:
- `password`, `secret`, `key`, `token`
- `auth`, `credential`, `api_key`
- `private`, `cert`, `ssl`, `tls`
- `oauth`

### Safe-by-Default Behavior
- Sensitive variables are hidden by default
- Only safe variables are returned unless explicitly requested
- Detailed information about hidden variables is provided
- Pattern matching works on both safe and sensitive variables

### Transparency
- Count of hidden sensitive variables is always provided
- Names of hidden variables are listed (but not their values)
- Clear notifications when sensitive variables are included or excluded

## Usage Examples

### Basic Environment Variable Access
```python
# Get all safe environment variables
env_vars = await get_environment_variables()

# Get variables matching a pattern
python_vars = await get_environment_variables(pattern="python")

# Get all variables including sensitive ones (use with caution)
all_vars = await get_environment_variables(include_sensitive=True)
```

### Specific Variable Retrieval
```python
# Get a specific environment variable
home_dir = await get_specific_env_var("HOME")
path_var = await get_specific_env_var("PATH")

# Check if a variable exists
api_key = await get_specific_env_var("API_KEY")
if api_key["exists"]:
    print(f"API key is set: {api_key['value']}")
```

### PATH Variable Analysis
```python
# Get detailed PATH information
path_info = await get_path_variables()

# Access individual components
for path in path_info["path_variables"]["PATH"]["paths"]:
    print(f"PATH component: {path}")
```

### Filtered Environment Analysis
```python
# Find all Java-related environment variables
java_vars = await get_environment_variables(pattern="java")

# Find all development-related variables
dev_vars = await get_environment_variables(pattern="dev")

# Get system information
system_info = await get_environment_variables()
platform = system_info["system_info"]["platform"]
```

## Error Handling

The server includes comprehensive error handling for common scenarios:
- Missing environment variables
- Invalid pattern matching
- System information retrieval errors
- Permission issues accessing environment variables

All errors are logged and returned with descriptive messages to help with debugging.

## Common Use Cases

### Development Environment Analysis
- Check for required environment variables
- Verify development tool configurations
- Analyze PATH settings for missing tools
- Identify configuration conflicts

### System Configuration Review
- Audit environment variable settings
- Check for security-related variables
- Verify system path configurations
- Platform-specific environment analysis

### Troubleshooting
- Diagnose missing environment variables
- Check for conflicting configurations
- Verify tool installations via PATH
- Platform compatibility checks

## Requirements

- Python 3.11+
- Standard library only (no external dependencies)
- Access to system environment variables
- Appropriate permissions for environment variable access

## License

This MCP server is part of the Capgemini Innersource MCP Servers Registry. Please refer to the repository for licensing information.

## Contributing

This server is maintained as part of the larger MCP servers registry. For issues, feature requests, or contributions, please visit the [main repository](https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry).
# ServiceNow Server MCP Server

A comprehensive Model Context Protocol (MCP) server that provides ServiceNow incident management capabilities. This server enables AI assistants to interact with ServiceNow instances to manage incidents, add comments, and perform various ServiceNow operations.

## Features

### Incident Management
- **Fetch incidents** with customizable query filters
- **Create new incidents** with description and details
- **Update existing incidents** with flexible field modifications
- **Resolve incidents** with resolution notes and close codes

### Incident Operations
- **Add comments and work notes** to incidents (internal or customer-visible)
- **Get specific incidents** by sys_id for detailed information
- **Health monitoring** to check ServiceNow API connectivity

### Integration Capabilities
- **Secure authentication** using environment variables
- **Comprehensive error handling** with detailed error messages
- **Flexible API operations** supporting GET, POST, PUT, and PATCH methods

## Installation

### Prerequisites
- ServiceNow instance access
- Valid ServiceNow credentials (username/password)
- Python 3.11+

### Environment Configuration
Set up your ServiceNow credentials as environment variables:
```bash
export SERVICENOW_USER="your_username"
export SERVICENOW_PASSWORD="your_password"
```

Or create a `.env` file:
```
SERVICENOW_USER=your_username
SERVICENOW_PASSWORD=your_password
```

### Option 1: Direct UV Run (Recommended)
Use uv to run the server directly without local installation:

```json
{
  "servicenow-server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
      "servicenow-mcp-server"
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
  "servicenow-server": {
    "command": "servicenow-mcp-server",
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
  "servicenow-server": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "/path/to/ptr_mcp_servers_registry",
      "servicenow-mcp-server"
    ]
  }
}
```

### Option 1: Direct UV Run (Recommended)
Use uv to run the server directly without local installation:

```json
{
  "git-server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
      "git-mcp-server"
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
  "git-server": {
    "command": "git-mcp-server",
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
  "git-server": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "/path/to/ptr_mcp_servers_registry",
      "git-mcp-server"
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

2. **Set up environment variables:**
   ```bash
   export SERVICENOW_USER="your_username"
   export SERVICENOW_PASSWORD="your_password"
   ```

3. **Build and start all services:**
   ```bash
   make start-all
   ```

4. **Or start the ServiceNow service specifically:**
   ```bash
   make start-servicenow_server
   ```

5. **List available services:**
   ```bash
   make list-services
   ```

6. **Configure your client to use the local server:**
   In your client configuration (e.g., Claude Desktop), add the server with the local URL:
   ```json
   {
     "servicenow-server": {
       "command":"npx",
    	"args":["mcp-remote@latest","http://localhost:8003/mcp", "--allow-http"]
     }
   }
   ```

#### Available Make Commands

- `make start-all` - Start all services using Docker Compose
- `make stop-all` - Stop all services
- `make start-servicenow_server` - Start the ServiceNow service
- `make stop-servicenow_server` - Stop the ServiceNow service
- `make restart-servicenow_server` - Restart the ServiceNow service
- `make list-services` - List all available services
- `make docker-build` - Build the Docker image
- `make generate-compose` - Generate Docker Compose file

### Option 5: Remote Server Deployment

For production use or when you want to share the MCP server with multiple users, you can deploy it to a remote server.

#### Prerequisites
- Remote server with Docker and Docker Compose installed
- SSH access to the remote server
- Domain name or public IP address
- ServiceNow instance credentials

#### Deployment Steps

1. **Deploy to your remote server:**
   ```bash
   # SSH into your remote server
   ssh user@your-remote-server.com
   
   # Clone the repository
   git clone https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git
   cd ptr_mcp_servers_registry
   
   # Set up environment variables
   export SERVICENOW_USER="your_username"
   export SERVICENOW_PASSWORD="your_password"
   
   # Build and start services
   make start-all
   ```

2. **Configure firewall (if needed):**
   ```bash
   # Allow traffic on port 8003 (ServiceNow server port)
   # Check the servers/server_config.json for the list of ports to be opened
   sudo ufw allow 8003
   ```

3. **Configure your client to use the remote server:**
   In your client configuration, use the remote server URL:
   ```json
   {
     "servicenow-server": {
       "command":"npx",
    	"args":["mcp-remote@latest","http://remote-ip:8003/mcp", "--allow-http"]
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
    "servicenow-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
        "servicenow-mcp-server"
      ],
      "env": {
        "SERVICENOW_USER": "your_username",
        "SERVICENOW_PASSWORD": "your_password"
      }
    }
  }
}
```

Using npx command and remote server

```json
{
  "mcpServers": {
    "servicenow-server": {
      "command":"npx",
    	"args":["mcp-remote@latest","http://<<remote-ip>>:8003/mcp", "--allow-http"]
    }
  }
}
```

### Other MCP Clients
The server follows the standard MCP protocol and can be integrated with any MCP-compatible client using the installation methods above.

### ServiceNow Configuration
- **Base URL**: Update `SERVICENOW_BASE_URL` in the code to match your ServiceNow instance
- **Authentication**: Uses basic authentication with username/password
- **API Access**: Ensure your ServiceNow user has appropriate permissions for incident management

## Available Tools

### Incident Management

#### `get_servicenow_incidents`
Fetch incidents from ServiceNow with customizable query filters.
- **Parameters:**
  - `query` (string, optional): ServiceNow query string (default: "active=true")
- **Returns:** Dictionary containing list of incidents matching the query
- **Example queries:**
  - `"active=true"` - Get all active incidents
  - `"priority=1"` - Get high priority incidents
  - `"assigned_to=user_sys_id"` - Get incidents assigned to specific user

#### `create_servicenow_incident`
Create a new incident in ServiceNow.
- **Parameters:**
  - `short_description` (string): Short description for the incident
  - `description` (string, optional): Detailed description
- **Returns:** Dictionary containing the created incident details

#### `update_servicenow_incident`
Update an existing incident with flexible field modifications.
- **Parameters:**
  - `incident_id` (string): The sys_id of the incident to update
  - `update_data` (dict): Dictionary containing fields to update
- **Returns:** Dictionary containing the updated incident
- **Common update fields:**
  - `state`: Incident state (1=New, 2=In Progress, 3=On Hold, 6=Resolved, 7=Closed)
  - `priority`: Priority level (1=Critical, 2=High, 3=Moderate, 4=Low, 5=Planning)
  - `assigned_to`: User sys_id for assignment
  - `work_notes`: Internal work notes

#### `get_servicenow_incident_by_id`
Get detailed information for a specific incident.
- **Parameters:**
  - `incident_id` (string): The sys_id of the incident to retrieve
- **Returns:** Dictionary containing detailed incident information

### Incident Operations

#### `servicenow_incident_add_comment`
Add comments or work notes to existing incidents.
- **Parameters:**
  - `incident_id` (string): The sys_id of the incident
  - `comment` (string): The comment text to add
  - `comment_type` (string, optional): Type of comment - "work_notes" (internal) or "comments" (customer visible)
- **Returns:** Dictionary containing the updated incident

#### `servicenow_resolve_incident`
Resolve incidents with resolution details and close codes.
- **Parameters:**
  - `incident_id` (string): The sys_id of the incident to resolve
  - `resolution_notes` (string): Notes describing how the incident was resolved
  - `close_code` (string, optional): Close code (default: "Solved (Permanently)")
- **Returns:** Dictionary containing the resolved incident
- **Common close codes:**
  - "Solved (Permanently)"
  - "Solved (Workaround)"
  - "Not Solved (Not Reproducible)"
  - "Closed/Resolved by Caller"

### System Operations

#### `check_servicenow_health`
Check ServiceNow API connectivity and health status.
- **Parameters:** None
- **Returns:** Dictionary containing health status and connection details


## Usage Examples

### Basic Incident Management
```python
# Get all active incidents
incidents = await get_servicenow_incidents("active=true")

# Create a new incident
new_incident = await create_servicenow_incident(
    "Email server down", 
    "Users unable to access email since 9 AM"
)

# Get specific incident details
incident_details = await get_servicenow_incident_by_id("abc123def456")

# Update incident priority
updated_incident = await update_servicenow_incident(
    "abc123def456", 
    {"priority": "1", "state": "2"}
)
```

### Adding Comments and Resolving
```python
# Add internal work note
await servicenow_incident_add_comment(
    "abc123def456",
    "Investigated the issue, found root cause in email configuration",
    "work_notes"
)

# Add customer-visible comment
await servicenow_incident_add_comment(
    "abc123def456",
    "We are working on resolving your email access issue",
    "comments"
)

# Resolve the incident
resolved_incident = await servicenow_resolve_incident(
    "abc123def456",
    "Issue resolved by restarting email service and updating configuration",
    "Solved (Permanently)"
)
```

### Advanced Queries
```python
# Get high priority incidents assigned to specific user
high_priority = await get_servicenow_incidents(
    "priority=1^assigned_to=user_sys_id"
)

# Get incidents updated in last 24 hours
recent_updates = await get_servicenow_incidents(
    "sys_updated_on>javascript:gs.daysAgoStart(1)"
)

# Check system health
health_status = await check_servicenow_health()
```

## Error Handling

The server includes comprehensive error handling for common ServiceNow operations:
- Invalid incident IDs or sys_ids
- Network connectivity issues to ServiceNow instance
- Authentication failures
- Permission errors for specific operations
- Invalid field values or data formats
- ServiceNow API rate limiting

All errors are logged and returned with descriptive messages to help with debugging.

## ServiceNow Field Reference

### Common Incident States
- `1` - New
- `2` - In Progress
- `3` - On Hold
- `6` - Resolved
- `7` - Closed

### Priority Levels
- `1` - Critical
- `2` - High  
- `3` - Moderate
- `4` - Low
- `5` - Planning

### Important Fields
- `sys_id` - Unique identifier for the incident
- `number` - Human-readable incident number
- `short_description` - Brief description of the incident
- `description` - Detailed description
- `state` - Current state of the incident
- `priority` - Priority level
- `assigned_to` - User assigned to the incident
- `caller_id` - User who reported the incident
- `work_notes` - Internal notes (not visible to caller)
- `comments` - Customer-visible comments
- `close_notes` - Resolution details
- `close_code` - Reason for closure

## Requirements

- Python 3.11+
- ServiceNow instance access
- Valid ServiceNow user credentials with incident management permissions
- Network access to ServiceNow instance
- `requests` library for HTTP operations

## License

This MCP server is part of the Capgemini Innersource MCP Servers Registry. Please refer to the repository for licensing information.

## Contributing

This server is maintained as part of the larger MCP servers registry. For issues, feature requests, or contributions, please visit the [main repository](https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry).

## Security Considerations

- Store ServiceNow credentials securely using environment variables
- Use HTTPS for all ServiceNow API communications
- Implement proper access controls in ServiceNow for the API user
- Regularly rotate ServiceNow passwords
- Monitor API usage and access logs


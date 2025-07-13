# AWS Utils MCP Server

A comprehensive Model Context Protocol (MCP) server that provides advanced AWS S3 storage capabilities. This server enables AI assistants to upload, download, and manage files in Amazon S3 buckets with seamless integration and presigned URL generation.

## Features

### File Management
- **Upload files** to S3 buckets with automatic presigned URL generation
- **Download files** from S3 buckets to local storage
- **Save JSON results** to S3 with organized folder structure

### S3 Operations
- **Presigned URL generation** for secure file access with configurable expiration
- **Organized storage** with timestamp-based naming for result files
- **Error handling** with comprehensive logging and status reporting
- **Content type detection** for optimal file handling

## Installation

### Option 1: Direct UV Run (Recommended)
Use uv to run the server directly without local installation:

```json
{
  "aws-utils-server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
      "aws-utils-mcp-server"
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
  "aws-utils-server": {
    "command": "aws-utils-mcp-server",
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
  "aws-utils-server": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "/path/to/ptr_mcp_servers_registry",
      "aws-utils-mcp-server"
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
- AWS credentials configured

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
   make start-aws_utils_server
   ```

4. **List available services:**
   ```bash
   make list-services
   ```

5. **Configure your client to use the local server:**
   In your client configuration (e.g., Claude Desktop), add the server with the local URL:
   ```json
   {
     "aws-utils-server": {
       "command":"npx",
    	"args":["mcp-remote@latest","http://localhost:8002/mcp", "--allow-http"]
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
- AWS credentials configured on the remote server

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
   # Allow traffic on port 8002
   # Check the servers/server_config.json for the list of ports to be opened
   sudo ufw allow 8002
   ```

3. **Configure your client to use the remote server:**
   In your client configuration, use the remote server URL:
   ```json
   {
     "aws-utils-server": {
       "command":"npx",
    	"args":["mcp-remote@latest","http://remote-ip:8002/mcp", "--allow-http"]
     }
   }
   ```

## Configuration

### AWS Credentials
Ensure your AWS credentials are configured using one of these methods:

1. **AWS CLI configuration:**
   ```bash
   aws configure
   ```

2. **Environment variables:**
   ```bash
   export AWS_ACCESS_KEY_ID=your-access-key
   export AWS_SECRET_ACCESS_KEY=your-secret-key
   export AWS_DEFAULT_REGION=your-region
   ```

3. **IAM roles** (for EC2 instances or Lambda functions)

### Claude Desktop
Add to your `claude_desktop_config.json`:

Using uv command

```json
{
  "mcpServers": {
    "aws-utils-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
        "aws-utils-mcp-server"
      ]
    }
  }
}
```

Using npx command and remote server

```json
{
  "mcpServers": {
    "aws-utils-server": {
      "command":"npx",
    	"args":["mcp-remote@latest","http://<<remote-ip>>:8002/mcp", "--allow-http"]
    }
  }
}
```

### Other MCP Clients
The server follows the standard MCP protocol and can be integrated with any MCP-compatible client using the installation methods above.

## Available Tools

### File Operations

#### `download_file_from_s3`
Download a file from an S3 bucket to local storage.
- **Parameters:**
  - `bucket` (string): S3 bucket name
  - `key` (string): S3 object key (file path in bucket)
  - `file_path` (string): Local path where the file should be saved
- **Returns:** Success message or error details

#### `upload_file_to_s3`
Upload a local file to an S3 bucket and get a presigned URL.
- **Parameters:**
  - `file_path` (string): Local path to the file to upload
  - `bucket` (string): S3 bucket name
  - `key` (string): S3 object key (destination path in bucket)
- **Returns:** Presigned URL for accessing the uploaded file (expires in 1 hour)

### Data Management

#### `save_to_s3`
Save analysis results or any dictionary data to S3 in JSON format with organized folder structure.
- **Parameters:**
  - `results` (dict): Dictionary containing the data to save
  - `git_url` (string): Git repository URL (used for organizing folder structure)
  - `branch` (string): Branch name (used for organizing folder structure)
  - `s3_bucket` (string): S3 bucket name where results will be saved
- **Returns:** Presigned URL for accessing the saved results (expires in 1 hour)

## Usage Examples

### Basic File Operations
```python
# Upload a local file to S3
file_url = await upload_file_to_s3(
    file_path="/path/to/local/file.txt",
    bucket="my-bucket",
    key="uploads/file.txt"
)

# Download a file from S3
await download_file_from_s3(
    bucket="my-bucket",
    key="uploads/file.txt",
    file_path="/local/download/file.txt"
)
```

### Saving Analysis Results
```python
# Save analysis results with organized structure
analysis_results = {
    "summary": "Repository analysis complete",
    "stats": {"commits": 150, "contributors": 5},
    "languages": {"python": 75, "javascript": 25}
}

results_url = await save_to_s3(
    results=analysis_results,
    git_url="https://github.com/user/repo.git",
    branch="main",
    s3_bucket="analysis-results"
)
```

### Integration with Git Analysis
```python
# Typical workflow: analyze repository and save results
repo_path = await clone_repository("https://github.com/user/repo.git", "main")
stats = await get_git_stats(repo_path)
languages = await identify_programming_languages(repo_path)

# Combine results
combined_results = {
    "timestamp": time.time(),
    "repository_stats": stats,
    "programming_languages": languages
}

# Save to S3
results_url = await save_to_s3(
    results=combined_results,
    git_url="https://github.com/user/repo.git",
    branch="main",
    s3_bucket="repo-analysis-results"
)
```

## File Organization

The `save_to_s3` function automatically organizes files using the following structure:
```
bucket/
├── repository-name/
│   ├── branch-name/
│   │   ├── 1641234567_results.json
│   │   ├── 1641234890_results.json
│   │   └── ...
│   └── other-branch/
│       └── ...
└── other-repository/
    └── ...
```

## Error Handling

The server includes comprehensive error handling for common AWS operations:
- Invalid AWS credentials or permissions
- Network connectivity issues
- S3 bucket access errors
- File not found errors
- Upload/download failures
- Invalid bucket names or object keys

All errors are logged and returned with descriptive messages to help with debugging.

## Security Features

- **Presigned URLs** provide secure, time-limited access to S3 objects
- **IAM integration** leverages AWS Identity and Access Management
- **Temporary credentials** support for enhanced security
- **Error message sanitization** to prevent information leakage

## Requirements

- Python 3.11+
- AWS credentials configured
- boto3 library for AWS SDK operations
- Network access to AWS S3 services
- Appropriate S3 bucket permissions (read/write access)

## Required AWS Permissions

Ensure your AWS credentials have the following S3 permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```

## License

This MCP server is part of the Capgemini Innersource MCP Servers Registry. Please refer to the repository for licensing information.

## Contributing

This server is maintained as part of the larger MCP servers registry. For issues, feature requests, or contributions, please visit the [main repository](https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry).

## Troubleshooting

### Common Issues

1. **AWS Credentials Not Found**
   - Ensure AWS credentials are properly configured
   - Check environment variables or AWS CLI configuration

2. **S3 Bucket Access Denied**
   - Verify bucket permissions and IAM policies
   - Check bucket name spelling and region settings

3. **File Upload Failures**
   - Ensure sufficient permissions for the target S3 bucket
   - Check file path validity and file accessibility

4. **Presigned URL Expiration**
   - URLs expire after 1 hour by default
   - Generate new URLs for continued access

For additional support, refer to the main repository documentation or AWS S3 troubleshooting guides.
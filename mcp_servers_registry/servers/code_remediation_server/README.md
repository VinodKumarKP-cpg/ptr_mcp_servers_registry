# Code Remediation Server MCP Server

A powerful Model Context Protocol (MCP) server that provides automated code analysis and remediation capabilities for Git repositories. This server enables AI assistants to analyze codebases, identify issues, and optionally generate remediated code suggestions.

## Features

### Repository Analysis
- **Comprehensive code analysis** of Git repositories with customizable branch selection
- **Issue detection** with configurable flags to enable/disable issue identification
- **Code remediation** with optional generation of fixed code suggestions
- **Multi-language support** for various programming languages and frameworks

### Automated Code Quality
- **Static code analysis** to identify potential bugs, security vulnerabilities, and code smells
- **Best practices validation** against industry standards and coding conventions
- **Performance optimization** suggestions and recommendations
- **Code structure analysis** for maintainability and readability improvements

## Installation

### Option 1: Direct UV Run (Recommended)
Use uv to run the server directly without local installation:

```json
{
  "code-remediation-server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
      "code-remediation-server"
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
  "code-remediation-server": {
    "command": "code-remediation-server",
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
  "code-remediation-server": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "/path/to/ptr_mcp_servers_registry",
      "code-remediation-server"
    ]
  }
}
```

## Configuration

### Claude Desktop
Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "code-remediation-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
        "code-remediation-server"
      ]
    }
  }
}
```

### Other MCP Clients
The server follows the standard MCP protocol and can be integrated with any MCP-compatible client using the installation methods above.

## Available Tools

### Repository Analysis

#### `analyze_repository`
Perform comprehensive analysis of a Git repository with configurable options for issue detection and code remediation.

- **Parameters:**
  - `git_url` (string): Git repository URL to analyze
  - `branch` (string, optional): Branch to analyze (default: "main")
  - `issue_flag` (boolean, optional): Flag to indicate if issues should be identified (default: True)
  - `remediated_code` (boolean, optional): Flag to indicate if remediated code should be returned (default: False)

- **Returns:** Dictionary containing comprehensive analysis results including:
  - Identified issues and their severity levels
  - Code quality metrics and recommendations
  - Remediated code suggestions (if enabled)
  - Analysis summary and statistics

## Usage Examples

### Basic Repository Analysis
```python
# Analyze a repository for issues only
result = await analyze_repository(
    git_url="https://github.com/user/repo.git",
    branch="main",
    issue_flag=True,
    remediated_code=False
)
```

### Full Analysis with Remediation
```python
# Analyze repository and get remediated code suggestions
result = await analyze_repository(
    git_url="https://github.com/user/repo.git",
    branch="develop",
    issue_flag=True,
    remediated_code=True
)
```

### Quick Code Review
```python
# Perform analysis without issue detection (faster)
result = await analyze_repository(
    git_url="https://github.com/user/repo.git",
    issue_flag=False,
    remediated_code=False
)
```

### Branch-Specific Analysis
```python
# Analyze a specific feature branch
result = await analyze_repository(
    git_url="https://github.com/user/repo.git",
    branch="feature/new-feature",
    issue_flag=True,
    remediated_code=True
)
```

## Analysis Results Structure

The `analyze_repository` tool returns a comprehensive dictionary with the following structure:

```json
{
  "repository_info": {
    "url": "string",
    "branch": "string",
    "analysis_timestamp": "string"
  },
  "issues": [
    {
      "file": "string",
      "line": "number",
      "severity": "string",
      "type": "string",
      "description": "string",
      "recommendation": "string"
    }
  ],
  "metrics": {
    "code_quality_score": "number",
    "security_score": "number",
    "maintainability_score": "number",
    "performance_score": "number"
  },
  "remediated_code": {
    "files": [
      {
        "path": "string",
        "original_content": "string",
        "remediated_content": "string",
        "changes_summary": "string"
      }
    ]
  },
  "summary": {
    "total_issues": "number",
    "critical_issues": "number",
    "files_analyzed": "number",
    "languages_detected": ["string"]
  }
}
```

## Common Use Cases

### Code Review Automation
- **Pull Request Analysis**: Analyze feature branches before merging
- **Quality Gate Integration**: Automated quality checks in CI/CD pipelines
- **Security Scanning**: Identify security vulnerabilities in codebases

### Development Workflow
- **Pre-commit Analysis**: Check code quality before committing changes
- **Refactoring Assistance**: Get suggestions for code improvements
- **Learning Tool**: Understand best practices through remediation suggestions

### Project Maintenance
- **Technical Debt Assessment**: Identify areas needing improvement
- **Code Modernization**: Get suggestions for updating legacy code
- **Performance Optimization**: Find and fix performance bottlenecks

## Error Handling

The server includes robust error handling for various scenarios:
- Invalid repository URLs or inaccessible repositories
- Network connectivity issues during repository cloning
- Unsupported file types or programming languages
- Analysis timeout for large repositories
- Permission errors when accessing private repositories

All errors are logged with detailed information and returned with user-friendly messages.

## Performance Considerations

- **Repository Size**: Large repositories may take longer to analyze
- **Branch Selection**: Analyze specific branches to reduce processing time
- **Issue Detection**: Disable issue detection for faster analysis when not needed
- **Remediation Generation**: Code remediation increases processing time significantly

## Requirements

- Python 3.11+
- Git installed and accessible in PATH
- Network access for cloning repositories
- Sufficient disk space for temporary repository storage
- Memory requirements scale with repository size

## Security

- Temporary repositories are automatically cleaned up after analysis
- No persistent storage of analyzed code
- Network requests are limited to Git operations
- All analysis is performed locally without external API calls

## License

This MCP server is part of the Capgemini Innersource MCP Servers Registry. Please refer to the repository for licensing information.

## Contributing

This server is maintained as part of the larger MCP servers registry. For issues, feature requests, or contributions, please visit the [main repository](https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry).

## Support

For technical support, troubleshooting, or questions about the code remediation server, please:
1. Check the [main repository documentation](https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry)
2. Open an issue in the repository
3. Consult the MCP protocol documentation for integration questions

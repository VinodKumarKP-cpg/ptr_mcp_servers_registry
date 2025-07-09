# MCP Servers Registry

A comprehensive collection of Model Context Protocol (MCP) servers designed to extend AI assistant capabilities with powerful development tools and utilities. This registry provides production-ready MCP servers for Git operations, code analysis, and repository management.

## Overview

The MCP Servers Registry is a curated collection of high-quality MCP servers that enable AI assistants to perform complex development tasks. Each server is designed to be easily integrated into existing MCP-compatible clients and provides specialized functionality for software development workflows.

## Available Servers

### 🔧 Git Server
**Location:** `git_server/`  
**Command:** `git-mcp-server`

A comprehensive Git repository analysis and management server that provides advanced capabilities for working with Git repositories.

**Key Features:**
- Repository cloning and management
- Comprehensive Git statistics and analysis
- Programming language detection
- Commit history analysis and search
- Contributor statistics
- Repository structure visualization

**Tools:** `clone_repository`, `get_file_list`, `get_git_stats`, `get_commit_history`, `identify_programming_languages`, `get_repository_structure`, `get_contributor_stats`, `search_commits`, `cleanup_repository`

### 🛠️ Code Remediation Server
**Location:** `code_remediation_server/`  
**Command:** `code-remediation-server`

An automated code analysis and remediation server that identifies issues and provides code improvement suggestions.

**Key Features:**
- Comprehensive code analysis
- Issue detection and classification
- Automated code remediation suggestions
- Multi-language support
- Security vulnerability scanning
- Performance optimization recommendations

**Tools:** `analyze_repository`

## Quick Start

### Installation Methods

#### Option 1: Direct UV Run (Recommended)
The fastest way to get started - no local installation required:

```json
{
  "mcpServers": {
    "git-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
        "git-mcp-server"
      ]
    },
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

#### Option 2: Pip Install + Run
Install once, then run the servers:

```bash
pip install git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git
```

```json
{
  "mcpServers": {
    "git-server": {
      "command": "git-mcp-server",
      "args": []
    },
    "code-remediation-server": {
      "command": "code-remediation-server",
      "args": []
    }
  }
}
```

#### Option 3: Local Development
Clone the repository for local development:

```bash
git clone https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git
cd ptr_mcp_servers_registry
```

```json
{
  "mcpServers": {
    "git-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/ptr_mcp_servers_registry",
        "git-mcp-server"
      ]
    },
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
}
```

### Claude Desktop Configuration

Add to your `claude_desktop_config.json` file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "git-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "git+https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git",
        "git-mcp-server"
      ]
    },
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

## Usage Examples

### Complete Repository Analysis Workflow

```python
# 1. Clone and analyze repository with Git Server
repo_path = await clone_repository("https://github.com/user/repo.git", "main")
git_stats = await get_git_stats(repo_path)
languages = await identify_programming_languages(repo_path)

# 2. Perform code analysis with Code Remediation Server
analysis = await analyze_repository(
    git_url="https://github.com/user/repo.git",
    branch="main",
    issue_flag=True,
    remediated_code=True
)

# 3. Get detailed commit history
commits = await get_commit_history(repo_path, limit=50)
contributors = await get_contributor_stats(repo_path)

# 4. Clean up
await cleanup_repository(repo_path)
```

### Code Review Automation

```python
# Analyze a feature branch for code review
pr_analysis = await analyze_repository(
    git_url="https://github.com/user/repo.git",
    branch="feature/new-feature",
    issue_flag=True,
    remediated_code=True
)

# Get commit history for the feature branch
feature_commits = await get_commit_history(
    repo_path,
    limit=20,
    since_days=7
)
```

### Repository Discovery and Insights

```python
# Get comprehensive repository insights
repo_structure = await get_repository_structure(repo_path, max_depth=3)
file_list = await get_file_list(repo_path)
recent_commits = await search_commits(repo_path, "feature", limit=10)
```

## Project Structure

```
ptr_mcp_servers_registry/
├── README.md                          # This file
├── pyproject.toml                     # Project configuration
├── requirements.txt                   # Python dependencies
├── git_server/                        # Git Server MCP implementation
│   ├── server.py                      # Main server implementation
│   └── README.md                      # Git Server documentation
├── code_remediation_server/           # Code Remediation Server implementation
│   ├── server.py                      # Main server implementation
│   └── README.md                      # Code Remediation Server documentation
├── mcp_servers_registry/              # Shared utilities and common code
│   └── utils/                         # Utility modules
│       ├── git_utils.py               # Git operations utilities
│       ├── code_remediation_utils.py  # Code analysis utilities
│       └── logger_utils.py            # Logging utilities
├── tests/                             # Test suite
│   ├── test_git_server.py             # Git Server tests
│   └── test_code_remediation.py       # Code Remediation tests
└── docs/                              # Additional documentation
    ├── installation.md                # Detailed installation guide
    ├── development.md                 # Development guidelines
    └── troubleshooting.md             # Common issues and solutions
```

## Common Use Cases

### For Development Teams
- **Code Review Automation**: Analyze pull requests before merging
- **Repository Health Monitoring**: Track code quality and contributor activity
- **Technical Debt Assessment**: Identify areas needing improvement
- **Security Scanning**: Automated vulnerability detection

### For Project Managers
- **Progress Tracking**: Monitor development activity and contributions
- **Quality Metrics**: Track code quality trends over time
- **Resource Planning**: Understand codebase complexity and requirements
- **Risk Assessment**: Identify potential issues before they become problems

### For DevOps Engineers
- **CI/CD Integration**: Automated quality gates and checks
- **Repository Analytics**: Comprehensive insights into development patterns
- **Performance Monitoring**: Track repository and code performance metrics
- **Compliance Checking**: Ensure code meets organizational standards

## Development

### Prerequisites
- Python 3.8 or higher
- Git installed and accessible in PATH
- UV package manager (recommended) or pip
- Network access for repository cloning

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/Capgemini-Innersource/ptr_mcp_servers_registry.git
cd ptr_mcp_servers_registry

# Install dependencies
uv sync

# Run a specific server for development
uv run git-mcp-server
# or
uv run code-remediation-server
```

### Adding New Servers

1. Create a new directory for your server: `new_server/`
2. Implement the server using FastMCP framework and name the script as 'server.py'
3. Add utility functions to `mcp_servers_registry/utils/`
4. Add documentation and README
5. Add an entry in pyproject.toml under the section "[project.scripts]" as follows:
```commandline
<<mcp-server-name>> = "mcp_servers_registry.servers.<<mcp server package name>>.server:main"
```
6. Update the main project README with summary details of the server.


## Security Considerations

- **Repository Access**: Servers only access public repositories or those you have permissions for
- **Temporary Storage**: All cloned repositories are automatically cleaned up
- **Network Security**: All operations are performed locally without external API calls
- **Data Privacy**: No code or analysis results are stored persistently
- **Permission Model**: Servers run with user-level permissions only

## Troubleshooting

### Common Issues

**Server Won't Start**
- Verify Python 3.11+ is installed
- Check that Git is accessible in PATH
- Ensure UV is installed and up to date
- Verify network connectivity for repository access

**Repository Clone Failures**
- Check repository URL format
- Verify repository accessibility (public/private permissions)
- Ensure sufficient disk space
- Check network connectivity

## Contributing

We welcome contributions to the MCP Servers Registry! Please follow these guidelines:

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Implement your changes with tests
4. Ensure all tests pass
5. Submit a pull request with detailed description

### Documentation Contributions
- Improve existing documentation
- Add usage examples
- Create tutorials and guides
- Report and fix documentation issues

### Bug Reports
- Use the GitHub issue tracker
- Provide detailed reproduction steps
- Include system information and logs
- Suggest potential solutions if possible

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For support, questions, or feature requests:

1. **Documentation**: Check the `docs/` directory for detailed guides
2. **Issues**: Use the GitHub issue tracker for bug reports and feature requests
3. **Discussions**: Join repository discussions for questions and community support
4. **Enterprise Support**: Contact the maintainers for enterprise-level support

## Roadmap

### Future Servers
- **Service Now Server**: Service now reporting and analysis
- **Documentation Server**: Automated documentation generation and analysis
- **Testing Server**: Test coverage analysis and test generation

## Acknowledgments

- Built on the Model Context Protocol (MCP) framework
- Powered by FastMCP for rapid server development
- Utilizes industry-standard Git operations and analysis tools
- Inspired by the needs of modern development teams

---

**Version**: 1.0.0  
**Last Updated**: July 2025  
**Maintainer**: Capgemini Innersource Team
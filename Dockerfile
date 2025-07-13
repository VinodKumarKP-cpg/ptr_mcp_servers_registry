# Runtime Generic Dockerfile for MCP Servers
FROM python:3.11-slim

ARG GITHUB_TOKEN
# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"\
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire mcp_servers_registry package
COPY mcp_servers_registry/ ./mcp_servers_registry/
COPY MANIFEST.in ./

# Install the package in development mode
RUN pip install -e .

# Create entrypoint script (as root)
RUN cat > /app/entrypoint.sh << 'EOF'
#!/bin/bash
if [ -z "$MCP_SERVER_NAME" ]; then
    echo "Error: MCP_SERVER_NAME environment variable is required"
    exit 1
fi
exec python -m mcp_servers_registry.servers.${MCP_SERVER_NAME}.server "$@"
EOF

# Make script executable and set ownership
RUN chmod +x /app/entrypoint.sh && \
    git config --system url.https://oauth2:${GITHUB_TOKEN}@github.com/Capgemini-Innersource.insteadOf https://github.com/Capgemini-Innersource

# Create a non-root user and change ownership
RUN useradd -m -u 1000 mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
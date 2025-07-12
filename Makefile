define RUN_MCP_SERVER
 @if docker ps -a --format '{{.Names}}' | grep -w $(3); then \
  echo "Container $(1) already exists and running"; \
 else \
  $(MAKE) docker-build; \
  docker run --rm -d -p ${2}:${2} --name $(1) \
  --env MCP_SERVER_NAME=${1} mcp_server:latest --transport sse; \
 fi
endef

define KILL_MCP_SERVER
 @if docker ps -a --format '{{.Names}}' | grep -w $(1); then \
  docker kill $(1); \
 else \
  echo "Container $(1) does not exist."; \
 fi
endef

install:
	pip install .

uninstall:
	pip uninstall mcp-server-registry

docker-build:
	docker build -f Dockerfile . -t mcp_server

docker-run-git-mcp-server:
	$(call RUN_MCP_SERVER,git_server,8000,mcp-git-server)

docker-kill-git-mcp-server:
	$(call KILL_MCP_SERVER,mcp-git-server)

docker-run-code-remediation-mcp-server:
	$(call RUN_MCP_SERVER,code_remediation_server,8001,mcp-code-remediation-server)

docker-kill-code-remediation-mcp-server:
	$(call KILL_MCP_SERVER,mcp-code-remediation-server)

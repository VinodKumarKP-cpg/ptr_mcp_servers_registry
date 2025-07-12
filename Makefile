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
  docker rm $(1); \
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

docker-run-mcp-git-server:
	$(call RUN_MCP_SERVER,git_server,8000,mcp-git-server)

docker-kill-mcp-git-server:
	$(call KILL_MCP_SERVER,mcp-git-server)

docker-run-mcp-code-remediation-server:
	$(call RUN_MCP_SERVER,code_remediation_server,8001,mcp-code-remediation-server)

docker-kill-mcp-code-remediation-server:
	$(call KILL_MCP_SERVER,mcp-code-remediation-server)

up-all-server:
	$(MAKE) docker-build
	docker compose up -d

up-down-server:
	docker compose down

up-mcp-git-server:
	docker compose up -d git_server

up-mcp-code-remediation-server:
	docker compose up -d code_remediation_server
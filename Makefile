install:
	pip install .

uninstall:
	pip uninstall mcp-server-registry

docker-build:
	docker build -f dockerfiles/Dockerfile.base . -t mcp_server

docker-run-git-server:
	$(MAKE) docker-build
	docker run --rm  --env MCP_SERVER_NAME=git_server -p 8000:8000 mcp_server:latest --transport sse

docker-run-code-remediation-server:
	$(MAKE) docker-build
	docker run --rm  --env MCP_SERVER_NAME=code_remediation_server --env RESULTS_BUCKET=${RESULTS_BUCKET} -p 8001:8001 mcp_server:latest --transport sse

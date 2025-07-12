SERVICES_DIR := ./mcp_servers_registry/servers
SERVICES := $(shell find $(SERVICES_DIR) -maxdepth 1 -type d -not -path $(SERVICES_DIR) -exec basename {} \;)

define KILL_MCP_SERVER
 @if docker ps --format '{{.Names}}' | grep -w $(1); then \
  echo "Stopping and removing container $(1)"; \
  docker stop $(1) && docker rm $(1); \
 elif docker ps -a --format '{{.Names}}' | grep -w $(1); then \
  echo "Removing stopped container $(1)"; \
  docker rm $(1); \
 else \
  echo "Container $(1) does not exist."; \
 fi
endef

define RUN_MCP_SERVER
 @if docker ps --format '{{.Names}}' | grep -w $(1); then \
  echo "Container $(1) is already running"; \
 else \
  if docker ps -a --format '{{.Names}}' | grep -w $(1); then \
   echo "Removing existing stopped container $(1)"; \
   docker rm $(1); \
  fi; \
  $(MAKE) docker-build; \
  docker run --rm -d -p $(2):$(2) --name $(1) \
  --env MCP_SERVER_NAME=$(1) mcp_server:latest --transport sse; \
 fi
endef

define RUN_DOCKER_COMPOSE
 $(MAKE) docker-build
 echo "Executing compose up";
 @if [ -z "$(1)" ]; then \
  docker compose up -d; \
 else \
  docker compose up -d $(1); \
 fi;
endef

define DOWN_DOCKER_COMPOSE
 echo "Executing compose down";
 @if [ -z "$(1)" ]; then \
  docker compose down; \
 else \
  docker compose stop $(1) && docker compose rm -f $(1); \
 fi;
endef

install:
	pip install .

uninstall:
	pip uninstall mcp-server-registry

docker-build:
	docker build -f Dockerfile . -t mcp_server

start-all:
	$(call RUN_DOCKER_COMPOSE)

stop-all:
	$(call DOWN_DOCKER_COMPOSE)

# List all discovered services
list-services:
	@echo "Discovered services:"
	@for service in $(SERVICES); do \
		echo "  - $$service"; \
	done


# Template for generating service targets
define SERVICE_TEMPLATE
start-$(1):
	@echo "Starting service: $(1)"
	$$(call RUN_DOCKER_COMPOSE,$(1))

stop-$(1):
	@echo "Stopping service: $(1)"
	$$(call DOWN_DOCKER_COMPOSE,$(1))

restart-$(1): stop-$(1) start-$(1)
	@echo "Restarted service: $(1)"
endef

# Generate targets for each service
$(foreach service,$(SERVICES),$(eval $(call SERVICE_TEMPLATE,$(service))))


help:
	@echo "Available commands:"
	@echo "  install                Install the Python package"
	@echo "  uninstall              Uninstall the Python package"
	@echo "  docker-build           Build the MCP server Docker image"
	@echo "  start-all              Start all services using docker compose"
	@echo "  stop-all               Stop all services using docker compose"
	@echo "  list-services          List all discovered services"
	@echo "  start-<service>        Start a specific service (replace <service> with name)"

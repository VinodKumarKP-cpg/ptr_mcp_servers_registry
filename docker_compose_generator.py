#!/usr/bin/env python3.11

import json
import yaml
import sys
from pathlib import Path


def load_server_config(config_file: str) -> dict:
    """Load server configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{config_file}': {e}")
        sys.exit(1)


def generate_service_config(service_name: str, config: dict) -> dict:
    """Generate Docker Compose service configuration."""
    port = config.get('port')

    # Base environment variables - always include MCP_SERVER_NAME
    environment = [f'MCP_SERVER_NAME={service_name}']

    # Add environment variables from config
    env_vars = config.get('environment', {})
    for key, value in env_vars.items():
        environment.append(f'{key}={value}')

    return {
        'build': {
            'context': '.',
            'dockerfile': 'Dockerfile'
        },
        'container_name': f'mcp-{service_name.replace("_", "-")}',
        'ports': [f"{port}:{port}"],
        'volumes': ['./logs:/tmp'],
        'environment': environment,
        'command': '--transport streamable-http',
        'restart': 'unless-stopped',
        'networks': ['mcp-network'],
        'healthcheck': {
            'test': ['CMD', 'curl', '-f', f'http://localhost:{port}/health'],
            'interval': '30s',
            'timeout': '10s',
            'retries': 3
        }
    }


def generate_docker_compose(server_config: dict) -> dict:
    """Generate complete Docker Compose configuration."""
    services = {}

    for service_name, config in server_config.items():
        port = config.get('port')
        if port is None:
            print(f"Warning: No port specified for service '{service_name}', skipping...")
            continue

        services[service_name] = generate_service_config(service_name, config)

    # Environment variables are already handled per service in generate_service_config

    return {
        'version': '3.8',
        'services': services,
        'networks': {
            'mcp-network': {
                'driver': 'bridge',
                'ipam': {
                    'config': [
                        {'subnet': '172.21.0.0/16'}
                    ]
                }
            }
        }
    }


def write_docker_compose(compose_config: dict, output_file: str = 'docker-compose.yaml'):
    """Write Docker Compose configuration to YAML file."""
    try:
        with open(output_file, 'w') as f:
            yaml.dump(compose_config, f, default_flow_style=False, sort_keys=False, indent=2, width=1000)
        print(f"Docker Compose file generated successfully: {output_file}")
    except Exception as e:
        print(f"Error writing Docker Compose file: {e}")
        sys.exit(1)


def main():
    """Main function to generate Docker Compose file."""
    # Default configuration file
    config_file = 'mcp_servers_registry/servers/server_config.json'
    output_file = 'docker-compose.yaml'

    # Parse command line arguments
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    print(f"Loading configuration from: {config_file}")

    # Load server configuration
    server_config = load_server_config(config_file)

    # Generate Docker Compose configuration
    compose_config = generate_docker_compose(server_config)

    # Write to file
    write_docker_compose(compose_config, output_file)

    # Print summary
    print(f"\nGenerated services:")
    for service_name, config in server_config.items():
        port = config.get('port', 'N/A')
        print(f"  - {service_name}: port {port}")


if __name__ == '__main__':
    main()
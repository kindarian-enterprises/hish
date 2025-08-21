#!/bin/bash

# MCP stdio server runner for Kindarian Cursor Context
# This script runs the MCP server in stdio mode for Cursor integration

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Check if Docker is available
if command -v docker &> /dev/null; then
    # Run MCP server via Docker
    docker compose -f compose.rag.yml --env-file env.framework run --rm -i mcp-qdrant-stdio
else
    echo "Docker not found. Please install Docker to use this MCP server." >&2
    exit 1
fi

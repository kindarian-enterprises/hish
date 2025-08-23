#!/usr/bin/env bash
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the project directory
cd "$PROJECT_DIR"

# Ensure Qdrant is up
docker compose -f compose.rag.yml --env-file env.mcp up -d qdrant

# Wait for Qdrant to be ready
sleep 5

# Run LlamaIndex MCP server in STDIO mode
exec docker compose -f compose.rag.yml --env-file env.mcp run --rm -i mcp-qdrant-llamaindex

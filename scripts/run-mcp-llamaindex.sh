#!/usr/bin/env bash
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the project directory
cd "$PROJECT_DIR"

# Ensure Qdrant is up
docker compose -f deploy/compose.rag.yml --env-file config/env.mcp up -d qdrant

# Wait for Qdrant to be ready
sleep 5

# Run LlamaIndex MCP server in STDIO mode
exec docker compose -f deploy/compose.rag.yml run --rm -i mcp-qdrant-llamaindex

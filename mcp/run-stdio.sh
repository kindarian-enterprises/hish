#!/usr/bin/env bash
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the project directory
cd "$PROJECT_DIR"

# Ensure Qdrant is up
docker compose -f ops/compose.rag.yml --env-file .env up -d qdrant

# Run MCP in STDIO mode attached to this terminal's stdin/stdout
exec docker compose -f ops/compose.rag.yml --env-file .env run --rm -i mcp-qdrant-stdio

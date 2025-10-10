#!/usr/bin/env bash
# MCP Server Launcher - Unified (Documentation/Framework)
# Single MPNet-based server for all markdown/doc collections

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Ensure Qdrant is up
docker compose -f deploy/compose.rag.yml --env-file config/env.mpnet up -d qdrant

# Wait for Qdrant to be ready
sleep 5

# Spawn MCP server via docker compose
exec docker compose -f deploy/compose.rag.yml run --rm -i mcp-qdrant-unified

#!/bin/bash
# Unified MCP Server Startup Script
# Uses MPNet embeddings for all collections

set -e

# Change to the correct directory (script may be called from anywhere)
cd "$(dirname "$0")/.."

# Start Qdrant if not already running (silently)
docker compose -f deploy/compose.rag.yml up -d qdrant >/dev/null 2>&1

# Start the unified MCP server (no echo output to avoid JSON parsing issues)
exec docker compose -f deploy/compose.rag.yml run --rm -i mcp-qdrant-unified

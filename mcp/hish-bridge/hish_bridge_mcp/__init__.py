"""
Hish MCP Bridge for Claude Code

Exposes Hish's Qdrant knowledge collections to Claude Code via MCP protocol.

Usage:
    python -m hish_bridge_mcp.server

Environment Variables:
    QDRANT_URL: Qdrant server URL (default: http://localhost:6333)
    QDRANT_API_KEY: Optional API key for Qdrant Cloud
"""

__version__ = "0.1.0"

from hish_bridge_mcp.server import (
    hish_find,
    hish_find_framework,
    hish_find_intelligence,
    hish_find_project,
    hish_store,
    hish_collections,
    main,
)

__all__ = [
    "hish_find",
    "hish_find_framework",
    "hish_find_intelligence",
    "hish_find_project",
    "hish_store",
    "hish_collections",
    "main",
]

# Hish MCP Bridge for Claude Code

MCP server that exposes Hish's Qdrant knowledge collections to Claude Code. Uses the same FastEmbed model and normalization as the Hish indexer for query compatibility.

## Installation

The MCP server is intended to run from a **virtualenv** managed by Hish so dependencies don’t conflict with your project. From Hish repo root:

```bash
make install-claude-code-mcp
```

This creates `hish/.venv-claude-mcp/` and installs this package into it. Project setup (`make setup-claude-code PROJECT=...`) then writes `.mcp.json` with `command` pointing at that venv’s Python.

To install into the current environment (e.g. for development):

```bash
cd hish/mcp/hish-bridge
pip install -e .
```

## Configuration

`make setup-claude-code PROJECT=...` generates `.mcp.json` for you with `command` set to the venv Python, e.g.:

```json
{
  "mcpServers": {
    "hish-knowledge": {
      "command": "/path/to/hish/.venv-claude-mcp/bin/python",
      "args": ["-m", "hish_bridge_mcp.server"],
      "env": {
        "QDRANT_URL": "http://localhost:6333"
      }
    }
  }
}
```

Use the venv’s Python so the server runs with the correct dependencies.

## Tools

| Tool | Purpose |
|------|---------|
| `hish_find` | Search multiple collections |
| `hish_find_framework` | Framework docs only |
| `hish_find_intelligence` | Cross-project patterns only |
| `hish_find_project` | Project-specific docs |
| `hish_store` | Store patterns (intelligence only) |
| `hish_collections` | List collections |

## Collections

| Collection | Access |
|------------|--------|
| `hish_framework_mpnet` | Read-only |
| `cross_project_intelligence_mpnet` | Read/Write |
| `{project}_docs_mpnet` | Read-only |

## Requirements

- Qdrant running (e.g. `docker compose -f deploy/compose.rag.yml up -d qdrant`)
- Collections indexed by Hish (e.g. `make index` from Hish root)

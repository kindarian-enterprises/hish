# Claude Code Integration

Hish can provide the same knowledge-driven workflow (framework docs, cross-project intelligence, pattern storage) inside **Claude Code** via an MCP bridge, `CLAUDE.md` directives, and slash commands.

## Overview

- **CLAUDE.md** – Injected into every Claude Code conversation; describes when to use Hish MCP tools vs native code tools.
- **MCP bridge** – Python package `hish_bridge_mcp` that exposes `hish_find`, `hish_find_framework`, `hish_find_intelligence`, `hish_store`, etc., using the same Qdrant collections and embedding model as the Hish indexer.
- **Slash commands** – `/dev` (activate Hish agent, run mandatory queries) and `/end-dev` (session end, pattern capture).

## Prerequisites

- Hish framework set up (Qdrant running, collections indexed).
- Python 3.10+ on your PATH (for creating the venv).
- Claude Code installed.

## Setup

### 1. Install the MCP bridge (once)

The MCP server runs inside a **dedicated virtualenv** in the Hish repo so its dependencies don’t clash with your project. From Hish repo root:

```bash
make install-claude-code-mcp
```

This creates `.venv-claude-mcp/` in the Hish root and installs `hish-bridge-mcp` into it. The venv is gitignored.

Verify:

```bash
./.venv-claude-mcp/bin/python -c "import hish_bridge_mcp; print('OK')"
```

### 2. Configure a project

From Hish repo root:

```bash
make setup-claude-code PROJECT=/path/to/your/project
```

Example:

```bash
make setup-claude-code PROJECT=~/projects/vara
```

This creates in the project:

- `CLAUDE.md` – Agent directives with placeholders filled.
- `.claude/commands/dev.md` – `/dev` command.
- `.claude/commands/end-dev.md` – `/end-dev` command.
- `.mcp.json` – MCP server config: `command` is the **absolute path** to the venv Python (e.g. `/path/to/hish/.venv-claude-mcp/bin/python`), so Claude Code runs the server with that environment.

### 3. Restart Claude Code

Restart Claude Code so it loads `.mcp.json` and the new commands.

### 4. Ensure Qdrant is running

From Hish root:

```bash
docker compose -f deploy/compose.rag.yml up -d qdrant
```

Index framework and project docs if needed:

```bash
make index
```

## Using Hish in Claude Code

1. **Start a session** – In Claude Code, type `/dev` and send. Claude will run the mandatory initialization queries and declare activation.
2. **During work** – Use `hish_find_framework()` and `hish_find_intelligence()` for patterns; use Claude Code’s native tools for code and files.
3. **End a session** – Type `/end-dev` to summarize and optionally store patterns with `hish_store()` (always ask the user before storing).

## MCP tools

| Tool | Purpose |
|------|---------|
| `hish_find(query, collections, limit)` | Search one or more collections |
| `hish_find_framework(query)` | Framework docs, workflows, templates |
| `hish_find_intelligence(query)` | Cross-project patterns, learnings |
| `hish_find_project(query, project)` | Project-specific docs (`{project}_docs_mpnet`) |
| `hish_store(content, pattern_type, project, tags, evidence)` | Store pattern (intelligence collection only; get user approval first) |
| `hish_collections()` | List collections and status |

## Optional: .gitignore

If you prefer not to commit generated Hish files:

```
CLAUDE.md
.mcp.json
```

The template files in `hish/templates/claude-code/` remain tracked in the Hish repo.

## Troubleshooting

### "ModuleNotFoundError: hish_bridge_mcp"

Install the bridge into the dedicated venv, then re-run project setup so `.mcp.json` points at that venv’s Python:

```bash
cd /path/to/hish && make install-claude-code-mcp
make setup-claude-code PROJECT=/path/to/your/project
```

`.mcp.json` must use the **absolute path** to `hish/.venv-claude-mcp/bin/python`. If you moved the Hish repo, run `make setup-claude-code PROJECT=...` again to refresh the path.

### MCP tools not visible in Claude Code

- Confirm `.mcp.json` exists in the project root and contains the `hish-knowledge` server entry.
- Restart Claude Code after changing `.mcp.json`.
- Check Claude Code’s MCP / extension logs for connection errors.

### Empty or irrelevant search results

- Check Qdrant: `curl -s http://localhost:6333/collections`.
- Ensure framework (and project) docs are indexed from Hish root: `make index`.
- The bridge uses the same embedding model as the Hish indexer; collections must be created and filled by Hish (e.g. `make index-framework`, `make index-repo`).

### `/dev` or `/end-dev` not appearing

- Ensure `.claude/commands/dev.md` and `.claude/commands/end-dev.md` exist (from `make setup-claude-code PROJECT=...`).
- Restart Claude Code so it rescans the `.claude/commands/` directory.

## Related documentation

- [Getting Started](getting-started.md) – Initial Hish setup.
- [Portable Context](portable-context.md) – Syncing `local/` across machines.
- [Agent Workflows](../agent-management/agent-workflows.md) – How agents use context.
- **mcp/hish-bridge/README.md** – MCP bridge package details.

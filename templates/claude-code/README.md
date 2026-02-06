# Hish Claude Code Templates

Templates for integrating Hish with Claude Code (MCP + CLAUDE.md + slash commands).

## Contents

- **CLAUDE.md.template** – Project-level agent directives (tool strategy, knowledge-first, collections). Placeholders: `{{PROJECT_NAME}}`, `{{HISH_ROOT}}`, `{{TIMESTAMP}}`, `{{QDRANT_URL}}`.
- **commands/dev.md.template** – `/dev` slash command: initialize Hish development agent and run mandatory queries.
- **commands/end-dev.md.template** – `/end-dev` slash command: session end and pattern capture.

## Usage

Do not copy these by hand. Use the setup script from Hish root:

```bash
make install-claude-code-mcp   # Once: install MCP bridge
make setup-claude-code PROJECT=/path/to/your/project
```

This creates in the project:

- `CLAUDE.md` (from template with placeholders replaced)
- `.claude/commands/dev.md` and `.claude/commands/end-dev.md`
- `.mcp.json` (MCP server config for `hish_bridge_mcp`)

## Command behavior

- **`/dev`** – Loads the activation prompt and tells the agent to run `hish_find_framework(...)` and `hish_find_intelligence(...)` before starting.
- **`/end-dev`** – Asks for session summary and offers to store patterns via `hish_store(...)` with user approval.

## Troubleshooting

- **Commands not showing in Claude Code** – Ensure `.claude/commands/*.md` exist and restart Claude Code.
- **MCP tools not available** – Restart Claude Code after creating `.mcp.json`; confirm `hish_bridge_mcp` is installed (`python -c "import hish_bridge_mcp"`).
- **Empty or wrong search results** – Ensure Qdrant is running and Hish collections are indexed (`make index` from Hish root).

See **docs/setup/claude-code-integration.md** for full setup and troubleshooting.

# Getting Started

## Prerequisites

Check the main [README Prerequisites](../README.md#prerequisites) first.

**Required**: Docker 20.10+, Git 2.20+, Make 3.81+, Python 3.8+

## Setup

```bash
# 1. Clone and setup
git clone https://github.com/kindarian-enterprises/hish.git
cd hish
make quick-start

# 2. Configure Cursor integration (builds MCP server with pre-warmed model)
make setup-cursor
# Add the provided JSON to Cursor settings.json and restart

# 3. Create project context
make new-context
# Provide project name and code repository path

# 4. Index your code
pip install -r rag/indexer/requirements.txt
make index
```

**What this creates:**
- `local/project-name/` - Agent-managed project context (gitignored)
- Vector index of your code and documentation
- MCP connection between Cursor and knowledge base

## Using Hish

**Development Agent:**
```
@prompts/dev_agent/dev_agent_init_prompt.md
```

**QA Agent:**
```
@prompts/qa/qa_agent_init_prompt.md
```

**Red Team Agent:**
```
@prompts/red_team/red_team_agent_init_prompt.md
```

This loads the appropriate agent with your project context and cross-project knowledge. From there, work naturally - agents automatically research patterns, propose solutions, and store learnings.

**Key files (agent-managed):**
- Agent contexts in `local/` - Don't edit manually
- See [Agent Management](../agent-management/) for interaction patterns

## Troubleshooting

**Common issues:**
- Docker not running → Start Docker service
- Port conflicts → Check ports 6333 are available
- MCP connection issues → Verify Cursor settings.json configuration
- Python issues → Use virtual environments (see [Virtual Environment Guide](virtual-environment-guide.md))

**MCP-specific issues:**
- "No such file or directory" → Check that the path in Cursor settings.json is correct
- "Connection refused" → Verify Cursor MCP connection is active, check port 6333 accessibility
- "No collections found" → Index content first with `make index`

**Debug commands:**
- `make health` - Check framework status
- `make collections` - List indexed collections
- `make logs` - View framework logs

**Documentation:** [Agent management](../agent-management/), [Technical architecture](../integration/)

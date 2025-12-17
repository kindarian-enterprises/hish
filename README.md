# Hish

Cursor is a powerful AI-assisted development tool that brings LLM capabilities directly into your editor. But when using third-party models, each session begins anew—fresh context, clean slate. Unlike human developers who accumulate institutional knowledge, learn from past decisions, and build on previous work, raw agents lack the ability to persist learnings across sessions or discover patterns across projects.

**Hish provides that missing layer.**

It indexes your documentation into searchable knowledge that agents query automatically. When implementing authentication in Project B, the agent discovers your JWT patterns from Project A. Database designs become institutional knowledge instead of lost conversation history. Architectural decisions persist and compound across work instead of requiring re-explanation each session.

The implementation is straightforward: vector search for semantic queries, MCP protocol for tool integration, structured prompts for behavioral discipline. Your documentation becomes agent memory. Your patterns become discoverable context. Your solutions inform future work without manual intervention.

Compatible with Claude, GPT-4, and Gemini. Integrates with Cursor's native code search. Runs locally with no external dependencies.

## How It Works

**Indexing:**
- Scans markdown files in your repositories
- Chunks content with overlap for context preservation
- Creates vector embeddings using MPNet model
- Stores in Qdrant vector database

**What gets indexed:**
- Markdown documentation
- README files
- Design decisions
- Project contexts

**What doesn't get indexed:**
- Source code (use Cursor's `codebase_search`)
- Binary files
- Generated files

**Agent Prompts:**
- Structured initialization prompts load project context
- Agents query indexed docs via `qdrant-find` MCP tool
- Agents store learnings via `qdrant-store` MCP tool
- Session end prompts capture knowledge for reuse

**Architecture:**
```
Markdown Docs → Python Indexer → Qdrant Vector DB
                                       ↓
                                   MCP Server
                                       ↓
                    Cursor ← Agent Prompts → Your Code
```

## Agent Personas

**Development Agent** (`/dev`)
- Pattern-driven implementation
- Queries docs for existing solutions
- Stores learnings for reuse
- Uses `qdrant-find` for docs, `codebase_search` for code

**Red Team Agent** (`/red`)
- Security analysis
- Vulnerability assessment
- Threat modeling
- Security pattern extraction

---

## Prerequisites

### **Required Software**
- **Docker**: Version 20.10+ with Docker Compose v2
  ```bash
  # Verify installation
  docker --version
  docker compose version
  ```
- **Git**: Version 2.20+
  ```bash
  git --version
  ```
- **Make**: GNU Make 3.81+
  ```bash
  make --version
  ```

### Python Environment
- **Python 3.8+** (3.12+ recommended)
- **Virtual environment required**

```bash
# Create venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r rag/indexer/requirements.txt
```

### **Network Requirements**
- **Internet Access**: Required for Docker image pulls and dependencies
- **Ports**: 6333 (Qdrant), 8000+ (MCP server)
- **Firewall**: Ensure Docker can bind to required ports

### **Troubleshooting Common Issues**
- **Docker Permission Errors**: Add user to docker group or use `sudo`
- **Port Conflicts**: Check if ports 6333, 8000+ are available
- **Python Version Issues**: Use pyenv or virtual environments for isolation



## Setup

```bash
# 1. Clone
git clone https://github.com/kindarian-enterprises/hish.git
cd hish

# 2. Setup Cursor integration
make setup-cursor
# Builds MCP server, installs custom commands
# Follow prompts to add config to Cursor settings.json
# Restart Cursor

# 3. Create project context
make new-context
# Interactive: provide project name and repo path
# Creates local/project-name/ (gitignored)

# 4. Index documentation
pip install -r rag/indexer/requirements.txt
make index

# 5. Use in Cursor
# Type /dev in chat to initialize agent
```

**What this creates:**
- MCP server connection to Qdrant
- Custom `/dev`, `/red`, `/end-dev`, `/end-red` commands
- Vector index of your documentation
- Project context in `local/` (gitignored)

## Usage

**Start session:**
```
Type /dev in Cursor chat
```

**Work normally:**
```
You: "Implement JWT auth for this API"

Agent:
- Queries indexed docs for auth patterns
- Finds existing JWT implementations
- Proposes solution based on your patterns
- Implements using Cursor's code tools
```

**End session:**
```
Type /end-dev in Cursor chat
```

**Commands available:**
- `/dev` - Initialize development agent
- `/red` - Initialize red team agent
- `/end-dev` - Close dev session
- `/end-red` - Close red team session
- `/verbalized-sampling` - Creative brainstorming mode

## Documentation

- [Getting Started](docs/setup/getting-started.md) - Complete setup guide
- [Directing Agents](docs/agent-management/directing-agents.md) - How to work with agents
- [Collection Governance](docs/collection-governance.md) - Managing indexed knowledge
- [Custom Commands](. cursor/commands/README.md) - Slash command reference

**Note:** `local/` is for customizations (gitignored). Editing core behavioral files may break framework. Framework changes need PRs.

# Framework Command Index

## 🚨 MANDATORY SESSION BEHAVIOR 🚨
**⚠️ CRITICAL: ALL framework operations MUST reference this index first ⚠️**
**🔒 ENFORCEMENT: Never improvise commands - use documented patterns only**
**📋 REQUIRED: Read this file during session initialization for all framework tasks**

## Setup and Configuration Commands

### Initial Framework Setup
```bash
# 1. Quick setup guide (shows steps, no auto-start)
make quick-start

# 2. Configure Cursor MCP integration
make setup-cursor

# 3. Create new project context (simplified - name + repo path only)
make new-context

# 4. Index everything (framework + all projects)
make index
```

### Context Management
```bash
# Create new project context
make new-context

# List all project contexts
make list-contexts

# Reindex specific contexts (positional args)
./reindex context1 context2 context3

# Reindex all contexts
./reindex all
```

### Knowledge Management
```bash
# Index everything (framework docs + all project repos) - host-based
make index

# Index framework documentation only (quick updates)
make index-framework

# Setup cross-project intelligence collection
make setup-intelligence

# Index specific repository - host-based
make index-repo REPO_PATH=/path/to/repo COLLECTION_NAME=repo_name_docs_mpnet

# Reindex specific contexts
make reindex-contexts CONTEXTS="context1 context2"
```

### Cross-Project Intelligence Storage
```bash
# Generate UUID for intelligence collection storage
python3 -c "import uuid; print(uuid.uuid4())"

# Store cross-project observations (requires UUID)
qdrant-store "Pattern observation with evidence..." cross_project_intelligence [UUID]

# Search intelligence collection
qdrant-find "query about patterns" cross_project_intelligence
```

### Framework Operations
```bash
# Start services manually (usually not needed - Cursor handles this)
make up

# Stop services
make down

# Check health
make health

# View status
make status

# View logs
make logs

# Clean up
make clean
```

### Development and Debugging
```bash
# Start MCP server for testing
make mcp

# View collections in Qdrant
make collections

# Search knowledge base (after MCP setup)
# In Cursor: qdrant-find "search query"

# Backup knowledge base
make backup
```

## Environment Files Reference

### Core Environment Files
- **`env.framework`** - Framework documentation indexing (docs/, local/, README.md files)
- **`env.code`** - External code repository indexing (comprehensive patterns)
- **`env.mcp`** - MCP server configuration (Qdrant connection, vector naming)

### Environment Variable Patterns
```bash
# Framework patterns (env.framework)
INDEX_INCLUDE=prompts/dev_agent/dev_agent_init_prompt.md,local/dev_agent_persona.md,prompts/dev_agent/dev_agent_session_end_prompt.md,prompts/qa/qa_agent_init_prompt.md,prompts/qa/qa_agent_session_end_prompt.md,prompts/red_team/red_team_agent_init_prompt.md,prompts/red_team/red_team_agent_session_end_prompt.md,README.md,local/*/dev_agent_context.md,local/*/README.md

# Code patterns (env.code)
INDEX_INCLUDE=**/*.py,**/*.yaml,**/*.yml,**/*.json,**/*.md,**/*.js,**/*.ts,**/*.tf,**/*.go,**/*.rs,**/*.scala,**/*.java,**/*.c,**/*.cpp,**/*.cc,**/*.cxx,**/*.h,**/*.hpp

# Common excludes
INDEX_EXCLUDE=**/.git/**,**/.data/**,**/node_modules/**,**/.terraform/**,**/.venv/**,**/dist/**,**/build/**,**/__pycache__/**,**/venv/**,**/.pytest_cache/**
```

## Collection Naming Patterns

### Standard Collection Names
- **`hish_framework_mpnet`** - Framework documentation and context files
- **`{project-name}_docs_mpnet`** - Project documentation (e.g., `mayr_docs_mpnet`)

### Vector Configuration
- **Model**: `BAAI/bge-small-en-v1.5`
- **Vector Name**: Same as model name (for LlamaIndex compatibility)
- **Dimension**: 384
- **Distance**: COSINE

## File Path References

### Key Framework Files
- **`prompts/dev_agent/dev_agent_init_prompt.md`** - Universal agent initialization
- **`local/dev_agent_persona.md`** - Universal agent persona
- **`prompts/dev_agent/dev_agent_session_end_prompt.md`** - Universal session end protocol
- **`prompts/qa/qa_agent_init_prompt.md`** - QA agent initialization
- **`prompts/qa/qa_agent_session_end_prompt.md`** - QA agent session end protocol
- **`templates/qa_agent_todo_checklist.md`** - QA agent systematic analysis checklist
- **`prompts/red_team/red_team_agent_init_prompt.md`** - Red team agent initialization
- **`prompts/red_team/red_team_agent_session_end_prompt.md`** - Red team agent session end protocol
- **`Makefile`** - All framework commands
- **`compose.rag.yml`** - Docker services configuration
- **`rag/indexer/app.py`** - Core indexing logic

### Directory Structure
- **`local/`** - Gitignored local contexts and workflows
- **`local/{project-name}/`** - Project-specific contexts
- **`local/workflow-indexes/`** - Internal workflow indexes (this system)
- **`local/workflows-and-processes/`** - Agent-managed workflows
- **`docs/`** - Framework documentation
- **`scripts/`** - Helper scripts
- **`templates/`** - Project templates

## Troubleshooting Command Patterns

### Common Issues
```bash
# Docker/Qdrant issues
docker compose -f compose.rag.yml logs qdrant
make down && make up

# MCP connection issues
make setup-cursor  # Get fresh config
# Restart Cursor after updating settings.json

# Collection issues
make collections  # List current collections
make clean && make index  # Full rebuild

# Permission issues
ls -la local/  # Check local directory permissions
```

## Account/Service References

### Docker Services
- **Qdrant**: Vector database (port 6333)
- **Indexer**: Python-based repository indexer
- **MCP Server**: LlamaIndex-compatible Qdrant MCP server

### MCP Configuration
- **Server Type**: stdio
- **Command**: `scripts/run-mcp-llamaindex.sh`
- **Environment**: Uses `env.mcp` configuration

# Hish Framework Repository Index

## 🚨 MANDATORY SESSION BEHAVIOR 🚨
**⚠️ CRITICAL: Use semantic search on these files instead of loading full content ⚠️**
**🔒 ENFORCEMENT: Reference this index to find the right component, then search specific sections**
**📋 REQUIRED: Never load entire large files - use targeted retrieval only**

## Repository Overview

**Hish** is a multi-project development agent framework that transforms engineering ecosystems into knowledge-powered learning machines through RAG-enhanced development workflows.

### Core Concepts
- **Multi-Project Intelligence**: One framework manages contexts for all projects
- **Shared Knowledge Base**: Patterns discovered in one project benefit ALL projects
- **Cross-Project Learning**: Agents learn from entire codebase ecosystem
- **Institutional Memory**: Persistent learning across teams, projects, and time

### Architecture Pattern
- **RAG System**: Qdrant vector database + LlamaIndex MCP server
- **Context Management**: Local gitignored contexts + universal persona
- **Knowledge Discovery**: Semantic search across framework + project collections
- **Workflow Recording**: Agent-managed process documentation

## Directory Structure → Purpose → Key Components

### Core Framework (`/`)
- **`Makefile`** - All framework commands and operations
  - Key Sections: Context management, knowledge indexing, setup workflows
  - Search Patterns: "index", "context", "setup", "mcp"
- **`dev_agent_persona.md`** - Universal AI agent persona for all projects
  - Key Sections: Multi-collection search protocol, quality standards
  - Search Patterns: "persona", "collection", "search"
- **`dev_agent_init_prompt.md`** - Universal initialization protocol
- **`dev_agent_session_end_prompt.md`** - Universal session end protocol

### RAG System (`rag/`)
- **`rag/indexer/app.py`** - Core indexing and embedding logic
  - Key Sections: Collection management, file processing, chunking
  - Search Patterns: "embed", "chunk", "collection", "qdrant"
- **`compose.rag.yml`** - Docker services configuration
  - Key Sections: Qdrant, indexer, MCP server definitions
  - Search Patterns: "service", "qdrant", "mcp"

### Documentation (`docs/`)
- **`docs/setup/`** - Setup and configuration guides
  - **`getting-started.md`** - 5-minute setup workflow
  - **`cursor-mcp-integration.md`** - Technical MCP integration
- **`docs/examples/`** - Usage examples and workflows
- **`docs/agent-management/`** - Agent direction and management

### Scripts and Utilities (`scripts/`)
- **`scripts/new-project-context.sh`** - Interactive context creation
  - Key Sections: User input, directory setup, README generation
  - Search Patterns: "context", "project", "template"
- **`scripts/run-mcp-llamaindex.sh`** - MCP server startup script
- **`reindex`** - User-friendly context reindexing script
  - Key Sections: Positional argument handling, context validation
  - Search Patterns: "reindex", "context", "validation"

### Configuration Files
- **`env.framework`** - Framework documentation indexing patterns
- **`env.code`** - External code repository indexing patterns
- **`env.mcp`** - MCP server configuration
- **`.gitignore`** - Ensures local/ directory is gitignored for user customization

### Templates (`templates/`)
- **`templates/context/`** - Project context templates
  - **`dev_agent_context_template.md`** - Standard project context structure

## Local Directory Structure (`local/`) - Gitignored

### Project Contexts (`local/{project-name}/`)
- **Purpose**: Individual project-specific contexts
- **Key Files**:
  - `dev_agent_context.md` - Project state and history tracking
  - `README.md` - Project documentation and usage
  - `repo_path.txt` - Path to actual code repository
- **Search Patterns**: Project name, "context", "state"

### Workflow Management (`local/workflows-and-processes/`)
- **Purpose**: Agent-managed workflow documentation
- **Key Sections**: Workflow lifecycle, recording protocols
- **Search Patterns**: "workflow", "process", "agent"

### Internal Indexes (`local/workflow-indexes/`)
- **Purpose**: Framework navigation and enforcement system
- **Key Files**:
  - `framework-command-index.md` - All framework commands
  - `framework-file-index.md` - File-to-purpose mapping
  - `session-workflow-enforcement.md` - Behavioral enforcement rules
- **Search Patterns**: "command", "index", "enforcement"

## Knowledge Collections

### Framework Documentation (`framework_docs`)
- **Content**: Framework files, project contexts, documentation
- **Include Patterns**: `dev_agent_*.md`, `README.md`, `local/*/dev_agent_context.md`
- **Search Strategy**: Start here for architectural context

### Project Code Collections (`{project-name}_code`)
- **Content**: External project repositories
- **Include Patterns**: Comprehensive code file patterns
- **Search Strategy**: Use for project-specific implementation details

## Environment Configuration Reference

### Framework Indexing (`env.framework`)
```bash
COLLECTION_NAME=framework_docs
INDEX_INCLUDE=dev_agent_init_prompt.md,dev_agent_persona.md,dev_agent_session_end_prompt.md,README.md,local/*/dev_agent_context.md,local/*/README.md
```

### Code Repository Indexing (`env.code`)
```bash
COLLECTION_NAME=external_code
INDEX_INCLUDE=**/*.py,**/*.yaml,**/*.yml,**/*.json,**/*.md,**/*.js,**/*.ts,**/*.tf,**/*.go,**/*.rs,**/*.scala,**/*.java,**/*.c,**/*.cpp,**/*.cc,**/*.cxx,**/*.h,**/*.hpp
INDEX_EXCLUDE=**/.git/**,**/.data/**,**/node_modules/**,**/.terraform/**,**/.venv/**,**/dist/**,**/build/**,**/__pycache__/**,**/venv/**,**/.pytest_cache/**
```

### MCP Server Configuration (`env.mcp`)
```bash
QDRANT_URL=http://qdrant:6333
VECTOR_NAME=BAAI/bge-small-en-v1.5
```

## Workflow Patterns

### Setup Workflow
1. `make quick-start` - Shows configuration steps
2. `make setup-cursor` - Generate MCP configuration
3. `make new-context` - Create project context (name + repo path)
4. `make index` - Index framework + all project repositories

### Development Workflow
1. `@dev_agent_init_prompt.md` - Initialize agent with universal persona
2. Agent loads project-specific context automatically
3. Use `qdrant-find` for cross-project knowledge discovery
4. Agent records workflows in `workflows-and-processes/`

### Maintenance Workflow
1. `./reindex project1 project2` - Selective reindexing
2. `make clean && make index` - Full rebuild if needed
3. `make backup` - Knowledge base backup

## File Size and Search Strategy

### Always Use Semantic Search (Large Files)
- `dev_agent_persona.md` (545 lines)
- `README.md` (421 lines)
- `rag/indexer/app.py` (267 lines)
- Large documentation files

### Targeted Search Recommended (Medium Files)
- `Makefile` (236 lines) - Search by specific command/section
- `scripts/new-project-context.sh` (289 lines) - Search by function
- Documentation in `docs/` directory

### Safe to Read Fully (Small Files)
- Environment files (`env.*`)
- Configuration files
- Templates
- Init prompts

## Integration Points

### Cursor Integration
- **MCP Protocol**: stdio-based communication
- **Configuration**: JSON in Cursor settings.json
- **Commands**: `qdrant-find`, `qdrant-store` available in Cursor

### Docker Integration
- **Services**: Qdrant (vector DB), Indexer (Python), MCP Server
- **Data Persistence**: `.data/qdrant/` for vector storage
- **Network**: Internal Docker network for service communication

### Git Integration
- **Framework**: Tracked in git for updates and collaboration
- **Local Contexts**: Gitignored for user-specific customization
- **Workflows**: Agent-managed, automatically indexed

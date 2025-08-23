# Framework File Reference Index

## 🚨 MANDATORY SESSION BEHAVIOR 🚨
**⚠️ CRITICAL: Use semantic search on these files instead of loading full content ⚠️**
**🔒 ENFORCEMENT: Reference this index to find the right file, then search specific sections**
**📋 REQUIRED: Never load entire files - use targeted retrieval only**

## File → Purpose → Key Sections

### Core Framework Files

#### `Makefile` (236 lines)
- **Purpose**: All framework commands and operations
- **Key Sections**:
  - Lines 61-83: Knowledge Management (`index`, `reindex-contexts`)
  - Lines 117-135: Repository indexing (`index-repo`)
  - Lines 141-152: Quick start and setup
  - Lines 42-58: Context management (`new-context`, `list-contexts`)
- **Search Patterns**: "index", "context", "setup", "mcp"

#### `dev_agent_persona.md` (545 lines) 
- **Purpose**: Universal AI agent persona and behavior guidelines
- **Key Sections**:
  - Lines 1-50: Core persona definition
  - Lines 200-250: Multi-collection search protocol  
  - Lines 300-400: Knowledge management strategies
  - Lines 450-545: Quality standards and enforcement
- **Search Patterns**: "collection", "search", "qdrant-find", "persona"

#### `dev_agent_init_prompt.md`
- **Purpose**: Universal agent initialization protocol
- **Key Sections**: Complete file is essential initialization content
- **Search Patterns**: "init", "context", "project"

### Configuration Files

#### `compose.rag.yml` (83 lines)
- **Purpose**: Docker services configuration for RAG system
- **Key Sections**:
  - Lines 1-25: Qdrant vector database service
  - Lines 26-50: Indexer service configuration
  - Lines 51-83: MCP server configuration
- **Search Patterns**: "qdrant", "indexer", "mcp", "service"

#### `env.framework` (22 lines)
- **Purpose**: Environment configuration for framework documentation indexing
- **Key Sections**:
  - Lines 11-13: Include/exclude patterns for framework files
  - Lines 7-8: Collection and model configuration
- **Search Patterns**: "INDEX_INCLUDE", "framework", "docs"

#### `env.code` (22 lines)
- **Purpose**: Environment configuration for external code repository indexing  
- **Key Sections**:
  - Lines 12-13: Comprehensive file patterns for code repositories
  - Lines 16-18: Chunking configuration
- **Search Patterns**: "INDEX_INCLUDE", "code", "patterns"

#### `env.mcp` (13 lines)
- **Purpose**: MCP server environment configuration
- **Key Sections**:
  - Lines 2-4: Qdrant connection settings
  - Lines 7-8: Vector naming for LlamaIndex compatibility
- **Search Patterns**: "QDRANT_URL", "VECTOR_NAME", "mcp"

### Core Logic Files

#### `rag/indexer/app.py` (267 lines)
- **Purpose**: Core repository indexing and vector embedding logic
- **Key Sections**:
  - Lines 27-52: Collection management and vector configuration
  - Lines 55-92: Embedding model loading and configuration  
  - Lines 180-320: File processing and chunking logic
  - Lines 199-280: Main indexing workflow
- **Search Patterns**: "collection", "embed", "chunk", "qdrant"

#### `scripts/new-project-context.sh` (289 lines)
- **Purpose**: Interactive project context creation
- **Key Sections**:
  - Lines 106-115: User input collection (simplified)
  - Lines 129-140: Context directory setup
  - Lines 192-255: README template generation  
  - Lines 259-268: Optional indexing workflow
- **Search Patterns**: "context", "project", "template"

### Documentation Files

#### `README.md` (421 lines)
- **Purpose**: Main framework documentation and quick start
- **Key Sections**:
  - Lines 105-170: Quick start workflow (5 steps)
  - Lines 200-300: Architecture and concepts
  - Lines 350-421: Advanced usage and troubleshooting
- **Search Patterns**: "quick start", "setup", "workflow"

#### `docs/setup/getting-started.md` (119 lines)
- **Purpose**: Detailed setup guide for new users
- **Key Sections**:
  - Lines 20-70: 5-minute setup workflow
  - Lines 80-95: How the framework works
  - Lines 95-119: Troubleshooting
- **Search Patterns**: "setup", "mcp", "cursor"

#### `docs/setup/cursor-mcp-integration.md`
- **Purpose**: Technical MCP integration details
- **Key Sections**: MCP server configuration and JSON settings
- **Search Patterns**: "mcp", "cursor", "settings", "json"

### Template and Context Files  

#### `templates/context/dev_agent_context_template.md`
- **Purpose**: Template for new project contexts
- **Key Sections**: Project state tracking structure
- **Search Patterns**: "context", "template", "project"

#### `local/{project-name}/dev_agent_context.md`
- **Purpose**: Project-specific context and state
- **Key Sections**: Varies by project
- **Search Patterns**: "context", project name

#### `local/{project-name}/README.md`
- **Purpose**: Project-specific documentation and setup
- **Key Sections**: Project info and usage instructions
- **Search Patterns**: "project", "usage", "setup"

### Workflow Management Files

#### `local/workflows-and-processes/README.md`
- **Purpose**: Agent-managed workflow documentation system
- **Key Sections**: Workflow lifecycle and management rules
- **Search Patterns**: "workflow", "process", "agent"

#### `local/workflow-indexes/` (this directory)
- **Purpose**: Internal framework navigation indexes
- **Key Sections**: Command references, file mappings, enforcement rules
- **Search Patterns**: "index", "command", "workflow"

## File Size Guidelines

### Small Files (< 100 lines) - Safe to Read Fully
- Environment files (`env.*`)
- Init prompts
- Simple templates

### Medium Files (100-300 lines) - Use Targeted Search  
- Scripts
- Configuration files
- Specific documentation

### Large Files (300+ lines) - Always Use Semantic Search
- `dev_agent_persona.md`
- `README.md` 
- Large documentation files

## Search Strategy Patterns

### For Commands
1. Check `framework-command-index.md` first
2. If not found, search `Makefile` with specific command name
3. Cross-reference with scripts in `scripts/` directory

### For Configuration
1. Identify the right environment file (`env.framework`, `env.code`, `env.mcp`)
2. Search specific sections rather than reading entire file
3. Cross-reference with `compose.rag.yml` for service config

### For Concepts/Architecture
1. Start with `README.md` overview sections
2. Drill down to specific docs in `docs/` directory
3. Reference `dev_agent_persona.md` for behavioral guidelines

# Hish Framework Changelog

This file tracks major changes, migrations, and required user actions for the Hish framework.

## Version 2025.09.09.1707 - MCP Server Pre-warming & Optimization Complete

**Date:** September 9, 2025 17:07 UTC
**Migration Required:** No
**Breaking Changes:** None

### Changes

- **Pre-warmed MCP Server**: Enhanced Dockerfile to pre-download MPNet model during image build using correct `fastembed` library
- **Faster Startup**: MCP server now starts instantly without model download delay (tested and verified)
- **Optimized Docker Layers**: Single-layer Dockerfile build for maximum efficiency and smaller image size
- **Proper Image Tagging**: Added `hish-mcp-unified:latest` tag for reliable runtime discovery
- **Build Integration**: `make setup-cursor` now builds optimized MCP server image automatically
- **New Command**: Added `make build-mcp` for standalone MCP server image building
- **Makefile Enhancement**: Updated help documentation and command organization

### Technical Details

- **Library Fix**: Switched from `sentence-transformers` to `fastembed` for model pre-warming (matches MCP server runtime)
- **Layer Optimization**: Combined all RUN commands into single layer since no user code changes
- **Consistent Tooling**: Used `uv` throughout Dockerfile for package management consistency

### Benefits

- **Instant MCP Server Startup**: No more waiting for model download on first use
- **Better Developer Experience**: Cursor integration setup now includes pre-built optimized server
- **Reliability**: Pre-warmed model eliminates network dependency during MCP server startup
- **Smaller Images**: Optimized layer structure reduces image size and build complexity

## Version 2025.09.09.1321 - MPNet Unification & Makefile Implementation

**Date:** September 9, 2025 13:21 UTC
**Migration Required:** Yes
**Breaking Changes:** Collection naming, embedding models, Makefile commands

### Changes

- **Unified Embedding Model**: Switched from dual embedding architecture (BGE + Jina Code) to unified `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
- **Collection Naming**: All collections now include model suffix (e.g., `hish_framework_mpnet`, `{project}_docs_mpnet`)
- **Single MCP Server**: Simplified from dual MCP servers back to single unified server
- **Makefile Implementation**: Updated all indexing commands to use unified MPNet embeddings
- **Improved Search**: Better granular text understanding while maintaining code comprehension

### Migration Required

#### 1. Vector Collection Migration
Existing collections need to be migrated to new MPNet-based collections:

```bash
# Reindex everything with unified MPNet embeddings
make index
```

#### 2. Cursor MCP Configuration Update
Update your Cursor settings.json to use the new unified server:

```json
{
  "mcpServers": {
    "qdrant-unified": {
      "type": "stdio",
      "command": "/Users/your-username/Documents/Projects/hish/scripts/run-mcp-unified.sh",
      "workingDirectory": "/Users/your-username/Documents/Projects/hish",
      "env": {
        "NO_COLOR": "1"
      }
    }
  }
}
```

#### 3. Environment Files
New environment configuration files:
- `config/env.mpnet` - For all indexing operations (unified)

### Benefits

- **Consistent Search Quality**: Same embedding model for both docs and code
- **Simplified Architecture**: Single configuration and MCP server
- **Better Keyword Matching**: MPNet provides improved literal text search
- **Multi-language Support**: Enhanced support for mixed-language codebases
- **Unified Collection Naming**: Clear `_mpnet` suffix for all collections

---

## Template for Future Entries

```markdown
## Version YYYY.MM - Feature Name

**Date:** Month Year
**Migration Required:** Yes/No
**Breaking Changes:** Description of breaking changes

### Changes

- Major change 1
- Major change 2

### Migration Required (if applicable)

#### 1. Step Name
Description and commands

#### 2. Step Name
Description and commands

### Benefits

- Benefit 1
- Benefit 2

### Rollback Instructions (if applicable)

Commands or steps to rollback
```

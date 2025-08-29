# Technical Architecture Overview

## Purpose

This document explains the technical decisions behind Hish's RAG + MCP architecture.

**For setup instructions, use the [Getting Started Guide](../setup/getting-started.md) - `make quick-setup` handles all configuration automatically.**

This document is for developers who want to understand why we chose specific technologies and how they work together.

## Architecture Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cursor IDE    │    │ LlamaIndex MCP  │    │   Qdrant DB    │
│                 │────│     Server      │────│                 │
│ - Dev Agent     │    │ - qdrant-find   │    │ - Named Vectors │
│ - Chat Context  │    │ - qdrant-store  │    │ - BGE Embeddings│
│ - Files/Code    │    │ - BGE Model     │    │ - Collections   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Technology Decisions

### Qdrant Vector Database

**Chosen over**: Pinecone, Weaviate, Chroma, FAISS

**Reasons**:
- **Self-hosted**: No API costs or rate limits for development
- **Named vectors**: MCP protocol requires collection naming, Qdrant supports this natively
- **Docker native**: Simple deployment in development environments
- **Rust performance**: Fast similarity search with reasonable memory usage
- **Open source**: No vendor lock-in concerns

**Trade-offs**: More setup complexity than managed services, but acceptable since `make quick-setup` automates this.

### BGE Embeddings (BAAI/bge-small-en-v1.5)

**Chosen over**: OpenAI embeddings, Sentence Transformers, other BGE models

**Reasons**:
- **No API dependency**: Works offline, no rate limits or costs
- **Code-optimized**: BGE models perform well on code and technical documentation
- **Size vs. quality**: 384 dimensions balance quality with storage/memory requirements
- **Proven performance**: Consistent results across different content types

**Trade-offs**: Slightly lower quality than larger models, but sufficient for code search use cases.

### Model Context Protocol (MCP)

**Chosen over**: Direct API integration, RAG frameworks, custom solutions

**Reasons**:
- **Cursor native**: Direct integration with Cursor IDE without additional configuration
- **Standardized**: Protocol standard emerging across AI development tools
- **Tool-based**: Clean separation between LLM and knowledge base operations
- **Simple interface**: `qdrant-find` and `qdrant-store` commands are intuitive

**Trade-offs**: Newer protocol with less ecosystem maturity, but good enough for our use case.

## Prerequisites

### System Requirements
- Docker and Docker Compose v2 installed
- Python 3.8+ available
- Git for repository management
- Sufficient RAM for Docker containers (varies by codebase size)
- Disk space for vector indices (scales with indexed content)

### **Project Requirements**
- A codebase or documentation repository to index
- Cursor IDE with MCP support enabled

## 🔧 **Technical Details**

### **Environment Configuration**
The framework uses three environment files:

- **`env.mcp`**: MCP server configuration
- **`env.framework`**: Framework documentation indexing
- **`env.code`**: External code repository indexing

### **Current MCP Server Configuration**
```bash
# env.mcp content
QDRANT_URL=http://qdrant:6333
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
VECTOR_NAME=BAAI/bge-small-en-v1.5
```

### **BGE Model Configuration**
```bash
# env.code content (for external repositories)
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
CHUNK_MAX_TOKENS=350
CHUNK_MIN_CHARS=150
CHUNK_OVERLAP_TOKENS=70
```

### **Vector Database Setup**
- **Database**: Qdrant vector database
- **Collections**: Named vector collections for MCP compatibility
- **Embeddings**: 384-dimensional vectors from BGE-small model
- **Distance**: Cosine similarity for semantic matching

## Docker Services

### Service Architecture
```yaml
# compose.rag.yml structure
services:
  qdrant:                    # Vector database
  mcp-qdrant-llamaindex:     # MCP server
```

**Note**: Indexing runs on the host system (not containerized) for better performance.

### Network Configuration
- **Qdrant**: Port 6333 (HTTP API)
- **MCP Server**: STDIO communication with Cursor
- **Indexing**: Host-based Python scripts

## Indexing Process

### Framework Documentation
```bash
# Index framework and all project repositories
make index

# Framework-only reindexing for quick updates
make index-framework
```

### External Code Repositories
```bash
# Index specific code repository
make index-repo REPO_PATH=/path/to/code COLLECTION_NAME=project_code
```

### **Chunking Strategy**
- **Maximum Tokens**: 350 per chunk
- **Minimum Characters**: 150 per chunk
- **Overlap**: 70 tokens between chunks
- **Context Headers**: `[repo: name] [file: path] [ext: type] [title: filename]`

## 🔌 **MCP Integration**

### **Cursor Configuration**
```json
{
  "mcpServers": {
    "qdrant": {
      "type": "stdio",
      "command": "/absolute/path/to/hish/scripts/run-mcp-llamaindex.sh",
      "workingDirectory": "/absolute/path/to/hish",
      "env": {
        "NO_COLOR": "1"
      }
    }
  }
}
```

### **Available Tools**
- **`qdrant-find`**: Semantic search across all collections
- **`qdrant-store`**: Store new knowledge and solutions
- **`qdrant-get-collections`**: List available collections
- **`qdrant-get-collection-details`**: Collection information

## 📊 **Collection Strategy**

### **Collection Naming**
- **Framework**: `framework_docs`
- **Code Repositories**: `{project_name}_code`
- **Separation**: Each project gets its own collection

### **Vector Configuration**
```python
# Named vector setup for MCP compatibility
vectors_config = {
    "BAAI/bge-small-en-v1.5": VectorParams(
        size=384, 
        distance=Distance.COSINE
    )
}
```

## 🛠️ **Advanced Configuration**

### **Custom Embedding Models**
To use a different embedding model:

1. Update `EMBEDDING_MODEL` in environment files
2. Update `VECTOR_NAME` in `env.mcp`
3. Recreate collections with `--recreate` flag
4. Reindex all content

### **Performance Tuning**
```bash
# Optimize collections for better search quality
make optimize-collections

# Parallel indexing (faster for large codebases)
MAX_WORKERS=8 make index
```

### **Custom Chunking**
```bash
# Adjust chunking parameters in env.code
CHUNK_MAX_TOKENS=500        # Larger chunks
CHUNK_MIN_CHARS=100         # Smaller minimum
CHUNK_OVERLAP_TOKENS=100    # More overlap
```

## 🚨 **Troubleshooting**

### **Common Issues**

**"Vector dimension mismatch"**
- Collections created with different model
- Solution: Recreate collections with `--recreate`

**"No collections found"**
- No content indexed yet
- Solution: Run `make index`

**"MCP server not responding"**
- Docker services not running
- Solution: Check Cursor MCP connection status

**"Connection refused to Qdrant"**
- Qdrant service not accessible
- Solution: Verify port 6333 is available

### **Debug Commands**
```bash
# Check service health
# Verify MCP connection in Cursor

# View collections
make collections

# Check logs
make logs

# Test MCP server directly
make mcp
```

## 📈 **Monitoring & Maintenance**

### **Regular Tasks**
- **Reindex**: When code changes significantly
- **Optimize**: Run `make optimize-collections` monthly
- **Backup**: Use `make backup` for important knowledge

### **Performance Metrics**
- **Search Quality**: Relevance of results
- **Index Size**: Disk space usage
- **Query Speed**: Response time for searches

---

## 🎯 **Summary**

The current RAG+MCP setup provides:
- **Streamlined Setup**: Single command deployment
- **Superior Search**: BGE model semantic understanding
- **MCP Integration**: Direct Cursor access via tools
- **Scalable Architecture**: Multi-project knowledge sharing

For basic usage, stick to the [Getting Started Guide](../setup/getting-started.md). Use this guide when you need to customize or troubleshoot the technical implementation.
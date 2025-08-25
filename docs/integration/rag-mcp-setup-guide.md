# RAG + MCP Integration Setup Guide

## 🎯 **Overview**
This guide covers the technical details of RAG (Retrieval Augmented Generation) with MCP (Model Context Protocol) integration.

**⚠️ For basic setup, use the [Getting Started Guide](../setup/getting-started.md) instead.**

This guide is for advanced users who need to understand the technical architecture and customize the setup.

## 🏗️ **Current Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cursor IDE    │    │ LlamaIndex MCP  │    │   Qdrant DB    │
│                 │────│     Server      │────│                 │
│ - Dev Agent     │    │ - qdrant-find   │    │ - Named Vectors │
│ - Chat Context  │    │ - qdrant-store  │    │ - BGE Embeddings│
│ - Files/Code    │    │ - BGE Model     │    │ - Collections   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Key Components:**
- **Single MCP Server**: `qdrant-llamaindex-mcp-server` handles all operations
- **BGE Embeddings**: `BAAI/bge-small-en-v1.5` for superior semantic search
- **Named Vectors**: Collections use named vectors for MCP compatibility
- **Docker Orchestration**: All services managed via `compose.rag.yml`

## 📋 **Prerequisites**

### **System Requirements**
- Docker and Docker Compose v2 installed
- Python 3.8+ available
- Git for repository management
- At least 4GB RAM for Qdrant vector database
- ~10GB disk space for embeddings and indices

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

## 🚀 **Docker Services**

### **Service Architecture**
```yaml
# compose.rag.yml structure
services:
  qdrant:                    # Vector database
  indexer:                   # Code indexing service
  mcp-qdrant-llamaindex:     # MCP server
```

### **Network Configuration**
- **Qdrant**: Port 6333 (HTTP API)
- **MCP Server**: STDIO communication with Cursor
- **Internal Network**: Docker Compose networking

## 🔍 **Indexing Process**

### **Framework Documentation**
```bash
# Uses env.framework
make index
# Indexes: docs/, local/, README.md, persona files
```

### **External Code Repositories**
```bash
# Uses env.code
make index-repo REPO_PATH=/path/to/code COLLECTION_NAME=project_code
# Indexes: source code, documentation, configuration files
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
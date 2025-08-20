# RAG + MCP Integration Setup Guide

## 🎯 **Overview**
This guide walks you through setting up RAG (Retrieval Augmented Generation) with MCP (Model Context Protocol) to create a knowledge-powered development agent that can access and store information across your entire project ecosystem.

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cursor IDE    │    │   MCP Server    │    │   Qdrant DB    │
│                 │────│                 │────│                 │
│ - Dev Agent     │    │ - qdrant-find   │    │ - Vector Store  │
│ - Chat Context  │    │ - qdrant-store  │    │ - Collections   │
│ - Files/Code    │    │ - Indexing      │    │ - Embeddings    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 **Prerequisites**

### **System Requirements**
- Docker and Docker Compose installed
- Python 3.8+ available
- Git for repository management
- At least 4GB RAM for Qdrant vector database
- ~10GB disk space for embeddings and indices

### **Project Requirements**
- A codebase or documentation repository to index
- Development agent persona and context files (use templates provided)
- Cursor IDE with MCP support enabled

## 🚀 **Quick Start Setup**

### **Step 1: Clone and Initialize**
```bash
# Create your project directory
mkdir your-project-name
cd your-project-name

# Copy the kindarian-cursor-context templates
cp -r /path/to/kindarian-cursor-context/templates/* ./
cp -r /path/to/kindarian-cursor-context/workflows-and-processes ./
cp -r /path/to/kindarian-cursor-context/docs ./

# Initialize your persona and context
cp templates/persona/dev_agent_persona_template.md dev_agent_persona.md
cp templates/context/dev_agent_context_template.md dev_agent_context.md
cp templates/prompts/dev_agent_init_prompt_template.md dev_agent_init_prompt.md
cp templates/prompts/dev_agent_session_end_prompt_template.md dev_agent_session_end_prompt.md
```

### **Step 2: Customize Your Agent**
```bash
# Edit your persona (define your project's coding standards, tech stack, etc.)
vim dev_agent_persona.md

# Edit your context (define current project state, goals, etc.)
vim dev_agent_context.md

# Edit initialization prompt (customize for your project)
vim dev_agent_init_prompt.md
```

### **Step 3: Setup RAG Infrastructure**
```bash
# Create RAG setup directory
mkdir rag
cd rag

# Create docker-compose.yml for Qdrant
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3
EOF

# Start Qdrant
docker-compose up -d
```

## 🔧 **MCP Server Setup**

### **Create MCP Server Script**
```bash
# Create mcp directory
mkdir mcp
cd mcp

# Create the MCP server script
cat > mcp_server.py << 'EOF'
#!/usr/bin/env python3
"""
MCP Server for Qdrant RAG Integration
Provides qdrant-find and qdrant-store tools for knowledge management
"""

import asyncio
import logging
import os
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
)
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
model = SentenceTransformer(MODEL_NAME)

# Initialize server
server = Server("qdrant-mcp")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="qdrant-find",
            description="Search for information in the knowledge base using semantic similarity",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant information"
                    },
                    "collection": {
                        "type": "string", 
                        "description": "Optional collection name to search in",
                        "default": None
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="qdrant-store",
            description="Store information in the knowledge base for future retrieval",
            inputSchema={
                "type": "object",
                "properties": {
                    "information": {
                        "type": "string",
                        "description": "Information to store in the knowledge base"
                    },
                    "collection": {
                        "type": "string",
                        "description": "Collection name to store in",
                        "default": "knowledge_base"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata to associate with the information",
                        "default": {}
                    }
                },
                "required": ["information"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "qdrant-find":
            return await handle_find(arguments)
        elif name == "qdrant-store":
            return await handle_store(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error in {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True
        )

async def handle_find(args: Dict[str, Any]) -> CallToolResult:
    """Handle qdrant-find requests."""
    query = args["query"]
    collection = args.get("collection")
    limit = args.get("limit", 10)
    
    # Get query embedding
    query_vector = model.encode(query).tolist()
    
    # Search in Qdrant
    if collection:
        collections = [collection]
    else:
        # Search all collections
        collections_info = client.get_collections()
        collections = [c.name for c in collections_info.collections]
    
    results = []
    for coll in collections:
        try:
            search_results = client.search(
                collection_name=coll,
                query_vector=query_vector,
                limit=limit
            )
            
            for result in search_results:
                results.append({
                    "collection": coll,
                    "content": result.payload.get("content", ""),
                    "metadata": result.payload.get("metadata", {}),
                    "score": result.score
                })
        except Exception as e:
            logger.warning(f"Error searching collection {coll}: {e}")
    
    # Sort by score and limit
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:limit]
    
    # Format response
    response_text = f"Results for the query '{query}'\n"
    for i, result in enumerate(results, 1):
        response_text += f"\n{i}. [Collection: {result['collection']}] "
        response_text += f"(Score: {result['score']:.3f})\n"
        response_text += f"{result['content']}\n"
        if result['metadata']:
            response_text += f"Metadata: {result['metadata']}\n"
    
    return CallToolResult(
        content=[TextContent(type="text", text=response_text)]
    )

async def handle_store(args: Dict[str, Any]) -> CallToolResult:
    """Handle qdrant-store requests."""
    information = args["information"]
    collection = args.get("collection", "knowledge_base")
    metadata = args.get("metadata", {})
    
    # Create collection if it doesn't exist
    try:
        client.get_collection(collection)
    except:
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    
    # Generate embedding
    vector = model.encode(information).tolist()
    
    # Create point
    point = PointStruct(
        id=None,  # Auto-generate ID
        vector=vector,
        payload={
            "content": information,
            "metadata": metadata
        }
    )
    
    # Store in Qdrant
    client.upsert(collection_name=collection, points=[point])
    
    return CallToolResult(
        content=[TextContent(
            type="text", 
            text=f"Successfully stored information in collection '{collection}'"
        )]
    )

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
EOF

# Make it executable
chmod +x mcp_server.py
```

### **Install Dependencies**
```bash
# Create requirements file
cat > requirements.txt << 'EOF'
mcp>=0.1.0
qdrant-client>=1.7.0
sentence-transformers>=2.2.0
asyncio
logging
EOF

# Install dependencies
pip install -r requirements.txt
```

## 📚 **Knowledge Base Setup**

### **Create Indexing Script**
```bash
# Create indexing script
cat > index_codebase.py << 'EOF'
#!/usr/bin/env python3
"""
Index codebase and documentation for RAG retrieval
"""

import os
import argparse
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
import uuid

class CodebaseIndexer:
    def __init__(self, qdrant_host="localhost", qdrant_port=6333):
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def create_collection(self, collection_name: str):
        """Create a new collection if it doesn't exist."""
        try:
            self.client.get_collection(collection_name)
            print(f"Collection '{collection_name}' already exists")
        except:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"Created collection '{collection_name}'")
    
    def index_files(self, directory: str, collection_name: str, 
                   extensions: List[str] = None, max_chunk_size: int = 1000):
        """Index files in a directory."""
        if extensions is None:
            extensions = ['.py', '.md', '.txt', '.js', '.ts', '.go', '.rs', '.java']
        
        self.create_collection(collection_name)
        
        files_processed = 0
        chunks_created = 0
        
        for root, dirs, files in os.walk(directory):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv']]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Create chunks
                        chunks = self._create_chunks(content, max_chunk_size)
                        
                        # Index each chunk
                        for i, chunk in enumerate(chunks):
                            if chunk.strip():  # Skip empty chunks
                                self._index_chunk(
                                    chunk, 
                                    collection_name,
                                    {
                                        "file_path": file_path,
                                        "chunk_index": i,
                                        "total_chunks": len(chunks),
                                        "file_extension": Path(file_path).suffix
                                    }
                                )
                                chunks_created += 1
                        
                        files_processed += 1
                        if files_processed % 50 == 0:
                            print(f"Processed {files_processed} files, created {chunks_created} chunks")
                    
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        
        print(f"Indexing complete: {files_processed} files, {chunks_created} chunks")
    
    def _create_chunks(self, content: str, max_size: int) -> List[str]:
        """Create chunks from content."""
        if len(content) <= max_size:
            return [content]
        
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line) + 1  # +1 for newline
            
            if current_size + line_size > max_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def _index_chunk(self, chunk: str, collection_name: str, metadata: Dict[str, Any]):
        """Index a single chunk."""
        vector = self.model.encode(chunk).tolist()
        
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "content": chunk,
                "metadata": metadata
            }
        )
        
        self.client.upsert(collection_name=collection_name, points=[point])

def main():
    parser = argparse.ArgumentParser(description="Index codebase for RAG retrieval")
    parser.add_argument("directory", help="Directory to index")
    parser.add_argument("--collection", default="codebase", help="Collection name")
    parser.add_argument("--extensions", nargs="+", 
                       default=['.py', '.md', '.txt', '.js', '.ts'],
                       help="File extensions to index")
    parser.add_argument("--chunk-size", type=int, default=1000, 
                       help="Maximum chunk size")
    
    args = parser.parse_args()
    
    indexer = CodebaseIndexer()
    indexer.index_files(
        args.directory, 
        args.collection,
        args.extensions,
        args.chunk_size
    )

if __name__ == "__main__":
    main()
EOF

chmod +x index_codebase.py
```

## ⚙️ **Cursor Integration**

### **Configure Cursor MCP**
```json
// Add to your Cursor settings.json
{
  "mcp": {
    "servers": {
      "qdrant": {
        "command": "python",
        "args": ["/path/to/your/project/mcp/mcp_server.py"],
        "env": {
          "QDRANT_HOST": "localhost",
          "QDRANT_PORT": "6333",
          "EMBEDDING_MODEL": "all-MiniLM-L6-v2"
        }
      }
    }
  }
}
```

### **Test the Integration**
```bash
# Start Qdrant
cd rag && docker-compose up -d

# Index your codebase
cd mcp
python index_codebase.py /path/to/your/project --collection your_project_code

# Index your documentation
python index_codebase.py /path/to/your/docs --collection your_project_docs --extensions .md .txt

# Test the MCP server
python mcp_server.py
```

## 🔍 **Usage Examples**

### **In Cursor Chat**
```
# Search for implementation patterns
qdrant-find "authentication implementation examples"

# Search for specific error solutions
qdrant-find "database connection error handling"

# Search in specific collection
qdrant-find "testing patterns" --collection your_project_code

# Store new knowledge
qdrant-store "Solution: JWT refresh token implementation - Used rotating refresh tokens with Redis blacklist for security. Context: Web API authentication. Files: auth/jwt_handler.py, auth/middleware.py"
```

### **Development Workflow Integration**
```bash
# Before implementing a feature
qdrant-find "similar feature implementations"
qdrant-find "architectural patterns for this component type"

# When debugging
qdrant-find "similar error patterns and solutions"
qdrant-find "troubleshooting steps for this issue"

# After solving a problem
qdrant-store "Problem: [description] - Solution: [approach] - Context: [when applicable] - Files: [affected files]"
```

## 🚀 **Advanced Configuration**

### **Multiple Collections Setup**
```python
# Example collection strategy
collections = {
    "project_code": "Source code and implementation patterns",
    "project_docs": "Documentation and guides", 
    "project_tests": "Test patterns and examples",
    "project_config": "Configuration files and deployment",
    "external_libs": "Third-party library documentation",
    "team_knowledge": "Team-specific patterns and decisions"
}
```

### **Performance Optimization**
```yaml
# docker-compose.yml optimization
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__LOG_LEVEL=INFO
      - QDRANT__STORAGE__WAL_CAPACITY_MB=32
      - QDRANT__STORAGE__WAL_SEGMENTS_AHEAD=0
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

## 🛠️ **Troubleshooting**

### **Common Issues**

**Qdrant Connection Failed**
```bash
# Check if Qdrant is running
curl http://localhost:6333/health

# Check Docker logs
docker-compose logs qdrant
```

**MCP Server Not Responding**
```bash
# Test MCP server directly
python mcp_server.py

# Check dependencies
pip install -r requirements.txt
```

**Slow Indexing Performance**
```bash
# Reduce chunk size
python index_codebase.py /path --chunk-size 500

# Exclude large files
python index_codebase.py /path --extensions .py .md
```

**Poor Search Quality**
```bash
# Try different embedding models
export EMBEDDING_MODEL="all-mpnet-base-v2"

# Adjust search parameters
qdrant-find "query" --limit 20
```

## 📊 **Monitoring and Maintenance**

### **Health Checks**
```bash
# Check Qdrant health
curl http://localhost:6333/health

# Check collection stats
curl http://localhost:6333/collections

# Monitor storage usage
du -sh rag/qdrant_data/
```

### **Backup Strategy**
```bash
# Backup Qdrant data
tar -czf qdrant_backup_$(date +%Y%m%d).tar.gz rag/qdrant_data/

# Restore from backup
tar -xzf qdrant_backup_YYYYMMDD.tar.gz
```

## 🎯 **Next Steps**

1. **Customize the persona and context templates** for your specific project
2. **Index your existing codebase and documentation** 
3. **Test the integration** with simple queries
4. **Establish workflows** for ongoing knowledge storage
5. **Train your team** on effective RAG query patterns
6. **Monitor performance** and optimize as needed

This setup provides a solid foundation for knowledge-driven development with persistent learning and pattern recognition across your entire project ecosystem.

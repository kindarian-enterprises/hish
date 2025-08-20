# 🔌 Cursor MCP Integration Setup

This guide walks you through integrating the Kindarian Cursor Context framework with Cursor IDE using the Model Context Protocol (MCP).

## 🎯 **Overview**

The MCP integration provides these tools directly in Cursor:
- **`qdrant-find`**: Search for patterns across all your projects
- **`qdrant-store`**: Store new solutions for the entire ecosystem
- **Cross-project intelligence**: Access knowledge from all your codebases

## 🚀 **Quick Setup**

### **1. Start the Framework**
```bash
cd kindarian-cursor-context
make quick-start
```

This starts:
- Qdrant vector database (localhost:6333)
- MCP server (available via Docker Compose)
- Health checks to verify everything is working

### **2. Configure Cursor Settings**

Open Cursor settings (`Cmd/Ctrl + ,`) and add the MCP server configuration:

#### **Option A: Via Settings UI**
1. Go to **Extensions** → **MCP**
2. Add a new server with these settings:
   - **Name**: `kindarian-qdrant`
   - **Command**: `docker`
   - **Args**: See JSON below

#### **Option B: Via settings.json**
Add this to your Cursor `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "kindarian-qdrant": {
        "command": "docker",
        "args": [
          "compose", 
          "-f", "/absolute/path/to/kindarian-cursor-context/compose.rag.yml", 
          "run", "--rm", "-i", "mcp-qdrant-stdio"
        ],
        "env": {
          "QDRANT_URL": "http://localhost:6333",
          "COLLECTION_NAME": "default",
          "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2"
        }
      }
    }
  }
}
```

**⚠️ Important**: Replace `/absolute/path/to/kindarian-cursor-context/` with your actual path!

### **3. Verify Integration**

1. **Restart Cursor** completely
2. **Open the framework directory** in Cursor:
   ```bash
   cursor /path/to/kindarian-cursor-context
   ```
3. **Test the tools** in a new chat:
   ```
   List available tools
   ```
   You should see `qdrant-find` and `qdrant-store` in the response.

4. **Test knowledge search**:
   ```
   qdrant-find "authentication patterns"
   ```

## 🛠️ **Advanced Configuration**

### **Alternative MCP Setup Methods**

#### **Method 1: Direct Docker Command**
```json
{
  "mcp": {
    "servers": {
      "kindarian-qdrant": {
        "command": "docker",
        "args": [
          "run", "--rm", "-i", 
          "--network", "kindarian-rag_default",
          "-e", "QDRANT_URL=http://qdrant:6333",
          "kindarian-rag-mcp-qdrant-stdio:latest"
        ]
      }
    }
  }
}
```

#### **Method 2: Local MCP Server (Advanced)**
If you prefer running the MCP server directly:

```bash
# Install dependencies
cd kindarian-cursor-context/mcp
pip install -r requirements.txt

# Run MCP server
python -m mcp_server_qdrant
```

Then configure Cursor:
```json
{
  "mcp": {
    "servers": {
      "kindarian-qdrant": {
        "command": "python",
        "args": ["/path/to/kindarian-cursor-context/mcp/mcp_server_qdrant.py"],
        "env": {
          "QDRANT_URL": "http://localhost:6333"
        }
      }
    }
  }
}
```

### **Environment Variables**

Available environment variables for customization:

```bash
QDRANT_URL=http://localhost:6333        # Qdrant database URL
QDRANT_API_KEY=                         # Optional API key
COLLECTION_NAME=default                 # Default collection for searches
EMBEDDING_MODEL=all-MiniLM-L6-v2       # Sentence transformer model
EMBEDDING_PROVIDER=fastembed            # Provider (fastembed, openai, etc.)
```

## 🧪 **Testing the Integration**

### **Basic Functionality Test**
```bash
# In Cursor chat
qdrant-find "test query"
qdrant-store "Test information for verification"
```

### **Cross-Project Search Test**
```bash
# Index some test data first
make index-repo REPO_PATH=/path/to/your/code COLLECTION_NAME=test_project

# Then search for it
qdrant-find "patterns from your codebase"
```

### **Multi-Collection Test**
```bash
# Search across multiple project collections
qdrant-find "authentication" --limit 10
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **MCP Server Not Found**
```
Error: Cannot start MCP server
```

**Solutions**:
1. Verify Docker is running: `docker ps`
2. Check framework is started: `make status`
3. Verify path in settings.json is absolute and correct
4. Restart Cursor completely

#### **Qdrant Connection Failed**
```
Error: Connection to Qdrant failed
```

**Solutions**:
1. Check Qdrant health: `make health`
2. Restart framework: `make down && make up`
3. Check port 6333 is available: `netstat -an | grep 6333`

#### **No Collections Found**
```
No results found
```

**Solutions**:
1. Index some content: `make index-repo REPO_PATH=/path/to/code COLLECTION_NAME=my_project`
2. Check collections: `make collections`
3. Verify content was indexed: `curl http://localhost:6333/collections`

#### **Permission Denied**
```
Permission denied accessing Docker
```

**Solutions**:
1. Add user to docker group: `sudo usermod -aG docker $USER`
2. Use absolute paths in MCP configuration
3. Check Docker socket permissions

### **Debug Commands**

```bash
# Check framework status
make status
make health

# View logs
make logs

# Test MCP server directly
make mcp

# Verify collections
make collections

# Clean restart
make clean && make quick-start
```

### **Verbose Logging**

Enable debug logging by setting environment variables:

```json
{
  "mcp": {
    "servers": {
      "kindarian-qdrant": {
        "command": "docker",
        "args": ["..."],
        "env": {
          "LOG_LEVEL": "DEBUG",
          "QDRANT_LOG_LEVEL": "DEBUG"
        }
      }
    }
  }
}
```

## 🚀 **Next Steps**

Once MCP integration is working:

1. **Create project contexts**: `make new-context`
2. **Index your codebases**: `make index-repo REPO_PATH=/path/to/code COLLECTION_NAME=project_name`
3. **Start using cross-project intelligence**:
   ```
   @contexts/your-project/dev_agent_init_prompt.md
   
   qdrant-find "authentication patterns"
   qdrant-find "testing strategies for React apps"
   ```

4. **Store solutions as you discover them**:
   ```
   qdrant-store "Solution: JWT refresh tokens with React hooks - Automatic refresh, secure storage, error handling. Context: React web apps. Files: hooks/useAuth.ts"
   ```

## 🌟 **Pro Tips**

### **Effective Search Patterns**
```bash
# Specific technology patterns
qdrant-find "React component patterns for user authentication"
qdrant-find "Go microservice error handling strategies"

# Cross-technology insights  
qdrant-find "authentication flows that work with mobile and web"
qdrant-find "caching strategies for high-performance applications"

# Anti-patterns and troubleshooting
qdrant-find "common mistakes with JWT token handling"
qdrant-find "performance bottlenecks in React applications"
```

### **Knowledge Storage Best Practices**
```bash
# Include context, implementation details, and trade-offs
qdrant-store "Pattern: React Error Boundaries - Catch component errors, show fallback UI, log errors for debugging. Context: Production React apps. Trade-offs: Additional complexity vs better UX. Files: components/ErrorBoundary.tsx"

# Store anti-patterns too
qdrant-store "Anti-pattern: Directly mutating state in React - Causes re-render issues and unpredictable behavior. Alternative: Use setState or useReducer. Context: Any React application."
```

---

With MCP integration complete, you now have access to cross-project intelligence directly in Cursor! 🧠✨

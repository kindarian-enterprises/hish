# 🔌 Cursor MCP Integration

**Technical integration guide for the Model Context Protocol (MCP)**

---

## 🎯 **Quick Setup**

**For basic setup, see the [Getting Started Guide](getting-started.md).**

This guide covers the technical details of MCP integration.

---

## ⚙️ **Configuration**

### **1. Get Configuration**
```bash
make setup-cursor
```

This generates the exact configuration for your system.

### **2. Add to Cursor Settings**
Add to your Cursor `settings.json`:

```json
{
  "mcpServers": {
    "qdrant": {
      "type": "stdio",
      "command": "/absolute/path/to/kindarian-cursor-context/scripts/run-mcp-llamaindex.sh",
      "workingDirectory": "/absolute/path/to/kindarian-cursor-context",
      "env": {
        "NO_COLOR": "1"
      }
    }
  }
}
```

⚠️ **Important**: Replace `/absolute/path/to/kindarian-cursor-context/` with your actual path!

---

## 🔧 **Technical Details**

### **Environment Variables**
- `QDRANT_URL`: URL to your Qdrant instance (default: http://localhost:6333)
- `COLLECTION_NAME`: Default collection for searches (default: default)

### **Docker Configuration**
The MCP server runs in a Docker container with:
- Access to the Qdrant database
- Proper networking configuration
- Environment variable injection

### **Network Ports**
- **Qdrant**: Port 6333 (vector database)
- **MCP Server**: Dynamic ports (8000+)

---

## 📚 **Usage in Cursor**

### **Basic Queries**
```
qdrant-find "authentication patterns"
qdrant-find "testing strategies for React"
qdrant-find "Docker deployment patterns"
```

### **Storing Knowledge**
```
qdrant-store "Solution: JWT refresh token rotation - Implemented secure token management with Redis blacklist. Context: Web API authentication. Performance: <50ms response time."
```

### **Project Context**
Reference the universal init prompt:
```
@dev_agent_init_prompt.md
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

**"No such file or directory"**
- Check that the path in `settings.json` is correct
- Ensure the framework is running (`make up`)

**"Connection refused"**
- Verify Qdrant is running (`make health`)
- Check that port 6333 is accessible

**"No collections found"**
- Index some content first (`make index-repo`)
- Check collection status (`make collections`)

### **Debug Commands**
```bash
# Check framework status
make health

# View logs
make logs

# Check collections
make collections

# Test MCP server
make mcp
```

---

## 🔒 **Security Considerations**

### **Local Development**
- The MCP server runs locally in Docker
- No external network access required
- Data stays within your development environment

### **Production Use**
- Consider network security for production deployments
- Implement proper authentication if needed
- Monitor resource usage and performance

---

## 📖 **Advanced Configuration**

### **Custom Collections**
You can specify different collections for different contexts:

```json
{
  "mcpServers": {
    "qdrant-framework": {
      "type": "stdio",
      "command": "/path/to/kindarian-cursor-context/scripts/run-mcp-stdio.sh",
      "workingDirectory": "/path/to/kindarian-cursor-context",
      "env": {
        "NO_COLOR": "1",
        "COLLECTION_NAME": "kindarian_framework"
      }
    },
    "qdrant-projects": {
      "type": "stdio",
      "command": "/path/to/kindarian-cursor-context/scripts/run-mcp-stdio.sh",
      "workingDirectory": "/path/to/kindarian-cursor-context",
      "env": {
        "NO_COLOR": "1",
        "COLLECTION_NAME": "project_code"
      }
    }
  }
}
```

---

## 🎉 **Integration Complete**

**Your Cursor editor now has access to:**
- Cross-project knowledge discovery
- Pattern recognition across your entire codebase
- Institutional memory and learning
- Automated workflow management

**Next steps:**
1. [Getting Started Guide](getting-started.md) - Complete setup
2. [Agent Management](../agent-management/directing-agents.md) - Working with agents
3. [Knowledge Management](../knowledge-management/indexing-and-reindexing.md) - Indexing content

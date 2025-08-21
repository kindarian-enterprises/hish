# 🚀 Getting Started - Kindarian Cursor Context

**Complete setup in 5 minutes or less**

---

## ⚠️ **Prerequisites Check**

**Before proceeding, ensure you meet all system requirements:**
- [Main README Prerequisites](../README.md#-prerequisites---read-before-starting)

**Required software:**
- ✅ Docker 20.10+ with Docker Compose v2
- ✅ Git 2.20+
- ✅ Make 3.81+
- ✅ Python 3.8+ (for local development)

---

## 🎯 **Quick Setup (5 Minutes)**

### **1. Clone and Setup**
```bash
# Clone the framework
git clone https://github.com/kindarian-enterprises/kindarian-cursor-context.git
cd kindarian-cursor-context

# Start the framework
make quick-start
```

### **2. Create Your First Project Context**
```bash
./scripts/new-project-context.sh
```

This creates: `local/your-project-name/` (gitignored for local changes)
├── dev_agent_context.md      # Project state and history
└── README.md                 # Project documentation

**Note**: The following files are now universal and shared across all projects:
- **`dev_agent_persona.md`** - Universal dev agent persona (top-level)
- **`dev_agent_init_prompt.md`** - Universal initialization protocol (top-level)
- **`dev_agent_session_end_prompt.md`** - Universal session end protocol (top-level)

### **3. Configure Cursor MCP Integration**
```bash
make setup-cursor
```

This shows you the exact JSON to add to your Cursor `settings.json`.

### **4. Test the Integration**
Restart Cursor and test with:
```
qdrant-find "test query"
```

---

## 📚 **What You Get**

- **Universal Dev Agent**: Single, all-knowing agent persona for all projects
- **Project Contexts**: Local, gitignored project contexts in `local/`
- **Cross-Project Intelligence**: RAG-powered knowledge discovery across all projects
- **Automatic Workflow Management**: Agents record and manage workflows automatically
- **MCP Integration**: Direct access to knowledge base from Cursor

## 🔄 **How It Works**

1. **Framework Setup**: Start the RAG system and MCP server
2. **Project Contexts**: Create project contexts in `local/` (automatically gitignored)
3. **Agent Initialization**: Use universal init prompt to load project context
4. **Workflow Recording**: Ask agents to record workflows as you work
5. **Knowledge Discovery**: Use RAG tools to find patterns from all projects

**Note**: The RAG-enhanced development workflow is built into the agent persona, so agents automatically follow knowledge-first development practices. Example contexts in `contexts/` demonstrate proper structure without duplicating universal content.

---

## 🚨 **Troubleshooting**

### **Common Issues**
- **Docker not running**: Start Docker service
- **Port conflicts**: Check if ports 6333, 8000+ are available
- **Permission errors**: Ensure user is in docker group
- **Python version issues**: Use pyenv or virtual environments

### **Getting Help**
- [Complete Documentation Hub](../README.md)
- [Cursor MCP Integration](cursor-mcp-integration.md)
- [Agent Management](../agent-management/directing-agents.md)

---

## 🎉 **You're Ready!**

**Next steps:**
1. **Index your code**: `make index-repo REPO_PATH=/path/to/code COLLECTION_NAME=my_project`
2. **Initialize agent**: In Cursor, use `@dev_agent_init_prompt.md`
3. **Start querying**: Use `qdrant-find "your search terms"`
4. **Record workflows**: Ask agents to document your processes

**Welcome to cross-project intelligence! 🧠✨**

# 🚀 **Getting Started in 5 Minutes**

**Welcome to Kindarian Cursor Context! This guide gets you up and running quickly.**

---

## 🎯 **What You'll Have After This Guide**

✅ **Multi-project development agent framework**  
✅ **Shared knowledge across all your repositories**  
✅ **Cross-project pattern discovery**  
✅ **Local customization without conflicts**  
✅ **Seamless upstream collaboration**

---

## 🚀 **Step 1: Quick Setup**

```bash
# Clone the framework directly
git clone https://github.com/kindarian-enterprises/kindarian-cursor-context.git
cd kindarian-cursor-context

# Start the knowledge system
make quick-start
```

**This will:**
- Start Qdrant vector database
- Build the MCP server  
- Show you the next steps

---

## 🔄 **Step 2: Create Your Working Branch (One-time setup)**

```bash
# Create a local branch for your work
git checkout -b my-team-customization

# Create local directories for your customizations
mkdir -p local overrides private tmp

# These directories are automatically ignored by Git
# Put your machine-specific files here to avoid conflicts
```

**Why this matters:**
- Your work is on a separate branch from the main framework
- You can customize without affecting the main code
- Easy to get updates from the main repository

---

## 📥 **Step 3: Get Updates When You Want New Features**

```bash
# Use the helper script (easiest option)
./scripts/sync-upstream.sh

# OR do it manually:
git checkout main
git fetch origin
git merge origin/main
git checkout my-team-customization
git merge main
```

**When to do this:**
- When you want new framework features
- When you see updates in the main repo
- Before starting major customizations

---

## 📝 **Step 4: Create Your First Project Context**

```bash
# Create a new project context
./scripts/new-project-context.sh

# This creates: contexts/your-project-name/
# ├── dev_agent_persona.md      # Your agent's personality
# ├── dev_agent_context.md      # Project state and history  
# ├── dev_agent_init_prompt.md  # How to initialize your agent
# └── project_config.yml        # Code repo paths and settings
```

---

## 🧠 **Step 5: Index Your Code Repositories**

```bash
# Index your project's code
make index-repo REPO_PATH=/path/to/your-project COLLECTION_NAME=my_project_code

# Index another project
make index-repo REPO_PATH=/path/to/another-project COLLECTION_NAME=another_project_code
```

**What happens:**
- Your code gets converted to searchable knowledge
- Patterns are discovered across projects
- You can query for solutions from any project

---

## 🔌 **Step 6: Configure Cursor MCP Integration**

```bash
# Get the exact configuration for your system
make setup-cursor
```

**This shows you the JSON to add to Cursor `settings.json`**

---

## 🎭 **Step 7: Initialize Your Agent**

In Cursor, open the kindarian-cursor-context framework and reference your project:

```
@contexts/your-project-name/dev_agent_init_prompt.md
```

**✅ You now have access to:**
- `qdrant-find "search query"` - Search patterns across all projects
- `qdrant-store "solution description"` - Store new solutions for the ecosystem

---

## 🧪 **Test Your Setup**

Try this in Cursor chat:

```
Research authentication patterns across our projects and propose an approach for this context that leverages our proven solutions.
```

**The agent will automatically:**
- Query knowledge base with `qdrant-find`
- Analyze patterns across projects
- Propose solutions combining best practices
- Store new solutions with `qdrant-store`

---

## 🎯 **What You Can Do Now**

### **Cross-Project Intelligence**
- Find solutions from ANY project when working on any other
- Discover patterns you didn't know existed
- Learn from your entire engineering history

### **Local Customization**
- Customize the framework for your team
- Add machine-specific configurations
- Keep everything in sync with upstream updates

### **Knowledge Sharing**
- Store successful patterns for future use
- Share solutions across your organization
- Build institutional knowledge

---

## 🔍 **Troubleshooting Common Issues**

### **"make: docker-compose: No such file or directory"**
**Problem:** Your system has Docker Compose v2 (modern) but the framework is configured for v1
**Solution:** This is already fixed! The framework now uses `docker compose` (v2 syntax)

### **"Permission denied" errors**
**Problem:** Docker permission issues
**Solution:**
```bash
# Add your user to docker group (one-time setup)
sudo usermod -aG docker $USER
# Log out and back in, then test:
docker run hello-world
```

### **"No such collection" when querying**
**Problem:** You haven't indexed any content yet
**Solution:**
```bash
# Index some content first
make index-repo REPO_PATH=/path/to/your-code COLLECTION_NAME=my_project
# Then check collections
make collections
```

### **Framework won't start**
**Problem:** Port conflicts or Docker issues
**Solution:**
```bash
# Check what's using port 6333
sudo lsof -i :6333
# Stop conflicting services, then:
make down && make up
```

## 🆘 **Need More Help?**

- **📚 [Complete Setup Guide](environment-setup.md)** - Detailed configuration
- **🔄 [Upstream Workflow](upstream-main-workflow.md)** - Collaboration guide  
- **❓ [FAQ](../faq.md)** - Common questions
- **🎭 [Example Contexts](../contexts/)** - See real examples

---

## 🚀 **Next Steps**

1. **Explore the examples**: Check out `contexts/example-*` for real usage
2. **Customize for your team**: Modify `env.framework` for your environment
3. **Index more projects**: Add your entire codebase ecosystem
4. **Share patterns**: Store solutions that others can discover

---

**🎉 You're now ready to transform your development workflow from reactive problem-solving to proactive, knowledge-driven engineering!**

*Questions? Check the guides above or use the helper scripts - they're designed to make everything simple.*

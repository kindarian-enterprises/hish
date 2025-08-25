# 🗂️ Knowledge Indexing and Reindexing Guide

This guide covers when, why, and how to index and reindex documentation and code in the Hish framework.

## 🎯 **When to Index/Reindex**

### **Initial Setup Indexing**

**When setting up the framework:**
```bash
# Index everything automatically
make index
```

This automatically indexes:
- **Framework documentation** (templates, workflows, guides) → `hish_framework` collection
- All local project contexts in `local/`
- **All project code repositories** (discovered automatically from project contexts)

**🧠 Cross-Project Intelligence:** Use `cross_project_intelligence` collection for dynamic observations and patterns. 

**⚠️ IMPORTANT:** Intelligence collection requires UUIDs for storage:
```bash
python3 -c "import uuid; print(uuid.uuid4())"  # Generate UUID first
qdrant-store "your observation..." cross_project_intelligence [UUID]
```

See [Cross-Project Intelligence Architecture](cross-project-intelligence-architecture.md) for details.

**How it works:**
1. When you create a project context with `make new-context`, you provide the path to your code repository
2. The framework stores this path in `local/your-project/repo_path.txt`
3. `make index` automatically discovers all these paths and indexes the code
4. No need to remember or manually specify repository paths!

### **Regular Reindexing Triggers**

**📅 Scheduled Reindexing (Weekly/Bi-weekly):**
- Keep knowledge fresh with recent code changes
- Capture new documentation and README updates
- Ensure agents have access to latest patterns

**🔄 Event-Driven Reindexing:**
- After major feature implementations
- When new workflow documentation is created
- After architectural decisions are documented
- When anti-patterns are identified and documented

**🚨 Quality-Driven Reindexing:**
- When agents repeatedly miss recent solutions
- After significant refactoring or code restructuring
- When knowledge queries return outdated results

## 🧠 **Why Reindexing Matters**

### **Knowledge Freshness**
- **Agents need current information** to make good decisions
- **Recent solutions** should be discoverable and applicable
- **Outdated patterns** can lead to deprecated approaches

### **Pattern Evolution**
- **Solutions improve over time** and should replace older approaches
- **New technologies** require updated implementation patterns
- **Cross-project learnings** accumulate and need to be accessible

### **Quality Compound Effect**
- **Fresh knowledge** leads to better agent decisions
- **Updated patterns** prevent regression to old approaches
- **Current examples** provide better implementation guidance

## 🛠️ **How to Index Effectively**

### **🚀 Host-Based Indexing**

**All indexing is now host-based for optimal performance:**
```bash
# Full indexing: framework + all project repositories
make index

# Framework documentation only (quick updates)
make index-framework

# Specific repository indexing
make index-repo REPO_PATH=/path/to/repo COLLECTION_NAME=collection_name
```

**Requirements:** Python 3.12+ virtual environment with dependencies installed:
```bash
pip install -r rag/indexer/requirements.txt
```

**Benefits:**
- **2-4x faster** than container-based approaches
- Better memory utilization for large repositories
- Direct filesystem access
- No Docker volume mount overhead

### **Setup Requirements**

**One-time virtual environment setup:**
```bash
# Using virtualenvwrapper (recommended)
mkvirtualenv hish-indexing --python=python3.12
pip install -r rag/indexer/requirements.txt

# Or using standard venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r rag/indexer/requirements.txt
```

**Daily usage:**
```bash
workon hish-indexing  # or: source .venv/bin/activate
make index-framework  # Quick framework updates
make index           # Full indexing when needed
```

### **Collection Strategy**

**Collections are created automatically:**
- `hish_framework` - Framework documentation, templates, and local contexts
- `cross_project_intelligence` - Dynamic observations, patterns, and relationships
- `{project_name}_code` - Source code (when manually indexed)
- `{project_name}_docs` - Project documentation (when manually indexed)

**Note:** Collection names are discovered automatically by agents during indexing. No manual configuration needed.

## 📋 **Indexing Workflows**

### **New Project Integration**

**When adding a new project to the framework:**

1. **Create project context:**
   ```bash
   make new-context
   # Follow prompts to create local/new-project/
   # The command will ask for your code repository path
   ```

2. **Index everything:**
   ```bash
   make index
   ```

3. **Agent discovers context automatically:**
   The agent will read the context directory structure and understand project relationships without configuration

### **Weekly Maintenance Reindexing**

**Recommended weekly workflow:**

```bash
# 1. Check what's changed
git log --since="1 week ago" --oneline

# 2. Index everything (framework + all project code)
make index

# 3. That's it! The framework automatically handles all repositories
```

### **After Major Documentation Updates**

**When significant documentation is created:**

```bash
# Index everything to capture all changes
make index
```

This will automatically include:
- New workflow documentation
- Updated project contexts
- New architectural decisions
- Anti-patterns and lessons learned

## 🔍 **Monitoring Indexing Health**

### **Check Collection Status**

```bash
# View all collections and their sizes
make collections

# Check framework health
make health

# View recent indexing logs
make logs
```

### **Quality Indicators**

**Healthy indexing signs:**
- Collections grow as new content is added
- Agents find relevant recent solutions
- Cross-project patterns are discoverable
- Recent workflow docs are applied by agents

**Reindexing needed indicators:**
- Agents suggest outdated approaches
- Recent solutions aren't being discovered
- Knowledge queries return old results
- Agents don't find newly documented patterns

### **Troubleshooting Indexing Issues**

**If indexing fails:**
```bash
# Check service connectivity in Cursor

# Restart services if needed
Restart Cursor MCP integration

# Check disk space for Qdrant data
du -sh rag/qdrant_data/
```

**If agents aren't finding recent content:**
- Verify recent content was actually indexed
- Run `make index` to ensure everything is up to date
- Check that content is in the expected directories

## 🎯 **Best Practices**

### **Indexing Frequency**

**High-frequency reindexing (daily/weekly):**
- Use `make index` after significant changes
- Reindex when adding new project contexts
- Reindex after creating new workflows

**Medium-frequency reindexing (bi-weekly/monthly):**
- Use `make index` for regular maintenance
- Reindex stable project codebases
- Reindex framework documentation

**Low-frequency reindexing (monthly/quarterly):**
- Legacy project code
- Stable shared libraries
- Historical documentation

### **Collection Management**

**Collections are managed automatically:**
- Framework creates appropriate collections
- Agents discover and organize content
- No manual collection configuration needed
- Context relationships are inferred from directory structure

### **Automation Opportunities**

**Consider automating:**
- Weekly `make index` runs
- Indexing triggered by significant git commits
- Notification when indexing hasn't been run recently

**Manual indexing for:**
- New project integration
- Major architectural changes
- Quality-driven reindexing decisions

---

## 🚀 **Quick Reference Commands**

```bash
# Index everything automatically (RECOMMENDED)
make index

# Check indexing health
# Check MCP connection status in Cursor
make collections

# Advanced: Index specific content manually
make index-repo REPO_PATH=/path/to/content COLLECTION_NAME=collection_name
```

---

**For most users, `make index` is all you need. It automatically discovers and indexes all your project code repositories!**

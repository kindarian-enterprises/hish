# 🗂️ Knowledge Indexing and Reindexing Guide

This guide covers when, why, and how to index and reindex documentation and code in the Kindarian Cursor Context framework.

## 🎯 **When to Index/Reindex**

### **Initial Setup Indexing**

**When setting up the framework:**
1. **Index the framework itself**: Templates, workflows, documentation
2. **Index existing code repositories**: All your current projects
3. **Index existing documentation**: READMEs, architecture docs, runbooks

```bash
# Index the framework documentation
make index-repo REPO_PATH=. COLLECTION_NAME=framework_docs

# Index your existing projects
make index-repo REPO_PATH=/path/to/project-alpha COLLECTION_NAME=project_alpha_code
make index-repo REPO_PATH=/path/to/project-beta COLLECTION_NAME=project_beta_code
```

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

### **Collection Strategy**

**Separate collections by purpose:**
```bash
# Framework and documentation
framework_docs          # This framework's documentation
shared_patterns         # Cross-project patterns and workflows

# Project-specific collections
project_alpha_code      # Source code and implementations
project_alpha_docs      # Project-specific documentation
project_beta_code       # Another project's code
project_beta_docs       # Another project's documentation

# Technology-specific collections
react_patterns          # React/frontend patterns across projects
api_patterns           # Backend/API patterns across projects
mobile_patterns        # Mobile development patterns
```

**Collection naming convention:**
- `{project_name}_code` - Source code and implementations
- `{project_name}_docs` - Project documentation
- `{technology}_patterns` - Technology-specific patterns
- `framework_docs` - Framework documentation
- `shared_patterns` - Cross-project patterns

**Note:** Collection names are discovered automatically by agents during indexing. No manual configuration needed.

### **Indexing Commands Reference**

**Framework documentation:**
```bash
# Index framework docs (workflows, guides, templates)
make index-repo REPO_PATH=. COLLECTION_NAME=framework_docs
```

**Project code repositories:**
```bash
# Index source code for pattern discovery
make index-repo REPO_PATH=/path/to/project COLLECTION_NAME=project_name_code
```

**Project documentation:**
```bash
# Index READMEs, docs/, architecture documentation
make index-repo REPO_PATH=/path/to/project/docs COLLECTION_NAME=project_name_docs
```

**Workflow and process documentation:**
```bash
# Index new workflow documentation
make index-repo REPO_PATH=./workflows-and-processes COLLECTION_NAME=shared_patterns
```

### **Selective Reindexing**

**When you don't need full reindexing:**
- Only documentation changed: reindex docs collections
- Only code changed: reindex code collections
- New workflow created: reindex shared_patterns collection

**Full reindexing triggers:**
- Major framework updates
- Significant architectural changes across projects
- New project additions to the ecosystem

## 📋 **Indexing Workflows**

### **New Project Integration**

**When adding a new project to the framework:**

1. **Create project context:**
   ```bash
   make new-context
   # Follow prompts to create contexts/new-project/
   ```

2. **Index project code:**
   ```bash
   make index-repo REPO_PATH=/path/to/new-project COLLECTION_NAME=new_project_code
   ```

3. **Index project documentation:**
   ```bash
   make index-repo REPO_PATH=/path/to/new-project/docs COLLECTION_NAME=new_project_docs
   ```

4. **Agent discovers context automatically:**
   The agent will read the context directory structure and understand project relationships without configuration

### **Weekly Maintenance Reindexing**

**Recommended weekly workflow:**

```bash
# 1. Check what's changed
git log --since="1 week ago" --oneline

# 2. Reindex framework docs if workflows/docs changed
make index-repo REPO_PATH=. COLLECTION_NAME=framework_docs

# 3. Reindex active project code
make index-repo REPO_PATH=/path/to/active-project COLLECTION_NAME=active_project_code

# 4. Reindex shared patterns if new workflows created
make index-repo REPO_PATH=./workflows-and-processes COLLECTION_NAME=shared_patterns
```

### **After Major Documentation Updates**

**When significant documentation is created:**

1. **Workflow documentation created:**
   ```bash
   make index-repo REPO_PATH=./workflows-and-processes COLLECTION_NAME=shared_patterns
   ```

2. **Architecture decisions documented:**
   ```bash
   make index-repo REPO_PATH=/path/to/project/docs COLLECTION_NAME=project_name_docs
   ```

3. **Anti-patterns documented:**
   ```bash
   make index-repo REPO_PATH=./workflows-and-processes COLLECTION_NAME=shared_patterns
   ```

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
# Check service health
make health

# Restart services if needed
make down && make up

# Check disk space for Qdrant data
du -sh .data/qdrant/
```

**If agents aren't finding recent content:**
- Verify recent content was actually indexed
- Check collection names match project configurations
- Ensure agents are querying appropriate collections

## 🎯 **Best Practices**

### **Indexing Frequency**

**High-frequency reindexing (daily/weekly):**
- Active development projects
- Frequently updated documentation
- Workflow and process documentation

**Medium-frequency reindexing (bi-weekly/monthly):**
- Stable project codebases
- Architecture documentation
- Framework documentation

**Low-frequency reindexing (monthly/quarterly):**
- Legacy project code
- Stable shared libraries
- Historical documentation

### **Collection Management**

**Keep collections focused:**
- Don't mix code and documentation in same collection
- Separate by technology when patterns differ significantly
- Use descriptive, consistent naming conventions

**Monitor collection sizes:**
- Large collections (>10k chunks) may need splitting
- Very small collections (<100 chunks) may need combining
- Balance between specificity and discoverability

**Collection discovery:**
- Agents automatically discover and organize collections during indexing
- No manual collection configuration needed
- Context relationships are inferred from directory structure and content

### **Automation Opportunities**

**Consider automating:**
- Weekly reindexing of active projects
- Indexing triggered by significant git commits
- Notification when collections haven't been updated recently

**Manual indexing for:**
- New project integration
- Major architectural changes
- Quality-driven reindexing decisions

---

## 🚀 **Quick Reference Commands**

```bash
# Check indexing health
make health
make collections

# Index new content
make index-repo REPO_PATH=/path/to/content COLLECTION_NAME=collection_name

# Framework maintenance
make index-repo REPO_PATH=. COLLECTION_NAME=framework_docs
make index-repo REPO_PATH=./workflows-and-processes COLLECTION_NAME=shared_patterns

# Project maintenance
make index-repo REPO_PATH=/path/to/project COLLECTION_NAME=project_code
make index-repo REPO_PATH=/path/to/project/docs COLLECTION_NAME=project_docs
```

---

**Regular indexing keeps your knowledge fresh and ensures agents have access to your latest wisdom and patterns. Make it part of your development rhythm.**

# 🧠 Hish

**A comprehensive prompt and knowledge framework for managing multiple development agents with shared context and cross-project intelligence.**

---

## 🎯 **Why This Framework Exists**

**The Problem**: You're using Cursor with AI models, but they don't know your codebase, your development decisions, your patterns, or your philosophy. Every conversation starts from scratch, and you waste time explaining context that should already be known.

**The Solution**: Hish transforms ANY AI model in Cursor into a powerful coding assistant with full knowledge of your development ecosystem. No more dedicated "coding agent" services needed.

### **What This Means for You**

**🧠 Instant Context**: Any AI model you use in Cursor immediately knows your codebase structure, architectural decisions, and development patterns.

**💡 Informed Decisions**: AI assistants understand your dev philosophy, coding standards, and why previous decisions were made.

**🚀 No More Repetition**: Stop explaining your project structure, tech stack, and patterns every time you start a new conversation.

**🎯 Universal Intelligence**: Whether you're using Claude, GPT, or any other model, they all get the same comprehensive context.

### **The Transformation**

**Before**: Every AI conversation feels like starting from scratch. You're constantly explaining your architecture, justifying past decisions, and re-teaching your development philosophy. It's like having a brilliant intern who shows up every day with amnesia.

**After**: Every AI model in Cursor becomes a seasoned member of your development team. They understand your codebase like they've been working on it for years. They know why you chose that authentication pattern, remember the performance issues you solved last month, and can suggest improvements based on your established standards.

**This isn't about managing multiple projects—it's about finally having AI coding assistants that actually understand your work instead of just guessing at it.**

---

## ⚠️ **PREREQUISITES - READ BEFORE STARTING** ⚠️

**🚨 MANDATORY: Your system must meet these requirements before proceeding**

### **Required Software**
- **Docker**: Version 20.10+ with Docker Compose v2
  ```bash
  # Verify installation
  docker --version
  docker compose version
  ```
- **Git**: Version 2.20+
  ```bash
  git --version
  ```
- **Make**: GNU Make 3.81+
  ```bash
  make --version
  ```

### **Python Environment (for local development)**
- **Python**: Version 3.12+ (required for host-based indexing, 3.8+ for MCP server only)
- **pip**: Latest version
- **pyenv** (optional): For Python version management
  ```bash
  # If using pyenv, ensure it's properly configured
  pyenv versions
  python --version
  ```

### **Virtual Environment Setup (Recommended for Host-Based Indexing)**
**🚀 NEW: Host-based indexing provides significantly better performance than container-based indexing**

For optimal performance with the new host-based indexing system, set up a Python virtual environment:

**Option 1: Using virtualenvwrapper (Recommended)**
```bash
# Install virtualenvwrapper (if not already installed)
pip install virtualenvwrapper

# Add to your shell profile (.bashrc, .zshrc, etc.)
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

# Create and activate virtual environment
mkvirtualenv hish-indexing
workon hish-indexing

# Install dependencies manually in your virtual environment
pip install -r rag/indexer/requirements.txt
```

**Option 2: Using standard venv**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies manually in your virtual environment
pip install -r rag/indexer/requirements.txt
```

**✅ Benefits of host-based indexing:**
- **2-4x faster** indexing performance
- Better memory utilization for large repositories
- No Docker volume mount overhead
- Direct filesystem access

**Note:** Install dependencies manually in your virtual environment: `pip install -r rag/indexer/requirements.txt`

### **Network Requirements**
- **Internet Access**: Required for Docker image pulls and dependencies
- **Ports**: 6333 (Qdrant), 8000+ (MCP server)
- **Firewall**: Ensure Docker can bind to required ports

### **Troubleshooting Common Issues**
- **Docker Permission Errors**: Add user to docker group or use `sudo`
- **Port Conflicts**: Check if ports 6333, 8000+ are available
- **Python Version Issues**: Use pyenv or virtual environments for isolation

**✅ All prerequisites met? Continue to Quick Start below!**

---

## 🆕 **NEW USER? START HERE! 🆕**

**🎯 This is a completely NEW TOOL - designed to be painless and unobtrusive!**

### **📚 [Getting Started Guide](docs/setup/getting-started.md) - 5 Minutes to Full Setup**
**Complete step-by-step onboarding with everything you need to know.**

### **🔄 [Upstream + Main Workflow](docs/setup/upstream-main-workflow.md) - Zero-Conflict Collaboration**
**Seamless team collaboration with automatic updates from the official repo.**

### **❓ [FAQ](docs/faq.md) - Common Questions Answered**
**Quick answers to get you unstuck fast.**

---

**🚀 Ready to transform your development workflow? Start with the Getting Started Guide above!**

## 🎯 **What Is This?**

Hish Cursor Context is a multi-project development agent framework that transforms your entire engineering ecosystem into a knowledge-powered learning machine:

- **Multi-Project Intelligence**: One framework manages contexts for all your projects
- **Shared Knowledge Base**: Patterns discovered in one project benefit ALL projects
- **Cross-Project Learning**: Agents learn from your entire codebase ecosystem
- **Centralized Context Management**: All project contexts, personas, and knowledge in one place
- **Institutional Memory**: Persistent learning across teams, projects, and time
- **Pattern Recognition**: Discover solutions from any project when working on any other project

## 🚀 **Quick Start (5 Minutes to Full Setup)**

**🎯 NEW TOOL ALERT: This is a completely new development workflow - designed to be painless and unobtrusive!**

### **📚 Start Here: [Getting Started Guide](docs/setup/getting-started.md)**

**Complete step-by-step onboarding with screenshots and examples.**

### **1. Set Up the Framework**
```bash
# Clone the framework directly from the main repository
git clone https://github.com/kindarian-enterprises/hish.git
cd hish

# Quick setup guide (shows configuration steps)
make quick-start

# This will:
# - Show MCP configuration steps
# - Explain the setup workflow
# - No Docker startup needed (Cursor handles that)
```

### **2. Configure Cursor MCP Integration**
```bash
# Get MCP configuration
make setup-cursor

# Add the provided JSON to Cursor settings.json and restart Cursor
```

### **3. Create Your First Project Context**
```bash
# Create a new project context (simplified setup)
make new-context

# This creates: local/your-project-name/ (gitignored for local changes)
# ├── dev_agent_context.md      # Project state and history
# └── README.md                 # Project documentation
```

**Note**: The following files are now universal and shared across all projects:
- **`dev_agent_persona.md`** - Universal dev agent persona (top-level)
- **`dev_agent_init_prompt.md`** - Universal initialization protocol (top-level)
- **`dev_agent_session_end_prompt.md`** - Universal session end protocol (top-level)

### **4. Index Your Code Repositories**
```bash
# 🚀 NEW: Host-based indexing (faster, recommended)
make index-host

# OR: Container-based indexing (original method)
make index

# OR: Framework documentation only (quick updates)
make index-framework

# Advanced: Index specific repositories manually
make index-repo REPO_PATH=/path/to/your-project-code COLLECTION_NAME=your_project_code

# All projects share the same knowledge base for cross-project insights!
```

### **5. Test the Integration**
```bash
# In Cursor, initialize your agent with:
# @dev_agent_init_prompt.md

# Test RAG queries:
# qdrant-find "test query"
```

**Quick MCP Setup**: Add this to your Cursor `settings.json`:
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
⚠️ **Replace `/absolute/path/to/hish/` with your actual path!**

### **5. Initialize Your Agent**
In Cursor, open the hish framework and reference the universal init prompt:
```
@dev_agent_init_prompt.md
```

The agent will automatically:
- Load the universal persona from `dev_agent_persona.md`
- Load project-specific context from `local/your-project-name/dev_agent_context.md`
- Be ready to operate with both universal intelligence and project-specific knowledge

**✅ You should now have access to these tools in Cursor:**
- `qdrant-find "search query"` - Search patterns across all your projects
- `qdrant-store "solution description"` - Store new solutions for the ecosystem

**🧪 Test your setup by directing the agent:**
```
Research authentication patterns across our projects and propose an approach for this context that leverages our proven solutions.
```

The agent will automatically:
- Query knowledge base with `qdrant-find`
- Analyze patterns across projects
- Propose solutions combining best practices
- Store new solutions with `qdrant-store`

## 🔄 **Simple Collaboration Workflow (NEW!)**

**🚀 Zero merge conflicts with local customization - designed for teams!**

### **📖 Complete Guide: [Collaboration Workflow](docs/setup/upstream-main-workflow.md)**

**What this means for you:**
- **Clone directly** from the main repository
- **Local overrides** in ignored folders (automatically safe)
- **Easy updates** from the main repo when you want new features

**Result**: Clean collaboration, no merge conflicts, easy customization.

### **⚡ One-time Setup (2 minutes)**
```bash
# Clone the repository
git clone https://github.com/kindarian-enterprises/hish.git
cd hish

# Create your working branch
git checkout -b my-team-customization

# Create local directories for your customizations
mkdir -p local overrides private tmp
```

### **🔄 Daily Workflow (30 seconds)**
```bash
# Get updates when you want new features
git checkout main
git fetch origin
git merge origin/main
git checkout my-team-customization
git merge main

# Work on your changes as normal
git add . && git commit -m "Your changes"
git push origin my-team-customization
```

### **🛡️ Local Customization (Zero Conflicts)**
```bash
# Put your machine-specific files here (automatically ignored):
mkdir local
cp env.framework local/env.framework.my-team

# Edit local/env.framework.my-team with your changes
# This won't conflict with main repo updates!
```

**🎯 See [Collaboration Workflow Guide](docs/setup/upstream-main-workflow.md) for complete details.**

## 📚 **What's Included**

### **Core Templates**
- **`templates/context/dev_agent_context_template.md`** - **REQUIRED** - Scaffold for new project contexts (contains the critical update protocol and comprehensive project tracking structure)
- **`contexts/`** - Framework examples showing proper context structure (no persona/prompts - those are universal)

### **🔄 Workflow Templates**
```
workflows-and-processes/     # Framework examples and shared patterns (tracked)
```

**Note**: User-specific workflows are automatically created in `local/workflows-and-processes/` when the first project context is added. Users ask agents to record and manage workflows rather than writing them manually. The RAG-enhanced development workflow is built into the agent persona.

### **🧠 RAG Infrastructure**
```
rag/                   # Knowledge indexing and search
mcp/                   # Model Context Protocol server
compose.rag.yml        # Docker orchestration for Qdrant vector DB
```

### **📖 Documentation**
```
docs/
├── integration/       # RAG/MCP setup guides
├── philosophy/        # Knowledge-driven development principles
└── setup/            # Installation and configuration guides
```

## 🎭 **Agent Persona System**

**Universal Intelligence**: The framework provides a single, comprehensive dev agent persona that operates across all projects.

**No configuration files needed** - agents intelligently discover context and relationships from directory structure and content.

The universal persona includes:

- **Universal Expertise**: Multi-project intelligence, technology agnostic, development methodologies
- **Coding Standards**: Language-agnostic patterns, quality requirements, anti-patterns
- **Architectural Philosophy**: Design principles, decision-making frameworks, quality evolution
- **RAG Integration**: Knowledge discovery and storage workflows across all projects

### **Project-Specific Context**
Each project in `local/` contains:
- **Project State**: Current status, achievements, issues, and historical tracking
- **Initialization Protocol**: How to initialize the agent for this specific project
- **Session Management**: Continuity and knowledge capture protocols

## 📊 **Context Management System**

The context template provides structured tracking of:

- **Project Phases**: Current status, goals, deliverables
- **Component Status**: Architecture, implementation state
- **Achievements**: Historical accomplishments with timestamps
- **Issues**: Current blockers, technical debt, priorities
- **Lessons Learned**: Anti-patterns, successful solutions

### **Update Protocol Enforcement**
- **Verified Timestamps**: No hallucinated dates allowed
- **Append-Only**: Preserve all historical information
- **Structured Format**: Consistent syntax for machine processing
- **Change Tracking**: Every modification requires rationale

## 🧠 **Knowledge-Driven Development**

### **RAG-Enhanced Workflow**
```bash
# Before implementing: Query existing patterns
qdrant-find "authentication implementation patterns"
qdrant-find "error handling approaches for APIs"

# After solving: Store new knowledge
qdrant-store "Solution: JWT refresh token rotation - Implemented secure token management with Redis blacklist. Context: Web API authentication. Performance: <50ms response time."
```

### **Cross-Project Learning**
- **Pattern Recognition**: Identify successful approaches across codebases
- **Anti-Pattern Avoidance**: Learn from historical mistakes
- **Decision Context**: Understand why previous choices were made
- **Performance Insights**: Apply optimization patterns that work

### **Automatic Indexing**
- **Local Contexts**: All project contexts in `local/` are automatically indexed
- **Framework Content**: Documentation, workflows, and examples are indexed
- **Cross-Project Discovery**: Find patterns from any project when working on any other

## 🛠️ **Setup Workflows**

### **For New Projects**
1. Copy and customize templates
2. Set up RAG infrastructure (optional)
3. Index existing codebase and documentation
4. Train team on knowledge query patterns
5. Establish context update protocols

### **For Existing Projects**
1. Create context based on current practices
2. Document current state in context template
3. Gradually build knowledge base from tribal knowledge
4. Integrate RAG queries into daily development
5. Store solutions as they are discovered

### **For Teams**
1. Establish shared context standards
2. Create team-wide knowledge collections
3. Set up automated knowledge capture workflows
4. Train on effective RAG query patterns
5. Implement knowledge review processes

## 🌟 **Cross-Project Intelligence in Action**

### **Real Example: Authentication Solution Discovery**
```bash
# 🎯 Scenario: You're building a new mobile app and need authentication

# 1. Query across ALL your projects for auth patterns
qdrant-find "JWT refresh token implementations"

# 2. Framework finds solutions from:
# - Web App: React useAuth hook with automatic refresh
# - API Service: Go middleware with Redis token blacklist  
# - Previous Mobile: React Native secure storage patterns
# - Shared: OAuth2 server configuration

# 3. You adapt the best patterns for your new context
qdrant-store "Mobile Auth Solution: Combined web useAuth pattern with RN secure storage - Automatic token refresh, biometric fallback, offline support. Context: React Native apps. Performance: <200ms auth check. Files: hooks/useAuth.ts, utils/secureStorage.ts"

# 4. Your solution becomes available to ALL future projects!
```

### **Example: Performance Pattern Cross-Pollination**
```bash
# API team discovers caching strategy
qdrant-store "Redis Caching Layer: 80% latency reduction with write-through cache - Cache user sessions, API responses, computed values. Context: High-traffic APIs. Implementation: Redis cluster with TTL."

# Mobile team later queries for performance
qdrant-find "caching strategies for better performance"
# Discovers the API caching pattern and adapts it for mobile local storage

# Web team benefits too
qdrant-find "user session optimization patterns"  
# Finds both API Redis patterns and mobile storage patterns
```
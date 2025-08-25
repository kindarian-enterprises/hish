# Hish

Context management framework for AI coding assistants in Cursor. Provides persistent memory and cross-project knowledge sharing via RAG + MCP integration.

## Problem

AI models in Cursor lack context about your codebase, architecture decisions, and development patterns. Each conversation starts from zero knowledge.

## Solution

- **Persistent Context**: AI models access your codebase structure, patterns, and decisions via vector search
- **Cross-Project Knowledge**: Solutions from one project inform work on others
- **Zero Configuration**: Automatic context discovery and indexing

---

## Prerequisites

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

### Python Environment
- **Python**: 3.8+ (3.12+ recommended for indexing performance)
- **Virtual Environment**: Required for indexing

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

Install dependencies: `pip install -r rag/indexer/requirements.txt`

### **Network Requirements**
- **Internet Access**: Required for Docker image pulls and dependencies
- **Ports**: 6333 (Qdrant), 8000+ (MCP server)
- **Firewall**: Ensure Docker can bind to required ports

### **Troubleshooting Common Issues**
- **Docker Permission Errors**: Add user to docker group or use `sudo`
- **Port Conflicts**: Check if ports 6333, 8000+ are available
- **Python Version Issues**: Use pyenv or virtual environments for isolation



## Quick Start

### 1. Set Up the Framework
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

### 2. Configure Cursor MCP Integration
```bash
# Get MCP configuration
make setup-cursor

# Add the provided JSON to Cursor settings.json and restart Cursor
```

### 3. Create Your First Project Context
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

### 4. Index Your Code Repositories
```bash
# Index everything: framework docs + all project repositories
make index

# OR: Framework documentation only (quick updates)
make index-framework

# Advanced: Index specific repositories manually
make index-repo REPO_PATH=/path/to/your-project-code COLLECTION_NAME=your_project_code

# Projects share knowledge base for cross-project insights
```

**Requirements**: Python 3.12+ and dependencies: `pip install -r rag/indexer/requirements.txt`

### 5. Test the Integration
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

### 5. Initialize Your Agent
In Cursor, reference: `@dev_agent_init_prompt.md`

Available tools:
- `qdrant-find "search query"` - Search indexed knowledge
- `qdrant-store "solution description"` - Store solutions

## Collaboration

See: [Upstream + Main Workflow](docs/setup/upstream-main-workflow.md)
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



## Architecture

### Components
- `rag/` - Knowledge indexing and search
- `mcp/` - Model Context Protocol server
- `deploy/compose.rag.yml` - Docker orchestration for Qdrant vector DB
- `config/` - Environment configuration files

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

## Project Contexts

Each project in `local/` tracks:
- Current status, achievements, issues
- Architecture and implementation state  
- Historical decisions and patterns

Workflow:
```bash
# Query existing patterns
qdrant-find "authentication patterns"

# Store new solutions  
qdrant-store "Solution: JWT with Redis blacklist"
```

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
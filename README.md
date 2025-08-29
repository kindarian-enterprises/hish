# Hish

Context management framework that gives Cursor AI agents persistent memory and cross-project knowledge. Instead of starting every conversation from zero, agents remember your codebase patterns, architectural decisions, and working solutions from all your projects.

**Two-part approach**: 
1. **Vector database** indexes your code into searchable knowledge
2. **Structured prompts** transform any LLM into a disciplined engineering agent

**Works with any model** - Claude, GPT-4, Gemini. The behavioral patterns are encoded in prompts, not dependent on model training.

## How It Works

### Indexing Your Codebase

The framework scans your repositories and breaks them into searchable knowledge:

**What gets indexed:**
- Source code files (functions, classes, patterns)
- Documentation and README files  
- Configuration files and deployment scripts
- Project contexts and historical decisions

**Chunking strategy**: Files get broken into overlapping chunks with repository, file path, and context metadata.

**Vector embeddings**: Creates semantic embeddings so similar code patterns cluster together in vector space, making them discoverable through natural language queries.

### Agent Intelligence

Once indexed, your code becomes searchable agent memory that works through structured behavioral prompts:

```
Your Code → Vector Index → Prompt-Guided Agent → Disciplined Output
```

**Prompt engineering system**: Instead of hoping LLMs follow good practices, Hish embeds engineering discipline directly into agent instructions through layered prompt structures:

- **Context injection**: Agents must load project state before starting work
- **Protocol enforcement**: Specific workflows for research → implementation → quality assurance  
- **Knowledge integration**: Mandatory patterns for querying existing solutions and storing new ones
- **Quality standards**: Built-in coding practices, anti-patterns, and engineering discipline

**Behavioral transformation**: Raw LLMs are unfocused and inconsistent. Hish prompts create agents that automatically query existing patterns, propose evidence-based solutions, implement with quality standards, and store results for team reuse.

**Technical architecture**: Qdrant vector database + MCP protocol bridge + automated indexing + structured prompt engineering. Standard RAG enhanced with behavioral discipline.

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



## Setup (5 minutes)

```bash
# 1. Clone
git clone https://github.com/kindarian-enterprises/hish.git
cd hish

# 2. Add to Cursor settings.json (restart Cursor after)
make setup-cursor

# 3. Create project context
make new-context

# 4. Index your code (requires Python 3.8+)
pip install -r rag/indexer/requirements.txt
make index

# 5. Test in Cursor
# @dev_agent_init_prompt.md
# qdrant-find "your search terms"
```

**What actually happens:**
- Step 2: Adds MCP server config to Cursor
- Step 3: Creates `local/project-name/` (gitignored)
- Step 4: Builds vector index of your code + docs
- Step 5: AI agents can now query/store knowledge

## Agent Workflow

### Session Initialization
```
@dev_agent_init_prompt.md
```
Agent loads project context, reads all relevant documentation, establishes cross-project intelligence protocols, and prepares for knowledge-driven development.

### Actual Usage Pattern

```
You: "I need to implement JWT authentication for this Node.js API"

Agent (with Hish): 
- Automatically queries existing auth patterns
- Finds Redis blacklist approach from ProjectA, refresh token logic from ProjectB
- Proposes solution: "I found proven JWT implementations across your projects..."
- Implements code using established patterns
- Stores new solution in knowledge base for team reuse

You: Just tell the agent what you want. It handles the knowledge discovery.
```

**Behind the scenes**: Agent uses `qdrant-find` to research patterns, `qdrant-store` to save solutions. You don't type these commands - the prompts make agents do it automatically.

### Session End
```
@dev_agent_session_end_prompt.md
```
Agent captures learnings, updates project context, stores successful patterns, and ensures knowledge transfers to future sessions and other team members.

## Team Collaboration

Details: [Upstream + Main Workflow](docs/setup/upstream-main-workflow.md) - Simple workflow where everyone clones the main repo, customizations go in `local/` and data goes in `.data/` (both gitignored), no merge conflicts.

**Important**: Files in `local/` are managed by agents. Manual editing can disrupt the framework's behavior and break agent context tracking. For proper agent interaction patterns, see [Agent Management](docs/agent-management/).

**Documentation**: [Setup guides](docs/setup/), [Integration help](docs/integration/)
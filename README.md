# Hish

Context management framework that gives Cursor AI agents persistent memory and cross-project knowledge through **enriched documentation and pattern taxonomy**. Instead of starting every conversation from zero, agents discover architectural patterns, design decisions, and curated learnings from all your projects.

**Two-part approach**:
1. **Enriched documentation** indexes markdown/docs into searchable patterns and knowledge
2. **Structured prompts** transform any LLM into a disciplined engineering agent

**Complements Cursor**: Cursor handles code search natively. Hish focuses on documentation patterns, file synopses, architectural decisions, and cross-project intelligence.

**Works with any model** - Claude, GPT-4, Gemini. The behavioral patterns are encoded in prompts, not dependent on model training.

## How It Works

### Indexing Your Documentation

The framework scans your repositories and creates enriched documentation knowledge:

**What gets indexed:**
- Markdown documentation and README files
- AGENTS.md file synopses (automated extraction)
- Architectural decisions and design rationale
- Project contexts and patterns
- Cross-project learnings (with approval)

**What's NOT indexed:**
- Source code (Cursor handles this natively via `codebase_search`)
- Implementation details (available through Cursor)

**Chunking strategy**: Markdown files broken into overlapping chunks with metadata (repository, file path, context).

**Vector embeddings**: Creates semantic embeddings so architectural patterns, design decisions, and learnings cluster together in vector space, discoverable through natural language queries.

### Agent Intelligence

Once indexed, your documentation becomes searchable agent memory that works through structured behavioral prompts:

```
Your Docs → Vector Index → Prompt-Guided Agent → Disciplined Output
     +                          +
 Cursor Code Search      Pattern Discovery
```

**Prompt engineering system**: Instead of hoping LLMs follow good practices, Hish embeds engineering discipline directly into agent instructions through layered prompt structures:

- **Context injection**: Agents must load project state before starting work
- **Protocol enforcement**: Specific workflows for research → implementation → quality assurance
- **Knowledge integration**: Mandatory patterns for querying existing solutions and storing new ones
- **Quality standards**: Built-in coding practices, anti-patterns, and engineering discipline

**Behavioral transformation**: Raw LLMs are unfocused and inconsistent. Hish prompts create agents that automatically query existing patterns, propose evidence-based solutions, implement with quality standards, and store results for team reuse.

**Technical architecture**: Qdrant vector database + MCP protocol bridge + automated indexing + structured prompt engineering. Standard RAG enhanced with behavioral discipline.

## Agent Personas

Hish provides two specialized agent personas, each optimized for different aspects of software development:

### 🔧 **Development Agent**
**Role**: Pattern-driven implementation and knowledge curation
- **Focus**: Pattern extraction, file synopses, architectural decisions, cross-project intelligence
- **Strengths**: Discover patterns from docs, propose evidence-based solutions, curate learnings
- **Use when**: Building features, extracting patterns, documenting decisions, cross-project learning
- **Tool separation**: Uses `qdrant-find` for docs/patterns, `codebase_search` for code

### 🛡️ **Red Team Agent**
**Role**: Security pattern analysis and vulnerability taxonomy
- **Focus**: Security patterns, vulnerability taxonomies, threat assessment, remediation guidance
- **Strengths**: Security pattern recognition, vulnerability reporting, cross-project security intelligence
- **Use when**: Security audits, vulnerability assessment, pattern-based threat analysis

**Quality Assurance**: Handled by CI/CD pipelines. Hish focuses on knowledge curation, not test execution.

**All agents share**: Cross-project intelligence, pattern taxonomy, and institutional memory capabilities.

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

# 2. Add to Cursor settings.json (builds MCP server, restart Cursor after)
make setup-cursor

# 3. Create project context
make new-context

# 4. Index your code (requires Python 3.8+)
pip install -r rag/indexer/requirements.txt
make index

# 5. Test in Cursor
# @prompts/dev_agent/dev_agent_init_prompt.md
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
@prompts/dev_agent/dev_agent_init_prompt.md
```
Agent loads project context, discovers AGENTS.md file synopses, extracts patterns from documentation, and prepares for knowledge-driven development with pattern extraction and cross-project intelligence.


### Red Team Agent Initialization
```
@prompts/red_team/red_team_agent_init_prompt.md
```
Red team agent loads security context, analyzes vulnerability landscapes, and prepares for comprehensive security analysis and threat assessment.

### Actual Usage Pattern

```
You: "I need to implement JWT authentication for this Node.js API"

Agent (with Hish):
- Automatically queries existing auth patterns from documentation
- Finds Redis blacklist pattern from ProjectA docs, refresh token design decisions from ProjectB
- Proposes solution: "I found proven JWT patterns in your documented architecture..."
- Implements code using Cursor's code search + documented patterns
- Stores new pattern in cross_project_intelligence_mpnet for team reuse (after your approval)

You: Just tell the agent what you want. It handles the knowledge discovery.
```

**Behind the scenes**: Agent uses `qdrant-find` to research documented patterns, `codebase_search` for code, `qdrant-store` to save validated learnings. You don't type these commands - the prompts make agents do it automatically.

### Session End
```
@prompts/dev_agent/dev_agent_session_end_prompt.md
```
Agent captures learnings, updates project context, stores successful patterns, and ensures knowledge transfers to future sessions and other team members.


### Red Team Session End
```
@prompts/red_team/red_team_agent_session_end_prompt.md
```
Red team agent captures security analysis achievements, vulnerability discoveries, and threat assessment learnings to ensure seamless continuity between security sessions.

## Team Collaboration

Details: [Upstream + Main Workflow](docs/setup/upstream-main-workflow.md) - Simple workflow where everyone clones the main repo, customizations go in `local/` and data goes in `.data/` (both gitignored), no merge conflicts.

**Important**: Files in `local/` are managed by agents. Manual editing can disrupt the framework's behavior and break agent context tracking. For proper agent interaction patterns, see [Agent Management](docs/agent-management/).

**Documentation**: [Setup guides](docs/setup/), [Integration help](docs/integration/), [Collection Governance](docs/collection-governance.md)

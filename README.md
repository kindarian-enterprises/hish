# 🧠 Kindarian Cursor Context

**A comprehensive framework for managing multiple development agents with shared knowledge and cross-project intelligence.**

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

Kindarian Cursor Context is a multi-project development agent framework that transforms your entire engineering ecosystem into a knowledge-powered learning machine:

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
git clone https://github.com/kindarian-enterprises/kindarian-cursor-context.git
cd kindarian-cursor-context

# Start the shared knowledge system
make quick-start

# This will:
# - Start Qdrant vector database
# - Build the MCP server
# - Show you the next steps
```

### **2. Create Your First Project Context**
```bash
# Create a new project context
./scripts/new-project-context.sh

# This creates: contexts/your-project-name/
# ├── dev_agent_persona.md      # Project-specific agent configuration
# ├── dev_agent_context.md      # Project state and history
# ├── dev_agent_init_prompt.md  # Initialization protocol
# └── project_config.yml        # Code repo paths and settings
```

### **3. Index Your Code Repositories**
```bash
# Index your project's code (stored separately from context)
make index-repo REPO_PATH=/path/to/your-project-code COLLECTION_NAME=your_project_code
make index-repo REPO_PATH=/path/to/another-project COLLECTION_NAME=another_project_code

# All projects share the same knowledge base for cross-project insights!
```

### **4. Configure Cursor MCP Integration**
```bash
# Get the exact configuration for your system
make setup-cursor

# This shows you the JSON to add to Cursor settings.json
# Or follow the detailed guide: docs/setup/cursor-mcp-integration.md
```

**Quick MCP Setup**: Add this to your Cursor `settings.json`:
```json
{
  "mcp": {
    "servers": {
      "kindarian-qdrant": {
        "command": "docker",
        "args": [
          "compose", "-f", "/absolute/path/to/kindarian-cursor-context/compose.rag.yml", 
          "run", "--rm", "-i", "mcp-qdrant-stdio"
        ],
        "env": {
          "QDRANT_URL": "http://localhost:6333",
          "COLLECTION_NAME": "default"
        }
      }
    }
  }
}
```
⚠️ **Replace `/absolute/path/to/kindarian-cursor-context/` with your actual path!**

### **5. Initialize Your Agent**
In Cursor, open the kindarian-cursor-context framework and reference your project:
```
@contexts/your-project-name/dev_agent_init_prompt.md
```

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
git clone https://github.com/kindarian-enterprises/kindarian-cursor-context.git
cd kindarian-cursor-context

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

### **📄 Core Templates**
```
contexts/              # Project-specific contexts (personas, contexts, prompts)
├── example-web-app/   # React/Node.js project context
├── example-api/       # Go microservices context
└── shared/            # Cross-project patterns and workflows
templates/             # Base templates for new projects
workflows-and-processes/ # Reusable workflows and process documentation
```

**No configuration files needed** - agents intelligently discover context and relationships

### **🔄 Workflow Templates**
```
workflows-and-processes/
├── examples/          # RAG-enhanced development workflows
└── templates/         # Testing, deployment, and process templates
```

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

**No configuration files needed** - agents intelligently discover context and relationships from directory structure and content.

The persona template lets you define:

- **Agent Identity**: Role, expertise areas, technology focus
- **Coding Standards**: Language-specific patterns, quality requirements
- **Architectural Philosophy**: Design principles, decision-making frameworks
- **Anti-Patterns**: What to avoid and why
- **RAG Integration**: Knowledge discovery and storage workflows

### **Example Persona Customization**
```markdown
## AGENT IDENTITY & ROLE
You are **MyProject Dev Agent** - a senior full-stack engineer with expertise in:
- **React/TypeScript Frontend** (Next.js, TailwindCSS, React Query)
- **Node.js Backend** (Express, PostgreSQL, Redis)
- **Cloud Infrastructure** (AWS, Docker, Kubernetes)
- **Production-Grade Development** (CI/CD, monitoring, security)

## ARCHITECTURAL PHILOSOPHY
### Reliability-First Design
- **Fault Tolerance**: Design for failure scenarios
- **Observability**: Comprehensive logging and monitoring
- **Security by Design**: Zero-trust architecture principles
```

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

## 🛠️ **Setup Workflows**

### **For New Projects**
1. Copy and customize templates
2. Set up RAG infrastructure (optional)
3. Index existing codebase and documentation
4. Train team on knowledge query patterns
5. Establish context update protocols

### **For Existing Projects**
1. Create persona based on current practices
2. Document current state in context template
3. Gradually build knowledge base from tribal knowledge
4. Integrate RAG queries into daily development
5. Store solutions as they are discovered

### **For Teams**
1. Establish shared persona standards
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

## 📈 **Benefits You'll See**

### **Immediate (Week 1)**
- **Cross-Project Discovery**: Find solutions from ANY project when working on any other
- **Zero Context Loss**: Agent remembers ALL project details across sessions
- **Institutional Memory**: Access to patterns from your entire engineering history

### **Short Term (Month 1)**
- **Accelerated Development**: Mobile apps benefit from web patterns, APIs learn from frontend
- **Quality Multiplication**: Anti-patterns discovered once prevent mistakes everywhere
- **Pattern Evolution**: Solutions improve through cross-project application and feedback

### **Long Term (Quarter 1)**  
- **Engineering Ecosystem Intelligence**: Your entire codebase becomes a learning system
- **Compound Knowledge Growth**: Each project makes ALL projects better
- **Team Velocity Multiplier**: New projects start with accumulated wisdom from all previous projects

## 🎓 **Learning Resources**

### **Essential Reading**
- **[📚 Documentation Hub](docs/README.md)** - **START HERE** - Complete navigation guide
- **[🎯 Directing Agents](docs/agent-management/directing-agents.md)** - **ESSENTIAL** - How to manage agents effectively
- **[🗂️ Knowledge Management](docs/knowledge-management/indexing-and-reindexing.md)** - When/why/how to index content
- **[🔌 Cursor MCP Integration](docs/setup/cursor-mcp-integration.md)** - Technical setup guide

### **Workflow Examples**
- [`workflows-and-processes/examples/rag-enhanced-development-workflow.md`](workflows-and-processes/examples/rag-enhanced-development-workflow.md) - Knowledge-first development process
- [`workflows-and-processes/examples/testing-workflow-template.md`](workflows-and-processes/examples/testing-workflow-template.md) - RAG-augmented testing strategies

### **Template Guides**
- [`templates/persona/dev_agent_persona_template.md`](templates/persona/dev_agent_persona_template.md) - Complete persona customization guide
- [`templates/context/dev_agent_context_template.md`](templates/context/dev_agent_context_template.md) - Context management structure and protocols

### **Multi-Project Examples**
- [`docs/examples/multi-project-workflow.md`](docs/examples/multi-project-workflow.md) - Complete day-in-the-life example of cross-project intelligence
- [`contexts/example-web-app/`](contexts/example-web-app/) - Example web application context
- [`contexts/example-api/`](contexts/example-api/) - Example API service context
- [`contexts/shared/cross_project_patterns.md`](contexts/shared/cross_project_patterns.md) - Shared knowledge patterns across all projects

## 🤝 **Contributing**

This scaffold is designed to be customized and extended. Common improvements:

- **Domain-Specific Templates**: Add templates for your industry or technology
- **Workflow Enhancements**: Create new process templates based on your experience  
- **Integration Patterns**: Develop connections to your specific tools and systems
- **Knowledge Patterns**: Share effective RAG query patterns that work for your domain

## 🛟 **Support and Community**

### **Getting Help**
- Review the documentation in `docs/` for comprehensive guides
- Check workflow examples for practical implementation patterns
- Use the knowledge system to learn from similar implementations

### **Best Practices**
- **Start Small**: Begin with core templates and basic context management
- **Build Habits**: Make knowledge queries and storage part of daily workflow
- **Measure Impact**: Track time savings and quality improvements
- **Share Learnings**: Contribute successful patterns back to knowledge base

## 🔮 **What Makes This Different**

Unlike static documentation or one-off prompts, Kindarian Cursor Context provides:

- **Persistent Learning**: Knowledge accumulates across all sessions and projects
- **Pattern Evolution**: Solutions improve based on real-world validation
- **Cross-Project Insights**: Learn from the entire organizational codebase
- **Institutional Memory**: Preserve knowledge beyond individual developers
- **Proactive Guidance**: Discover relevant patterns before problems occur

---

**Transform your development workflow from reactive problem-solving to proactive, knowledge-driven engineering.**

*Start with the templates, add your context, query for patterns, store your solutions, and watch your development velocity accelerate while quality improves.*

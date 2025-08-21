# Agent Workflows

## Overview

This document describes common workflows for managing development agents within the Kindarian Cursor Context framework.

## Creating a New Project Context

### 1. Run the Setup Script
```bash
./scripts/new-project-context.sh
```

### 2. Customize the Context
The script creates a project context in `local/your-project-name/` with:
- `dev_agent_context.md` - Project state and history
- `README.md` - Project documentation

**Note**: The following files are now universal and shared across all projects:
- **`dev_agent_persona.md`** - Universal dev agent persona (top-level)
- **`dev_agent_init_prompt.md`** - Universal initialization protocol (top-level)
- **`dev_agent_session_end_prompt.md`** - Universal session end protocol (top-level)

### 3. Edit Project-Specific Details
Edit the context files to reflect your project's specific needs, technology stack, and current state.

## Managing Multiple Projects

### Context Organization
- **Local Contexts**: `local/` directory (gitignored) for your project contexts
- **Shared Contexts**: `contexts/` directory (tracked) for framework examples and patterns

### Cross-Project Knowledge
- All project contexts are automatically indexed for knowledge discovery
- Use `qdrant-find` to discover patterns from other projects
- Use `qdrant-store` to contribute solutions back to the knowledge base

## Agent Initialization

### In Cursor
Reference the universal init prompt:
```
@dev_agent_init_prompt.md
```

### Agent Behavior
- The agent will read the universal persona from `dev_agent_persona.md`
- Project-specific context is loaded from `local/your-project-name/dev_agent_context.md`
- The agent operates with both universal intelligence and project-specific knowledge

## Knowledge Management

### Storing Solutions
```bash
qdrant-store "Solution: [description] - Context: [when this applies] - Implementation: [approach] - Performance: [metrics]"
```

### Finding Patterns
```bash
qdrant-find "authentication patterns across projects"
qdrant-find "testing strategies for [project type]"
qdrant-find "performance optimization approaches"
```

## Workflow Integration

### Daily Development
1. Initialize agent with project context
2. Query knowledge base before implementing new features
3. Store successful solutions for future projects
4. Update project context with achievements and lessons learned

### Team Collaboration
1. Share knowledge through the centralized knowledge base
2. Learn from patterns discovered by other team members
3. Contribute solutions that benefit the entire organization
4. Maintain consistent quality standards across all projects

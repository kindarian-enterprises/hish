# Agent Workflows

## Overview

This document describes common workflows for managing development agents within the Hish framework.

## Creating a New Project Context

### 1. Create Project Context
```bash
make new-context
```

### 2. Customize the Context
The script creates a project context in `local/your-project-name/` with:
- `dev_agent_context.md` - Project state and history
- `README.md` - Project documentation

**Note**: The following files are now universal and shared across all projects:
- **`dev_agent_persona.md`** - Universal dev agent persona (top-level)
- **`prompts/dev_agent/dev_agent_init_prompt.md`** - Universal initialization protocol
- **`prompts/dev_agent/dev_agent_session_end_prompt.md`** - Universal session end protocol
- **`prompts/qa/qa_agent_init_prompt.md`** - QA agent initialization protocol
- **`prompts/qa/qa_agent_session_end_prompt.md`** - QA agent session end protocol
- **`prompts/red_team/red_team_agent_init_prompt.md`** - Red team agent initialization protocol
- **`prompts/red_team/red_team_agent_session_end_prompt.md`** - Red team agent session end protocol

### 3. Let Agents Manage Context
**Important**: Context files in `local/` are managed by agents. Direct editing can disrupt framework behavior. Instead, use agent workflows to update project context through proper protocols.

## Managing Multiple Projects

### Context Organization
- **Local Contexts**: `local/` directory (gitignored) for your project contexts
- **Shared Contexts**: `contexts/` directory (tracked) for framework examples and patterns

### Cross-Project Knowledge
- All project contexts are automatically indexed for knowledge discovery
- Agents automatically discover patterns from other projects when you ask
- Agents automatically store solutions in the knowledge base for future reference

## Agent Initialization

### Development Agent
Reference the universal init prompt:
```
@prompts/dev_agent/dev_agent_init_prompt.md
```

### QA Agent
Reference the QA agent init prompt:
```
@prompts/qa/qa_agent_init_prompt.md
```

### Red Team Agent
Reference the red team agent init prompt:
```
@prompts/red_team/red_team_agent_init_prompt.md
```

### Agent Behavior
- **Dev Agent**: Reads universal persona, loads project context, implements solutions
- **QA Agent**: Reads QA persona, analyzes quality standards, generates reports
- **Red Team Agent**: Reads red team persona, analyzes security vulnerabilities, generates security reports
- Project-specific context is loaded from `local/your-project-name/dev_agent_context.md`
- All agents operate with universal intelligence and project-specific knowledge

## Knowledge Management

### Storing Solutions
Ask agents to store solutions in the knowledge base:
```
"Please store this JWT implementation for future reference, including the Redis blacklist approach and performance characteristics."
```

### Finding Patterns
Ask agents to research existing patterns:
```
"Research authentication patterns across our projects before we implement this new service."
"What testing strategies have worked well for similar components?"
```

**Behind the scenes**: Agents use `qdrant-store` and `qdrant-find` automatically. You don't need to run these commands manually.

## Daily Development Examples

### Starting a New Feature
```
You: "I need to add user authentication to this React app"

Agent: "I found JWT implementations across your projects. Your API backend uses
Express with Redis token blacklisting, and your mobile app has a useAuth hook
with automatic refresh. Should I adapt these patterns for React?"

You: "Yes, use the useAuth hook approach but integrate with our Express backend"

Agent: [Implements solution] "I've created the useAuth hook and integrated it
with your existing JWT backend. I'll store this React+Express auth pattern
for future projects."
```

### Debugging Issues
```
You: "The API is returning 500 errors intermittently"

Agent: "I found similar debugging workflows from your other services. Let me check
error patterns... I see you've used structured logging and APM tooling before.
Should I add the same monitoring setup here?"

You: "Good idea, and check if we've seen this specific error pattern before"

Agent: "Found it! ProjectB had identical symptoms - Redis connection pooling issue.
Here's the fix that worked..."
```

### Code Review and Quality
```
You: "Review this authentication middleware for security issues"

Agent: "Comparing against your security patterns from other projects... I notice
this is missing rate limiting that you implemented in ProjectA, and the token
validation differs from your proven approach in ProjectC. Here are the specific
improvements..."

You: "Apply those security patterns and document the rationale"

Agent: [Makes improvements] "Applied security patterns and stored this
middleware template for future authentication implementations."
```

### Architecture Decisions
```
You: "Should we use GraphQL or REST for this new service?"

Agent: "Analyzing your past decisions... ProjectA used GraphQL for complex
data fetching and saw 40% fewer API calls. ProjectB used REST for simple
CRUD and had faster development time. Based on your current requirements..."

You: "What were the specific trade-offs we documented?"

Agent: "Here's what you learned: GraphQL better for frontend teams with complex
queries, REST better for simple APIs with caching. Your current service looks
more like ProjectB's use case..."
```

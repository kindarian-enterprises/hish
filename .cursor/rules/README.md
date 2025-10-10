# HISH Cursor Rules

**Status**: Currently unused

## Background

Cursor Rules (`.mdc` files) were explored for routing between dual MCP servers (qdrant-mpnet and qdrant-jina). However, this approach was abandoned in favor of a **simplified single-server architecture**.

## Architectural Decision

**Decision**: Use Cursor's native `codebase_search` for code, Hish for documentation
**Rationale**:
1. Cursor's code search is already excellent - don't duplicate it
2. Single MCP server (unified) is simpler and faster
3. Clear separation of concerns: Hish = docs/patterns, Cursor = code
4. Hooks provide sufficient agent guidance without rules

## Current Architecture

```
Hish (qdrant-find):
  └─ hish_framework_mpnet (framework docs)
  └─ cross_project_intelligence_mpnet (patterns)
  └─ {project}_docs_mpnet (project documentation)

Cursor Native (codebase_search):
  └─ Code symbols, implementations, imports
```

## Agent Guidance Mechanism

Instead of rules, we use:
1. **`prioritize_local_data` hook** - Injects collection guidance into every prompt
2. **Agent personas** - Define tool usage strategy in `templates/dev_agent_persona.md`
3. **Init prompts** - Explicit examples in `prompts/dev_agent/dev_agent_init_prompt.md`

## Future Use

This directory is retained for potential future Cursor Rules if needed. Any `.mdc` files placed here will be automatically loaded by Cursor (no installation required).

**Cursor Rules Documentation**: https://cursor.com/docs/agent/rules

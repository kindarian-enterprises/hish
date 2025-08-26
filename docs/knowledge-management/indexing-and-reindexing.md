# Knowledge Indexing Guide

When to index and reindex your code for optimal agent intelligence.

## When to Index

**Initial setup:**
```bash
make index
```

Indexes framework docs, project contexts, and all discovered code repositories.

**How discovery works:** Project contexts in `local/` contain repository paths. `make index` finds and indexes all of them automatically.

## When to Reindex

**Regular reindexing (weekly/bi-weekly):**
- After major code changes
- When agents seem to miss recent solutions
- After significant refactoring

**Event-driven reindexing:**
- New project added
- Major feature implementation
- Architecture changes

## Indexing Commands

**Setup once:**
```bash
pip install -r rag/indexer/requirements.txt
```

**Regular use:**
```bash
make index-framework  # Quick framework updates
make index           # Full reindexing (all projects)
```

**Manual project indexing:**
```bash
make index-repo REPO_PATH=/path/to/code COLLECTION_NAME=project_code
```

**Collections created automatically:**
- `hish_framework` - Framework docs and contexts
- `cross_project_intelligence` - Patterns and observations  
- `{project}_code` - Source code from specific projects

## Workflows

**New project:**
```bash
make new-context  # Creates context, asks for repo path
make index        # Indexes everything
```

**Weekly maintenance:**
```bash
make index        # Updates all knowledge
```

**Quick framework updates:**
```bash
make index-framework  # Just docs and contexts
```

## Health Check

**Check status:**
```bash
make collections  # View all collections
make health      # Check framework status
```

**Agents missing recent solutions?** → Run `make index`

**Indexing fails?** → Check Cursor MCP connection and restart if needed

That's it! The framework handles complexity automatically - just run `make index` when you want agents to know about recent changes.



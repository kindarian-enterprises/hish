# Knowledge Indexing Guide

When and how to index your code so agents can access current information.

## When to Index

**Initial setup:**
```bash
make index
```

Indexes framework docs, project contexts, and all discovered code repositories.

**How discovery works:** Project contexts in `local/` contain repository paths. `make index` finds and indexes all of them automatically.

## When to Reindex

**Regular reindexing:**
- After major code changes
- When you want agents to know about recent work
- After significant refactoring
- Weekly or bi-weekly maintenance

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

**Reindex specific projects:**
```bash
./reindex shire                    # Single project
./reindex shire platform-backend  # Multiple projects
./reindex all                      # All projects (same as make index)
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

**Agents not finding recent code?** → Run `make index`

**Indexing fails?** → Check Cursor MCP connection and restart if needed

The framework handles complexity automatically - just run `make index` when you want agents to access recent changes.



# Knowledge Indexing Guide

When and how to index your code so agents can access current information.

## ⚠️ **IMPORTANT: Indexing Behavior**

**Code Collections (Project Repositories):**
- **DESTRUCTIVE**: `make index` and `./reindex` will **DROP and RECREATE** code collections
- **All existing code chunks are lost** when reindexing
- **Use when**: You want fresh, current code information
- **Avoid when**: You need to preserve historical code knowledge

**Framework Collections (Preserved):**
- **NON-DESTRUCTIVE**: Framework documentation and cross-project intelligence are **PRESERVED**
- **Existing knowledge patterns remain intact**
- **Use when**: You want to update framework docs without losing intelligence

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

**⚠️ WARNING**: Reindexing **DESTROYS** existing code knowledge. Only reindex when you need fresh code information.

## Indexing Commands

**Setup once:**
```bash
pip install -r rag/indexer/requirements.txt
```

**Regular use with optimal embeddings:**
```bash
make index-framework  # Framework docs only (BGE-small, PRESERVES data)
make index-code      # Code repositories only (Jina Code, DESTROYS code)
make index           # Full reindexing (BGE + Jina Code, DESTROYS code, PRESERVES framework)
```

**Reindex specific projects:**
```bash
./reindex shire                    # Single project (Jina Code, DESTROYS project code)
./reindex shire platform-backend  # Multiple projects (Jina Code, DESTROYS project code)
./reindex all                      # All projects (Jina Code, DESTROYS all code, PRESERVES framework)
```

**Manual project indexing with auto-detection:**
```bash
make index-repo REPO_PATH=/path/to/code COLLECTION_NAME=project_code  # Auto-detects Jina Code for code
make index-repo REPO_PATH=. COLLECTION_NAME=hish_framework           # Auto-detects BGE for framework
```

**Collections created automatically:**
- `hish_framework` - Framework docs and contexts (**PRESERVED**)
- `cross_project_intelligence` - Patterns and observations (**PRESERVED**)
- `{project}_code` - Source code from specific projects (**DESTROYED on reindex**)

## Workflows

**New project:**
```bash
make new-context  # Creates context, asks for repo path
make index        # Indexes everything (DESTROYS existing code, PRESERVES framework)
```

**Weekly maintenance:**
```bash
make index        # Updates all knowledge (DESTROYS code, PRESERVES framework)
```

**Quick framework updates:**
```bash
make index-framework  # Just docs and contexts (PRESERVES all data)
```

**Code-only updates:**
```bash
./reindex project-name  # Updates specific project code (DESTROYS project code only)
```

## Health Check

**Check status:**
```bash
make collections  # View all collections
make health      # Check framework status
```

**Agents not finding recent code?** → Run `make index` (⚠️ **DESTROYS existing code**)

**Indexing fails?** → Check Cursor MCP connection and restart if needed

## ⚠️ **Data Loss Prevention**

**Before reindexing code:**
1. **Verify you need fresh code information**
2. **Ensure important code knowledge is stored in framework collections**
3. **Consider using `make index-framework` for framework-only updates**

**Framework collections are safe:**
- `hish_framework` - Your documentation and guides
- `cross_project_intelligence` - Patterns and learnings across projects

**Code collections are volatile:**
- `{project}_code` - Recreated on every reindex
- Contains only current code state, not historical knowledge

---

The framework handles complexity automatically - just run `make index` when you want agents to access recent changes. **Remember: Code reindexing is destructive, framework indexing is safe.**

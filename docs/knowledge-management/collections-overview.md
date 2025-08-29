# Knowledge Collections Overview

How the framework organizes knowledge for agents.

## What Are Collections?

Collections are organized knowledge storage that agents search automatically. You don't interact with them directly - agents handle all the searching and storage.

## Collection Types

**Framework documentation** (`hish_framework`)
- Hish documentation and guides
- Project context files from `local/` directories  
- Official templates and workflows
- **PRESERVED**: Never destroyed during reindexing

**Cross-project intelligence** (`cross_project_intelligence`)
- Patterns agents discover across your projects
- Relationships between different codebases
- Effectiveness data from implemented solutions
- **PRESERVED**: Never destroyed during reindexing

**Project code** (`projectname_code`)
- Source code from specific repositories
- One collection per project for focused search
- Created automatically when you run `make index`
- **VOLATILE**: Destroyed and recreated on every reindex

## How It Works

**When you index:** `make index` creates collections from your code and documentation

**When agents search:** They automatically query relevant collections based on your questions

**When agents store:** They save successful solutions and patterns for future reference

**You don't need to manage collections directly** - the framework handles organization automatically.

## ⚠️ **Important: Data Preservation**

**Collections that are PRESERVED:**
- `hish_framework` - Your documentation and guides
- `cross_project_intelligence` - Patterns and learnings across projects

**Collections that are DESTROYED on reindex:**
- `{project}_code` - Source code from repositories
- These are recreated fresh each time

**Why this design:**
- **Framework knowledge** builds up over time and should be preserved
- **Code knowledge** should always be current and accurate
- **Fresh code indexing** ensures agents have the latest implementation details

## Checking Status

**View available collections:**
```bash
make collections
```

**Check framework health:**
```bash
make health
```

## Data Management Strategy

**For persistent knowledge:**
- Store important patterns in `cross_project_intelligence`
- Document solutions in framework collections
- Use `make index-framework` for safe updates

**For current code:**
- Use `make index` when you need fresh code information
- Accept that code collections will be recreated
- Focus on current implementation, not historical code

---

That's it! The system handles knowledge organization automatically while you focus on development. **Remember: Framework knowledge is preserved, code knowledge is always fresh.**

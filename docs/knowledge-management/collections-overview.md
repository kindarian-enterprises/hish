# Knowledge Collections Overview

How the framework organizes knowledge for agents.

## What Are Collections?

Collections are organized knowledge storage that agents search automatically. You don't interact with them directly - agents handle all the searching and storage.

## Collection Types

**Framework documentation** (`hish_framework`)
- Hish documentation and guides
- Project context files from `local/` directories  
- Official templates and workflows

**Cross-project intelligence** (`cross_project_intelligence`)
- Patterns agents discover across your projects
- Relationships between different codebases
- Effectiveness data from implemented solutions

**Project code** (`projectname_code`)
- Source code from specific repositories
- One collection per project for focused search
- Created automatically when you run `make index`

## How It Works

**When you index:** `make index` creates collections from your code and documentation

**When agents search:** They automatically query relevant collections based on your questions

**When agents store:** They save successful solutions and patterns for future reference

**You don't need to manage collections directly** - the framework handles organization automatically.

## Checking Status

**View available collections:**
```bash
make collections
```

**Check framework health:**
```bash
make health
```

That's it! The system handles knowledge organization automatically while you focus on development.

# SBMI Expansion Protocol (L1→L2→L3)

**Version:** 1.0
**Date:** 2025-12-09
**Status:** Phase 1 Complete

---

## Overview

The SBMI expansion protocol defines how agents navigate from compressed indexes (L1) to targeted content (L2) to full files (L3) using semantic search and depth budgets.

**Key Principle:** Load minimal pointers, expand exactly what's needed based on depth.

---

## Layer Definitions

### L0: Symbol Dictionary (Root - Future)
**File:** `local/workflow-indexes/symbol-dict.compact` (not yet implemented)
**Purpose:** Master symbol-to-entity mappings for symbolic compression
**Load:** Once per session initialization
**Status:** Phase 2+ (optional enhancement)

### L1: Compressed Indexes (Navigation Layer)
**Files:**
- `framework-command-index.compact` (~1.5k tokens, 28% reduction)
- `framework-file-index.compact` (~2.0k tokens, 6% reduction)
- `framework-repository-index.compact` (~2.0k tokens, 6% reduction)
- `session-workflow-enforcement.compact` (~1.4k tokens, 8% reduction)

**Purpose:** Lightweight navigation pointers
**Load:** During session initialization
**Cost:** ~7k tokens total (vs ~8.7k original)

**Content:**
- Command names only (descriptions removed)
- File paths and line ranges
- Repository structure
- Workflow rules (compact)

**Example:**
```
### Context mgmt
newctx
make list-ctx
./reindex context1 context2
```

### L2: Targeted Sections (Medium Cost)
**Method:** Semantic search via `codebase_search`
**Source:** Original uncompressed files
**Cost:** 300-800 tokens per expansion

**When to use:**
- Need details about a specific command
- Want to understand a file's purpose
- Seeking specific workflow guidance

**How to expand:**
```
Agent sees in L1: "make index"
Agent needs details → semantic search original file
codebase_search("make index command details", "framework-command-index.md")
→ Returns targeted section (500 tokens)
```

### L3: Full Content (Heavy Cost)
**Method:** Complete file read via `read_file`
**Source:** Original uncompressed files
**Cost:** Unbounded (entire file)

**When to use:**
- Comprehensive understanding required
- Multiple sections needed
- Architecture exploration

**How to expand:**
```
Agent needs complete context →
read_file("framework-command-index.md")
→ Returns full file (2.5k tokens)
```

---

## Expansion Strategies

### Strategy 1: Index-Only Navigation (L1)
**Use Case:** Quick command lookup, simple tasks
**Pattern:** Reference compressed index directly

```
User: "What command creates a new context?"
Agent: *Checks framework-command-index.compact*
       "make new-context or use the shorthand: newctx"
Cost: 0 additional tokens (already loaded)
```

### Strategy 2: Targeted Expansion (L1→L2)
**Use Case:** Need specific details, moderate exploration
**Pattern:** Index identifies topic → semantic search original

```
User: "How do I index a specific repository?"
Agent: *Sees "make index-repo" in L1 compact index*
       *Needs details → expands to L2*
       codebase_search("index-repo repository indexing", "framework-command-index.md")
       → Gets: "make index-repo REPO_PATH=/path COLLECTION_NAME=name"
Cost: ~500 tokens (targeted section)
```

### Strategy 3: Comprehensive Study (L1→L2→L3)
**Use Case:** Architecture understanding, debugging, learning
**Pattern:** Index → targeted sections → full context

```
User: "Explain the complete indexing workflow"
Agent: *Checks L1: multiple index commands*
       *Expands L2: specific sections for each*
       codebase_search("knowledge management indexing", "framework-command-index.md")
       codebase_search("collection setup", "framework-repository-index.md")
       *Still needs context → expands to L3*
       read_file("rag/indexer/app.py")
Cost: ~1k (L2 searches) + ~3k (L3 file) = 4k tokens
```

### Strategy 4: Full Load (L3 Direct)
**Use Case:** Behavioral prompts, critical files
**Pattern:** Always load complete, never compress

```
User: "Initialize dev agent"
Agent: *Loads L3 directly (no compression)*
       read_file("prompts/dev_agent/dev_agent_init_prompt.md")
       read_file("templates/dev_agent_persona.md")
Cost: Full file tokens (no shortcuts - quality critical)
```

---

## Expansion Decision Tree

```
┌─────────────────────────────────────────┐
│  Agent encounters need for information  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │ Check L1 Index  │
         └────────┬────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
   ┌─────────┐         ┌─────────┐
   │ Found   │         │ Not in  │
   │ Answer  │         │ Index   │
   └────┬────┘         └────┬────┘
        │                   │
        ▼                   ▼
   ┌─────────┐         ┌──────────────┐
   │ Return  │         │ Full semantic│
   │ L1 info │         │ search needed│
   └─────────┘         └──────────────┘
        ▲
        │
        ▼
   Simple answer
   sufficient?
        │
    ┌───┴───┐
    │       │
   Yes     No
    │       │
    │       ▼
    │  ┌─────────────┐
    │  │ Need details│
    │  └──────┬──────┘
    │         │
    │         ▼
    │  Is it a behavioral
    │  file (persona/init)?
    │         │
    │    ┌────┴────┐
    │   Yes       No
    │    │         │
    │    ▼         ▼
    │  ┌─────┐  ┌──────┐
    │  │ L3  │  │  L2  │
    │  │Full │  │Trgted│
    │  └─────┘  └───┬──┘
    │              │
    │              ▼
    │         Sufficient?
    │              │
    │         ┌────┴────┐
    │        Yes       No
    │         │         │
    │         ▼         ▼
    │      Done      ┌─────┐
    │                │ L3  │
    │                │Full │
    │                └─────┘
    │
    └──────────────────────┘
```

---

## File-Specific Expansion Rules

### Workflow Indexes (Use Compressed L1)
**Files:**
- `framework-command-index.md` → `.compact`
- `framework-file-index.md` → `.compact`
- `framework-repository-index.md` → `.compact`
- `session-workflow-enforcement.md` → `.compact`

**Access Pattern:**
1. **L1**: Load compressed version (session init)
2. **L2**: Semantic search original if details needed
3. **L3**: Full read only for comprehensive study

### Behavioral Prompts (Always L3 Full)
**Files:**
- `prompts/dev_agent/dev_agent_init_prompt.md`
- `templates/dev_agent_persona.md`
- `prompts/dev_agent/dev_agent_session_end_prompt.md`
- All persona and initialization files

**Access Pattern:**
1. **L3 ONLY**: Always full read, never compressed
2. No L1/L2 shortcuts - quality critical

### Code Files (L2→L3)
**Files:**
- `rag/indexer/app.py`
- `Makefile`
- Project source files

**Access Pattern:**
1. **L2**: Semantic search for specific functions/sections
2. **L3**: Full read if comprehensive understanding needed

### Config Files (L2 Direct)
**Files:**
- `config/env.mpnet`
- `config/sbmi-compression.yaml`
- Small config files (<100 lines)

**Access Pattern:**
1. **L2 Direct**: Just read the file (small, low cost)
2. No index needed - files are already compact

---

## Semantic Search Patterns (L2 Expansion)

### For Commands
```
# Pattern: "command-name command details"
codebase_search("make index command details", "framework-command-index.md")
codebase_search("new-context creation workflow", "framework-command-index.md")
```

### For Files
```
# Pattern: "file-purpose context understanding"
codebase_search("Makefile knowledge management", "framework-file-index.md")
codebase_search("app.py indexing logic", "framework-file-index.md")
```

### For Concepts
```
# Pattern: "concept-name architecture patterns"
codebase_search("collection management patterns", "framework-repository-index.md")
codebase_search("cross-project intelligence setup", "framework-repository-index.md")
```

### For Workflows
```
# Pattern: "workflow-name enforcement rules"
codebase_search("command execution rules", "session-workflow-enforcement.md")
codebase_search("multi-collection query protocol", "session-workflow-enforcement.md")
```

---

## Cost Analysis

### Baseline (No Compression)
```
Session Init Load:
- framework-command-index.md: 2.5k tokens
- framework-file-index.md: 2.2k tokens
- framework-repository-index.md: 2.4k tokens
- session-workflow-enforcement.md: 1.6k tokens
Total: 8.7k tokens loaded upfront
```

### With SBMI L1 Compression
```
Session Init Load:
- framework-command-index.compact: 1.8k tokens (28% reduction)
- framework-file-index.compact: 2.1k tokens (6% reduction)
- framework-repository-index.compact: 2.3k tokens (6% reduction)
- session-workflow-enforcement.compact: 1.5k tokens (8% reduction)
Total: 7.7k tokens loaded upfront

Savings: ~1k tokens (12% reduction)
```

### Expansion Costs
```
L2 Targeted Expansion (semantic search):
- Average: 500 tokens per search
- Max per query: 3 expansions (standard mode)
- Total L2 budget: 1.5k tokens per query

L3 Full File Read:
- Small files (<100L): 200-500 tokens
- Medium files (100-300L): 500-1.5k tokens
- Large files (>300L): 1.5k-5k tokens
```

### Session Total Examples
```
Quick Session (L1 only):
  Load: 7.7k tokens
  Work: 0k tokens (answers from L1)
  Total: 7.7k tokens

Standard Session (L1 + L2):
  Load: 7.7k tokens
  L2 expansions: 1.5k tokens (3 searches)
  Total: 9.2k tokens

Deep Session (L1 + L2 + L3):
  Load: 7.7k tokens
  L2 expansions: 1.5k tokens
  L3 reads: 3k tokens (2 full files)
  Total: 12.2k tokens
```

---

## Implementation Guidance

### For Agent Initialization
```python
# Conceptual - not actual code
def initialize_agent():
    # Load compressed indexes (L1)
    load("framework-command-index.compact")
    load("framework-file-index.compact")
    load("framework-repository-index.compact")
    load("session-workflow-enforcement.compact")

    # Load behavioral prompts (L3 - always full)
    load("prompts/dev_agent/dev_agent_init_prompt.md")  # Full
    load("templates/dev_agent_persona.md")  # Full

    # Ready with ~10k tokens loaded (vs ~11k without compression)
```

### For Query Processing
```python
# Conceptual
def answer_query(query):
    # Check L1 compressed indexes first
    l1_answer = check_compressed_indexes(query)
    if l1_answer.is_sufficient():
        return l1_answer

    # Need details - expand to L2
    l2_sections = semantic_search_original_files(query, limit=3)
    if l2_sections.is_sufficient():
        return l2_sections

    # Still need more - expand to L3
    l3_full_files = read_full_files(relevant_files)
    return l3_full_files
```

### For Behavioral File Access
```python
# Conceptual
def load_behavioral_file(filepath):
    # NEVER use compressed version
    # ALWAYS full read (L3)
    if is_behavioral_file(filepath):
        return read_file(filepath)  # Full content
    else:
        # Navigation files can use L1→L2→L3 progression
        return smart_load(filepath)
```

---

## Best Practices

### ✅ DO
- Load compressed indexes (L1) at session init
- Use semantic search (L2) for targeted details
- Always load behavioral prompts in full (L3)
- Cache L2 expansions within session
- Start with L1, expand only when needed

### ❌ DON'T
- Compress behavioral prompts or persona files
- Skip L1 and go straight to L3 for navigation
- Expand everything upfront "just in case"
- Use compressed versions of critical files
- Assume L1 has all details (it's navigation only)

---

## Future Enhancements (Phase 2+)

### Depth Budget System
**Modes:**
- Quick: L1 only (7.7k tokens)
- Standard: L1 + 3xL2 (9.2k tokens)
- Deep: L1 + L2 + 2xL3 (12.2k tokens)
- Massive: Unrestricted

### Symbolic Compression (L0)
**Optional enhancement:**
- Symbol dictionary for ultra-compact indexes
- Requires Phase 0 tokenization validation
- Target: 70-80% reduction (vs current 12%)

### Hot Path Pre-Loading
**Optimization:**
- Identify common expansion patterns
- Pre-bundle frequently co-expanded sections
- Reduce cold-start expansion costs

---

## Examples

### Example 1: Quick Command Lookup
```
User: "How do I list all contexts?"

Agent process:
1. Check framework-command-index.compact (L1)
2. Find: "make list-ctx"
3. Return answer
4. Cost: 0 additional tokens (already loaded)
```

### Example 2: Command with Details
```
User: "How do I index a specific repository with custom collection name?"

Agent process:
1. Check framework-command-index.compact (L1)
2. Find: "make index-repo" but need syntax details
3. Expand to L2:
   codebase_search("index-repo repository custom collection", "framework-command-index.md")
4. Get: "make index-repo REPO_PATH=/path COLLECTION_NAME=name"
5. Return detailed command
6. Cost: ~500 tokens (L2 expansion)
```

### Example 3: Comprehensive Workflow
```
User: "Explain the complete framework setup process"

Agent process:
1. Check session-workflow-enforcement.compact (L1)
2. Find: References to setup flow
3. Expand to L2:
   codebase_search("setup workflow initialization", "framework-command-index.md")
   codebase_search("setup workflow", "session-workflow-enforcement.md")
4. Still need comprehensive context
5. Expand to L3:
   read_file("framework-command-index.md")
   read_file("docs/setup/getting-started.md")
6. Return comprehensive guide
7. Cost: ~1k (L2) + ~4k (L3) = 5k tokens
```

### Example 4: Behavioral Prompt (No Compression)
```
User: "Initialize dev agent"

Agent process:
1. Load behavioral prompts (L3 direct - no L1/L2)
   read_file("prompts/dev_agent/dev_agent_init_prompt.md")  # Full
   read_file("templates/dev_agent_persona.md")  # Full
2. Execute initialization protocol
3. Cost: Full file tokens (quality critical)
```

---

## Validation Checklist

Before expanding to L2/L3, ask:
- [ ] Is L1 compressed index insufficient?
- [ ] Is this a navigation file (not behavioral)?
- [ ] Will targeted search (L2) suffice?
- [ ] Or do I need full context (L3)?
- [ ] Have I cached this expansion already?

---

## Related Documentation

- **Design:** `local/symbolic-budget-index-system-design.md`
- **Config:** `config/sbmi-compression.yaml`
- **Exclusions:** `local/workflow-indexes/compression-exclusion-rules.md`
- **Package:** `sbmi/README.md`
- **Tests:** `sbmi/tests/`

---

**Version History:**
- 1.0 (2025-12-09): Initial expansion protocol documentation
- Phase 1 complete - ready for Phase 2 depth budget implementation

# SBMI Depth Budgets Reference

**Version:** 2.0
**Date:** 2025-12-09
**Status:** Phase 2 - Depth Budget System

---

## Overview

Depth-based token budget management for SBMI expansion, defining how agents navigate the L0→L1→L2→L3 hierarchy based on task complexity and session mode.

**Core Concept:** Expansion depth is tracked as a graph, not a counter. Each layer costs differently, and agents must choose the minimal expansion path to answer queries while staying within mode budgets.

---

## Depth Modes

### Quick Mode (Lightweight)
**Target:** Simple queries, fast responses
**Budget:** L1 only
**Typical Session:** Command lookups, file path queries

**Load Strategy:**
- L1 compressed indexes: Loaded upfront
- L2 expansions: None (fallback to prompt)
- L3 full reads: Behavioral files only

**Token Consumption:**
```
Session Init: ~8k tokens (L1 indexes + behavioral prompts)
Per Query: 0k (answer from loaded L1)
Total Budget: ~8k tokens
```

**Use Cases:**
- "What command lists contexts?"
- "Where is the Makefile?"
- "Quick reference lookup"

**Limitations:**
- No detailed explanations
- Cannot answer "how" or "why" questions requiring context
- Falls back to elevation prompt if insufficient

---

### Standard Mode (Balanced)
**Target:** Moderate complexity, most common sessions
**Budget:** L1 + up to 3 L2 expansions
**Typical Session:** Command usage details, file purpose queries

**Load Strategy:**
- L1 compressed indexes: Loaded upfront
- L2 expansions: Up to 3 semantic searches
- L3 full reads: Behavioral files + 1 targeted file if needed

**Token Consumption:**
```
Session Init: ~8k tokens (L1 indexes + behavioral prompts)
L2 Expansions: ~500 tokens each × 3 = 1.5k tokens
L3 Targeted: ~1k tokens (if needed)
Total Budget: ~10.5k tokens
```

**Use Cases:**
- "How do I index a specific repository?"
- "What does make setup-framework do?"
- "Explain the session workflow enforcement rules"

**Limitations:**
- Limited to 3 semantic searches
- One full file read maximum (excluding behavioral)
- Falls back to elevation if needs comprehensive study

---

### Deep Mode (Comprehensive)
**Target:** Complex tasks, architecture understanding
**Budget:** L1 + unlimited L2 + up to 5 L3 full reads
**Typical Session:** Design understanding, debugging, implementation planning

**Load Strategy:**
- L1 compressed indexes: Loaded upfront
- L2 expansions: Unlimited semantic searches
- L3 full reads: Behavioral files + up to 5 additional files

**Token Consumption:**
```
Session Init: ~8k tokens (L1 indexes + behavioral prompts)
L2 Expansions: Unlimited (~3-6k typical)
L3 Full Reads: ~1.5k tokens each × 5 = 7.5k tokens
Total Budget: ~18.5k tokens (typical)
```

**Use Cases:**
- "Explain the complete RAG indexing architecture"
- "How does the SBMI compilation pipeline work end-to-end?"
- "Debug why make index-framework fails"

**Limitations:**
- Max 5 full file reads (excluding behavioral)
- Must use semantic search (L2) to narrow scope before L3
- Falls back to Massive if needs more files

---

### Massive Mode (Unrestricted)
**Target:** Comprehensive system understanding, major refactoring
**Budget:** Unrestricted
**Typical Session:** Full codebase exploration, architecture redesign

**Load Strategy:**
- L1 compressed indexes: Loaded upfront
- L2 expansions: Unlimited
- L3 full reads: Unlimited

**Token Consumption:**
```
Session Init: ~8k tokens (L1 indexes + behavioral prompts)
L2 Expansions: Unlimited (as needed)
L3 Full Reads: Unlimited (as needed)
Total Budget: No limit (context window is the constraint)
```

**Use Cases:**
- "Refactor the entire SBMI package"
- "Understand all integration points between RAG and MCP"
- "Implement a new major feature across multiple files"

**Limitations:**
- Context window size (1M tokens for most models)
- Performance degradation with excessive context
- Should still prefer L2→L3 progression for efficiency

---

## Expansion Cost Tracking

### Layer Costs
```
L0 (Symbol Dict): 0 tokens (future: ~200 tokens if implemented)
L1 (Compressed Indexes): Pre-loaded (~8k session init)
L2 (Semantic Search): ~300-800 tokens per expansion
L3 (Full File): Variable by file size
  - Small (<100L): 200-500 tokens
  - Medium (100-300L): 500-1.5k tokens
  - Large (>300L): 1.5k-5k tokens
```

### Graph Tracking
Agents must track expansion as a **directed graph**, not a simple counter:

```
Session Start (Quick Mode)
│
├── L1: framework-command-index.compact (loaded)
├── L1: framework-file-index.compact (loaded)
├── L1: framework-repository-index.compact (loaded)
├── L1: session-workflow-enforcement.compact (loaded)
│
└── Query: "How do I index a repo?"
    │
    └── L1 answer insufficient
        ├── Mode: Quick → Cannot expand → Elevation prompt
        └── Mode: Standard → Can expand to L2
            │
            └── L2: codebase_search("index-repo", "framework-command-index.md")
                └── Returns detailed command syntax
```

### Budget Enforcement Rules

**Quick Mode:**
1. If L1 insufficient → **Prompt for elevation to Standard**
2. Do NOT automatically expand to L2
3. Behavioral files (L3) always allowed

**Standard Mode:**
1. Track L2 expansions: `current_l2_count <= 3`
2. If `current_l2_count == 3` and still insufficient → **Prompt for elevation to Deep**
3. Allow 1 L3 read (non-behavioral) if L2 insufficient
4. Behavioral files (L3) always allowed

**Deep Mode:**
1. L2 expansions: Unlimited (but prefer efficiency)
2. Track L3 reads: `current_l3_count <= 5`
3. If `current_l3_count == 5` and still insufficient → **Prompt for elevation to Massive**
4. Behavioral files (L3) always allowed

**Massive Mode:**
1. No limits
2. Still prefer L2→L3 progression for efficiency
3. Monitor context window usage

---

## Mode Elevation Protocol

### Elevation Triggers

**Quick → Standard:**
```
Agent detects: L1 compressed index insufficient for query
Agent response:
  "The compressed index doesn't have enough detail for this query.
   I can search the original documentation (Standard mode) for
   detailed information.

   Elevate to Standard mode? (yes/no)"
```

**Standard → Deep:**
```
Agent detects: Used 3/3 L2 expansions, still need more context
Agent response:
  "I've reached the Standard mode limit (3 detailed searches).
   To provide a comprehensive answer, I need Deep mode access
   to read full files and explore the architecture.

   Elevate to Deep mode? (yes/no)"
```

**Deep → Massive:**
```
Agent detects: Used 5/5 L3 reads, still need more files
Agent response:
  "I've read 5 full files (Deep mode limit) and still need more
   context for a complete solution. This appears to be a complex
   cross-cutting task requiring extensive codebase exploration.

   Elevate to Massive mode for unrestricted access? (yes/no)"
```

### User-Initiated Elevation
```
User: "Use Deep mode for this session"
Agent: "Switching to Deep mode (L1 + unlimited L2 + up to 5 L3 reads)"

User: "Go Massive"
Agent: "Switching to Massive mode (unrestricted expansion)"
```

### Mode De-Elevation
```
User: "Switch back to Standard mode"
Agent: "Confirmed. Now in Standard mode (L1 + 3 L2 expansions)"

Note: De-elevation resets expansion counters
```

---

## Decision Flowcharts

### Expansion Decision (Standard Mode)

```
┌─────────────────────┐
│ Query received      │
└──────────┬──────────┘
           │
           ▼
  ┌────────────────┐
  │ Check L1 index │
  └────┬───────────┘
       │
       ▼
  L1 sufficient?
       │
   ┌───┴───┐
  Yes     No
   │       │
   │       ▼
   │  ┌───────────────────┐
   │  │ L2 budget check:  │
   │  │ current_l2 < 3?   │
   │  └───┬──────────┬────┘
   │     Yes        No
   │      │          │
   │      ▼          ▼
   │  ┌─────────┐  ┌──────────────┐
   │  │ Expand  │  │ Prompt for   │
   │  │ to L2   │  │ Deep mode    │
   │  └────┬────┘  └──────────────┘
   │       │
   │       ▼
   │  L2 sufficient?
   │       │
   │   ┌───┴───┐
   │  Yes     No
   │   │       │
   │   │       ▼
   │   │  ┌─────────────────┐
   │   │  │ L3 budget check:│
   │   │  │ used_l3 < 1?    │
   │   │  └───┬──────┬──────┘
   │   │     Yes    No
   │   │      │      │
   │   │      ▼      ▼
   │   │  ┌─────┐  ┌──────────────┐
   │   │  │ L3  │  │ Prompt for   │
   │   │  │Read │  │ Deep mode    │
   │   │  └──┬──┘  └──────────────┘
   │   │     │
   │   │     ▼
   │   │  Sufficient?
   │   │     │
   │   │  ┌──┴──┐
   │   │ Yes   No
   │   │  │     │
   │   │  │     ▼
   │   │  │  ┌──────────────┐
   │   │  │  │ Prompt for   │
   │   │  │  │ Deep mode    │
   │   │  │  └──────────────┘
   │   │  │
   └───┴──┴────────────────┐
                           │
                           ▼
                    ┌─────────────┐
                    │ Return      │
                    │ answer      │
                    └─────────────┘
```

### Mode Selection (Session Start)

```
┌─────────────────────┐
│ Session initialized │
└──────────┬──────────┘
           │
           ▼
  ┌────────────────────┐
  │ User specified     │
  │ mode preference?   │
  └────┬───────────────┘
       │
   ┌───┴───┐
  Yes     No
   │       │
   ▼       ▼
┌──────┐  ┌────────────────┐
│ Use  │  │ Infer from     │
│ that │  │ query type:    │
│ mode │  │ - Simple ref?  │
└──────┘  │   → Quick      │
          │ - How/explain? │
          │   → Standard   │
          │ - Architecture?│
          │   → Deep       │
          │ - Refactor?    │
          │   → Massive    │
          └────────────────┘
```

---

## Best Practices

### ✅ DO
- Start with the most restrictive mode that seems reasonable
- Prompt user before elevation (don't auto-elevate)
- Track expansion graph per session
- Reset counters when switching modes
- Prefer L2→L3 progression even in Massive mode
- Always load behavioral files in full (exempt from budgets)

### ❌ DON'T
- Auto-elevate without user consent
- Skip L1 and go straight to L3
- Expand everything in Massive mode "just because"
- Count behavioral file reads against L3 budget
- Use Quick mode for complex architectural questions
- Ignore mode limits to "be helpful" (prompt for elevation instead)

---

## Examples

### Example 1: Quick Mode (Success)
```
User: "What command lists contexts?"
Mode: Quick
Agent process:
  1. Check framework-command-index.compact (L1)
  2. Find: "make list-ctx"
  3. Return answer
Cost: 0 additional tokens (L1 already loaded)
```

### Example 2: Quick Mode (Elevation Needed)
```
User: "How do I index a repository with a custom collection name?"
Mode: Quick
Agent process:
  1. Check framework-command-index.compact (L1)
  2. Find: "make index-repo" (but no syntax details)
  3. L1 insufficient, Quick mode cannot expand to L2
  4. Prompt: "Elevate to Standard mode for detailed command syntax?"
User: "yes"
Mode: Standard (elevated)
Agent continues:
  5. Expand to L2: codebase_search("index-repo custom collection", ...)
  6. Return detailed syntax
Cost: ~500 tokens (L2 expansion)
```

### Example 3: Standard Mode (Within Budget)
```
User: "Explain the make index-framework command"
Mode: Standard
Agent process:
  1. Check L1: "make index-framework" found (basic reference)
  2. L1 insufficient, expand to L2 (count: 1/3)
  3. codebase_search("index-framework command details", ...)
  4. Return detailed explanation
Cost: ~500 tokens (L2 expansion)
L2 budget remaining: 2/3
```

### Example 4: Standard Mode (Budget Exhausted)
```
User: "Explain the complete RAG indexing architecture"
Mode: Standard
Agent process:
  1. Check L1: Multiple related entries
  2. Expand L2 #1: codebase_search("RAG indexer architecture", ...)
  3. Expand L2 #2: codebase_search("indexer chunking strategy", ...)
  4. Expand L2 #3: codebase_search("indexer metadata", ...)
  5. Still need comprehensive view, but L2 budget exhausted (3/3)
  6. Prompt: "Elevate to Deep mode for full file access?"
User: "yes"
Mode: Deep (elevated)
Agent continues:
  7. L3 read: rag/indexer/app.py
  8. L3 read: rag/indexer/README.md
  9. Return comprehensive architecture explanation
Cost: 1.5k (L2) + 3k (L3) = 4.5k tokens
L3 budget remaining: 3/5
```

### Example 5: Deep Mode (Success)
```
User: "How does the SBMI compilation work end-to-end?"
Mode: Deep
Agent process:
  1. Check L1: SBMI references found
  2. L2 expansions (multiple, unlimited in Deep):
     - codebase_search("SBMI compilation", ...)
     - codebase_search("hash-based cache", ...)
     - codebase_search("compression strategies", ...)
  3. L3 reads (within budget):
     - sbmi/compiler/compiler.py (L3 count: 1/5)
     - sbmi/compiler/cache.py (L3 count: 2/5)
     - sbmi/compiler/strategies.py (L3 count: 3/5)
  4. Return comprehensive end-to-end explanation
Cost: ~2k (L2) + ~4.5k (L3) = 6.5k tokens
L3 budget remaining: 2/5
```

### Example 6: Massive Mode (Unrestricted)
```
User: "Refactor the SBMI package to add Level 3 symbol compression"
Mode: Massive
Agent process:
  1. Check L1: SBMI references
  2. L2 expansions (multiple, unlimited):
     - Design docs, architecture references
  3. L3 reads (unlimited):
     - All sbmi/compiler/*.py files
     - All sbmi/tests/*.py files
     - config/sbmi-compression.yaml
     - Design documentation
     - (6+ full file reads, no budget constraint)
  4. Implement refactoring across multiple files
Cost: ~10-20k tokens (comprehensive codebase load)
```

---

## Behavioral File Exemption

**Critical Rule:** Behavioral files are ALWAYS loaded in full (L3), regardless of mode, and do NOT count against L3 budgets.

### Exempt Files
- `prompts/dev_agent/dev_agent_init_prompt.md`
- `prompts/dev_agent/dev_agent_session_end_prompt.md`
- `prompts/red_team/red_team_agent_init_prompt.md`
- `prompts/red_team/red_team_agent_session_end_prompt.md`
- `templates/dev_agent_persona.md`
- `templates/red_team_agent_persona.md`
- All files matching exclusion patterns in `config/sbmi-compression.yaml`

### Rationale
Behavioral files define agent behavior and must be read completely for quality. They are never compressed, always verbatim-copied to `.compact` extensions, and their L3 reads are exempt from budget tracking.

---

## Implementation Checklist

### For Agent Developers
- [ ] Add mode selection to agent initialization
- [ ] Implement expansion graph tracking
- [ ] Create elevation prompt templates
- [ ] Add mode switch commands
- [ ] Exempt behavioral files from L3 counting
- [ ] Test elevation workflows

### For Session Management
- [ ] Default to Standard mode unless specified
- [ ] Track current mode in session state
- [ ] Reset counters on mode change
- [ ] Persist mode preference across queries
- [ ] Log expansion costs for telemetry

### For Validation
- [ ] Verify elevation prompts trigger correctly
- [ ] Ensure behavioral files never count against budgets
- [ ] Test mode de-elevation
- [ ] Validate graph tracking accuracy
- [ ] Confirm Quick mode never auto-expands

---

## Related Documentation

- **Expansion Protocol:** `expansion-protocol.md` - L1→L2→L3 navigation
- **Design Doc:** `../symbolic-budget-index-system-design.md` - Full SBMI spec
- **Config:** `../../config/sbmi-compression.yaml` - Compression settings
- **Package Docs:** `../../sbmi/README.md` - Implementation details

---

**Version History:**
- 1.0 (2025-12-09): Initial depth budget specification
- 2.0 (2025-12-09): Phase 2 implementation - formal mode definitions

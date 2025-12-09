# SBMI Mode Selection Protocol

**Version:** 2.0
**Date:** 2025-12-09
**Status:** Phase 2 - Agent Behavioral Integration

---

## Overview

This document defines how agents select and manage SBMI depth modes during sessions. This is **behavioral guidance** that agents must internalize, not just reference documentation.

---

## Mode Selection at Session Start

### Default Behavior
**Always start in Standard mode** unless:
1. User explicitly specifies a mode
2. Query type strongly suggests different mode
3. Prior session preference is stored

### Mode Inference from Query

**Quick Mode signals:**
- "What command..." / "Where is..."
- Simple lookups, no "how" or "why"
- Fast reference needed

**Standard Mode signals:** (DEFAULT)
- "How do I..." / "Explain..."
- Implementation questions
- Moderate detail needed

**Deep Mode signals:**
- "Understand the architecture..."
- "Debug..." / "Why isn't..."
- Comprehensive study needed

**Massive Mode signals:**
- "Refactor..." / "Redesign..."
- "Implement [major feature]..."
- Cross-cutting changes

### User-Specified Mode
```
User: "Use Deep mode for this session"
Agent: "Switching to Deep mode (L1 + unlimited L2 + up to 5 L3 reads).
        I'll track expansion depth and prompt for elevation if needed."
```

---

## Expansion Tracking (CRITICAL)

### Internal State Management
Agents MUST track:
```
current_mode: "Standard"  # Quick | Standard | Deep | Massive
l2_expansions: 0  # Count of semantic searches
l3_reads: 0  # Count of full file reads (excluding behavioral)
expansion_graph: []  # List of (layer, file, cost) tuples
```

### Counting Rules

**L2 Expansions (Semantic Search):**
- Count: Each `codebase_search` call to non-code files
- Exempt: Code file searches (use unlimited)
- Exempt: Behavioral file searches

**L3 Reads (Full Files):**
- Count: Each `read_file` call to documentation/markdown
- Exempt: Code file reads (use unlimited)
- Exempt: Behavioral file reads (personas, init prompts, guides)
- Exempt: Config files <100 lines

**Behavioral File Exemption (ALWAYS):**
Files matching these patterns are ALWAYS L3 exempt:
- `*_agent_persona.md`
- `*_init_prompt.md`
- `*_session_end_prompt.md`
- `*_workflow_guide.md`
- `style-and-philosophy/**`
- `workflows-and-processes/**`

---

## Elevation Protocol (BEHAVIORAL)

### When to Prompt

**Quick → Standard:**
Trigger when L1 compressed index is insufficient

**Standard → Deep:**
Trigger when either:
- L2 count reaches 3 and still insufficient
- L3 count reaches 1 and still insufficient

**Deep → Massive:**
Trigger when L3 count reaches 5 and still insufficient

### How to Prompt

**Template:**
```
I've reached the [CURRENT_MODE] mode limit ([SPECIFIC_LIMIT]).
To [PROVIDE_WHAT_USER_NEEDS], I need [NEXT_MODE] mode access
to [SPECIFIC_CAPABILITY].

Elevate to [NEXT_MODE] mode? (yes/no)
```

**Example (Standard → Deep):**
```
I've reached the Standard mode limit (3 detailed searches).
To provide a comprehensive architecture explanation, I need Deep mode
access to read full source files and explore the implementation.

Elevate to Deep mode? (yes/no)
```

### User Response Handling

**If "yes":**
- Switch mode immediately
- Reset counters for new mode
- Continue with elevated permissions

**If "no":**
- Provide best answer with current information
- Suggest: "I can provide more details if you elevate later"
- Do NOT auto-elevate

**If unclear:**
- Ask for clarification
- Explain what elevation enables

---

## Mode-Specific Behaviors

### Quick Mode Agent Behavior
```
Internal rule: "I can only use L1 compressed indexes"

When user asks for details:
1. Check L1 compressed index
2. If found: Answer from L1
3. If insufficient: Prompt for Standard elevation
4. Do NOT expand to L2 without permission
```

### Standard Mode Agent Behavior
```
Internal rule: "I have 3 L2 searches, 1 L3 read"

Expansion strategy:
1. Check L1 first (free)
2. If insufficient: Use L2 semantic search (track count)
3. If L2 count reaches 3: Prompt for Deep elevation
4. If critical file needed: Use 1 L3 read
5. If L3 used and still need more: Prompt for Deep elevation
```

### Deep Mode Agent Behavior
```
Internal rule: "Unlimited L2, 5 L3 reads"

Expansion strategy:
1. Check L1 first (free)
2. Use L2 freely to narrow scope
3. Read full files (L3) when needed (track count)
4. If L3 count reaches 5: Prompt for Massive elevation
5. Prefer L2→L3 progression for efficiency
```

### Massive Mode Agent Behavior
```
Internal rule: "No limits, but still be smart"

Expansion strategy:
1. Still check L1 first (efficiency)
2. Use L2 to narrow before L3 (don't waste context)
3. Read what you need (no artificial limits)
4. Monitor context window usage
5. Warn if approaching context limits
```

---

## Response Patterns

### Successful L1 Answer (Any Mode)
```
User: "What command lists contexts?"
Agent: [Checks L1 index]
       "The command is: make list-ctx

        This is available in the framework command index."
Cost: 0 tokens (L1 already loaded)
```

### L2 Expansion (Standard Mode)
```
User: "How do I index a specific repository?"
Agent: [Checks L1, finds "make index-repo" but needs details]
       [Expands to L2: codebase_search(...)]
       [Increments l2_count: 1/3]

       "To index a specific repository:
        make index-repo REPO_PATH=/path COLLECTION_NAME=name

        [Details from semantic search...]"

Cost: ~500 tokens
Mode: Standard (2/3 L2 remaining)
```

### Elevation Prompt (Standard Mode)
```
User: "Explain the complete RAG architecture"
Agent: [Checks L1, insufficient]
       [L2 search #1: "RAG architecture"]
       [L2 search #2: "indexer chunking"]
       [L2 search #3: "embeddings"]
       [Still insufficient, l2_count = 3/3]

       "I've used all 3 Standard mode searches and have a partial
        picture. To explain the complete architecture, I need Deep
        mode to read the full source files.

        Elevate to Deep mode? (yes/no)"
```

### Mode Switch Confirmation
```
User: "yes"
Agent: "Switched to Deep mode (unlimited L2 + up to 5 L3 reads).
        Continuing with comprehensive analysis..."
        [Resets counters for Deep mode]
        [Reads full files as needed]
```

---

## Best Practices (Agent Internalization)

### ✅ DO
- Start in Standard mode by default
- Track expansion counts accurately
- Prompt before elevation (never auto-elevate)
- Explain what elevation enables
- Reset counters when switching modes
- Exempt behavioral files from all budgets
- Use L1→L2→L3 progression even in Massive

### ❌ DON'T
- Auto-elevate without user permission
- Count behavioral file reads
- Skip L1 check (always try L1 first)
- Expand everything in Massive "because I can"
- Forget to reset counters on mode switch
- Prompt for elevation if behavioral file is the answer

---

## Integration Points

### Agent Init Prompt
Add section:
```markdown
## 🎚️ SBMI Depth Mode Selection

**Default Mode:** Standard (L1 + 3 L2 expansions + 1 L3 read)

**Read and internalize:**
- `local/workflow-indexes/depth-budgets.md.compact` - Mode definitions
- `local/workflow-indexes/sbmi-mode-selection-protocol.md.compact` - This file
- `local/workflow-indexes/expansion-protocol.md.compact` - L1→L2→L3 navigation

**Mode tracking:**
Initialize: current_mode = "Standard", l2_count = 0, l3_count = 0

**Behavioral rules:**
- ALWAYS check L1 compressed indexes first
- Track expansion depth as you navigate
- Prompt for elevation when limits reached
- NEVER count behavioral file reads against budgets
```

### Agent Persona
Add section:
```markdown
## Expansion Depth Management

You manage token budgets through depth mode selection:
- **Quick:** Fast answers from L1 indexes only
- **Standard:** Moderate depth (your default mode)
- **Deep:** Comprehensive study with multiple file reads
- **Massive:** Unrestricted for major tasks

You MUST track expansion and prompt for elevation when needed.
You NEVER auto-elevate without user permission.
```

### Session End Prompt
Add reminder:
```markdown
## Mode Usage Report

Report to user:
- Mode used: [Quick/Standard/Deep/Massive]
- L2 expansions: [X]
- L3 reads: [Y]
- Elevations requested: [Z]

If frequently hitting limits, suggest starting next session in higher mode.
```

---

## Examples (Full Behavioral Flow)

### Example 1: Quick Mode Elevation
```
User: "What's make index-framework?"
Agent: [Mode: Quick, L2: 0/0, L3: 0/0]
       [Checks L1 index]
       [Finds basic reference but no details]

       "I found the command in the index, but Quick mode doesn't have
        enough detail. I can search the documentation (Standard mode)
        for comprehensive information.

        Elevate to Standard mode? (yes/no)"

User: "yes"
Agent: [Switches to Standard: L2: 0/3, L3: 0/1]
       [Expands L2: codebase_search("index-framework", ...)]
       [L2: 1/3]

       "The make index-framework command:
        [Full details from semantic search...]"
```

### Example 2: Standard Mode Multi-Expansion
```
User: "How does the SBMI compiler work?"
Agent: [Mode: Standard, L2: 0/3, L3: 0/1]
       [Checks L1, finds references]

       [L2 #1: "SBMI compiler overview"] (L2: 1/3)
       [L2 #2: "hash-based cache"] (L2: 2/3)
       [L2 #3: "compression strategies"] (L2: 3/3)

       "The SBMI compiler uses:
        [Details from 3 searches...]

        I've used all 3 Standard mode searches. If you need the
        complete implementation details, I can elevate to Deep
        mode to read the source files.

        Continue with current information or elevate? (current/elevate)"
```

---

## Validation Checklist

Before declaring mode selection integrated:
- [ ] Init prompt includes mode selection section
- [ ] Persona includes expansion depth management
- [ ] Session end includes mode usage reporting
- [ ] Elevation prompts are clear and specific
- [ ] Behavioral file exemption is enforced
- [ ] Counter tracking is accurate
- [ ] Mode switching resets counters
- [ ] Default mode is Standard

---

## Related Documentation

- **Depth Budgets:** `depth-budgets.md` - Formal mode definitions
- **Expansion Protocol:** `expansion-protocol.md` - L1→L2→L3 navigation
- **SBMI Design:** `../symbolic-budget-index-system-design.md` - Full spec

---

**This is BEHAVIORAL guidance. Agents must internalize these patterns, not just reference them.**

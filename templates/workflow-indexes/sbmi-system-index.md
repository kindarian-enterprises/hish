# SBMI System Index (Symbolic Budget-Managed Index)

## Overview

The SBMI system optimizes framework documentation for AI agent token budgets while maintaining full semantic search capability.

**Key concept:** Agents READ `.compact` files (token-optimized), WRITE to `.md` files (full text), RAG indexes `.md` files (semantic search).

---

## Core Components

### 1. Compression Engine (`sbmi/`)

**Purpose:** Compile framework `.md` → `.compact` files

**Components:**
- `compiler/compiler.py` - Main IndexCompiler class
- `compiler/strategies.py` - Compression strategies (structural, phrase, combined)
- `compiler/config.py` - Configuration loader
- `compiler/cache.py` - Hash-based change detection
- `analyzer/frequency.py` - Phrase frequency analysis

### 2. Configuration (`config/sbmi-compression.yaml`)

**Defines:**
- Scan directories (`templates/`, `prompts/`, `local/`)
- Excluded directories (`docs/`, `style-and-philosophy/`)
- Exclusion patterns (personas, init prompts)
- Phrase mappings (empirically optimized)

### 3. Scripts

**Compilation:**
- `scripts/compact-framework.py` - Incremental compilation CLI
- `scripts/compile-indexes.py` - Full compilation (legacy)
- `scripts/analyze-phrase-frequency.py` - Phrase optimization

---

## Makefile Commands

### Session-End Workflow
```bash
make sbmi-compact          # Incrementally recompile changed files ONLY
```

### Setup & Maintenance
```bash
make setup-framework       # Initial setup (force compile all)
make sbmi-compact-force    # Force recompile everything
make sbmi-stats            # Show cache statistics
```

### Optimization
```bash
make sbmi-analyze          # Analyze phrase frequency
                          # Generates optimized mappings
```

### Testing
```bash
make test-sbmi            # Run all SBMI tests with coverage
make test-sbmi-unit       # Unit tests only
```

---

## Agent Workflow

### 1. Session Start
```
/dev or /red
  ↓
Loads: prompts/{agent}/init_prompt.md.compact
```

### 2. Active Session
```
Agent modifies: templates/workflow-guide.md  (full text)
Agent reads:    templates/workflow-guide.md.compact  (optimized)
```

### 3. Session End
```
/end-dev or /end-red
  ↓
Loads: prompts/{agent}/session_end_prompt.md.compact
  ↓
Reminder: Run make sbmi-compact
  ↓
Only changed files recompiled
```

---

## File Types

### Compressed Files (16-30% reduction)
- Workflow indexes (`local/workflow-indexes/*.md`)
- Templates (`templates/*.md`)
- Framework design docs

**Strategy:** Structural + phrase compression
**Output:** `.compact` files

### Verbatim Files (0% reduction, copied as-is)
- Agent personas (`*_agent_persona.md`)
- Init prompts (`*_init_prompt.md`)
- Session-end prompts (`*_session_end_prompt.md`)
- Style & philosophy (`style-and-philosophy/*.md`)
- Workflows & processes (`workflows-and-processes/*.md`)

**Strategy:** Verbatim copy with header
**Output:** `.md.compact` files
**Rationale:** Behavioral context must be preserved exactly

### Excluded Directories (never scanned)
- `docs/` - User documentation (human-readable only)
- `node_modules/`, `.git/` - System directories

---

## Compression Strategies

### Level 1: Structural Compression
- Remove formatting markers (emojis, separators)
- Remove code block markers
- Strip verbose descriptions
- Remove comments
- Compact whitespace
- Remove empty lines

### Level 2: Structural + Phrase
- All Level 1 passes
- Replace common phrases:
  - `"cross-project intelligence"` → `"xproj-intel"`
  - `"search patterns"` → `"srch-pat"`
  - `"framework documentation"` → `"fw-docs"`
  - `"red team"` → `"rt"`
- Compact syntax (arrows, colons)

**Current implementation:** Combined structural + phrase compression

---

## Cache System

### Hash-Based Change Detection
- **Algorithm:** SHA256 on file contents
- **Storage:** `local/.sbmi-cache.json`
- **Behavior:**
  - New files → compile
  - Changed files → recompile
  - Unchanged files → skip

### Cache Operations
```python
# Check cache stats
make sbmi-stats

# Clear cache (force rebuild)
rm local/.sbmi-cache.json && make sbmi-compact-force
```

---

## Testing

### Test Coverage

**Test Suites:**
1. **test_cache.py** - Hash computation, change detection, cache persistence
2. **test_compiler.py** - Verbatim copy, directory exclusion, incremental compilation
3. **test_config.py** - Config loading, pattern/mapping retrieval
4. **test_strategies.py** - Command preservation, context integrity, compression passes

### Running Tests
```bash
make test-sbmi              # All tests + coverage report
make test-sbmi-unit         # Unit tests only
```

---

## Cursor Integration

### Shortcuts Reference Compact Files
- `/dev` → `dev_agent_init_prompt.md.compact`
- `/end-dev` → `dev_agent_session_end_prompt.md.compact`
- `/red` → `red_team_agent_init_prompt.md.compact`
- `/end-red` → `red_team_agent_session_end_prompt.md.compact`

**Setup:** `make setup-cursor` compiles all `.compact` files automatically

---

## Configuration Deep Dive

### Scan Directories
```yaml
scan_directories:
  - "templates"
  - "prompts"
  - "local"
```

### Excluded Directories
```yaml
excluded_directories:
  - "docs"  # User docs
  - "templates/style-and-philosophy"  # Behavioral
  - "**/node_modules"
  - "**/.git"
```

### Exclusion Patterns (Verbatim Copy)
```yaml
exclusion_patterns:
  - "**/dev_agent_persona.md"
  - "**/qa_agent_persona.md"
  - "**/red_team_agent_persona.md"
  - "**/dev_agent_init_prompt.md"
  - "**/*_session_end_prompt.md"
  - "**/style-and-philosophy/**"
  - "**/workflows-and-processes/**"
```

### Phrase Mappings (Top 30 by impact)
```yaml
phrase_mappings:
  "cross-project intelligence": "xproj-intel"  # 770 chars saved
  "search patterns": "srch-pat"                # 605 chars saved
  "framework documentation": "fw-docs"          # 475 chars saved
  # ... 27 more mappings
```

---

## Optimization Workflow

### 1. Analyze Current Docs
```bash
make sbmi-analyze
```

**Output:**
- Top 50 single words
- Top 50 two-word phrases
- Top 50 three-word phrases
- Suggested phrase mappings (by impact)

### 2. Update Config
Edit `config/sbmi-compression.yaml`:
```yaml
phrase_mappings:
  "new frequent phrase": "abbrev"
```

### 3. Rebuild & Test
```bash
make sbmi-compact-force
make test-sbmi
```

### 4. Measure Impact
```bash
make sbmi-stats

# Output:
# Total files compiled: 56
# Average reduction: 16.5%
```

---

## Troubleshooting

### Issue: Low compression rates

**Solution:**
1. Run `make sbmi-analyze`
2. Add high-impact phrases to `phrase_mappings`
3. Recompile: `make sbmi-compact-force`

### Issue: Changed file not recompiled

**Solution:**
```bash
# Check cache
make sbmi-stats

# Invalidate and rebuild
rm local/.sbmi-cache.json
make sbmi-compact
```

### Issue: Behavioral context mangled

**Check:**
1. Is file in `exclusion_patterns`?
2. Verify verbatim copy: `grep "EXCLUDED from compression" file.md.compact`

---

## Architecture Decisions

### Why Two File Versions?

**Agent reads `.compact`:**
- Token budget optimization
- Faster loading
- Uniform interface

**Agent writes `.md`:**
- Human readability
- Full semantic content
- Git-friendly diffs

**RAG indexes `.md`:**
- Full semantic search accuracy
- No compression artifacts
- Complete context retrieval

### Why Verbatim Copy for Behavioral Files?

**Problem:** Compression could alter nuanced behavioral directives

**Solution:** Copy personas/prompts verbatim to `.compact` extension

**Benefit:** Uniform `.compact` interface without risking behavioral integrity

### Why Hash-Based Caching?

**Problem:** Full recompilation slow (56 files)

**Solution:** SHA256-based change detection

**Result:** Session-end recompilation < 1s (only changed files)

---

## Performance

### Compilation Speed
- **Cold start (no cache):** Fast for all framework files
- **Incremental (cached):** Sub-second for typical session
- **Single file:** Near-instant

### Compression Results
- **Workflow indexes:** Significant reduction
- **Templates:** Moderate reduction
- **Framework design:** Moderate reduction
- **Behavioral files:** Verbatim copy (exact preservation)

### Optimization
- Use `make sbmi-analyze` to identify high-value phrase mappings
- Update `config/sbmi-compression.yaml` with findings
- Rebuild with `make sbmi-compact-force`

---

## Future Enhancements

1. **Expanded phrase mappings** (target: 50% compression)
2. **Semantic compression** (preserve meaning, not text)
3. **Context-aware compression** (different strategies per file type)
4. **Auto-tuning** (learn phrase frequencies over time)

---

## Related Documentation

### User Documentation
- **Quick start:** `../../README.md` (Framework Optimization section)
- **User guide:** `../../docs/agent-management/framework-optimization.md` - Workflows, FAQ
- **Session workflow:** `../workflows-and-processes/sbmi-session-workflow.md` - Detailed workflows

### Developer Documentation
- **Package docs:** `../../sbmi/README.md` - Commands, API, hash mechanism
- **This file:** `local/workflow-indexes/sbmi-system-index.md` - System architecture
- **Design doc:** `../symbolic-budget-index-system-design.md` - Original spec
- **Expansion protocol:** `expansion-protocol.md` - Depth-based expansion (L1→L2→L3)
- **AGENTS.md:** `../../AGENTS.md` - Framework synopsis with SBMI section

### Configuration & Testing
- **Config file:** `../../config/sbmi-compression.yaml` - All settings
- **Test suite:** `../../sbmi/tests/` - All test files
- **CI workflow:** `../../.github/workflows/test-sbmi.yml`
- **Test config:** `../../sbmi/pytest.ini`

### Key Commands
```bash
make sbmi-compact        # Incremental compilation (session-end)
make sbmi-compact-force  # Force full compilation
make sbmi-stats          # View cache statistics
make sbmi-analyze        # Phrase frequency analysis
make test-sbmi           # Run all tests
```

See `sbmi/README.md` for detailed command documentation and Python API.

# Hish Framework - Agent Synopsis

## Purpose
Context management framework providing AI agents with persistent memory and cross-project knowledge through enriched documentation and structured behavioral prompts.

## Architecture

### Core Systems
1. **RAG Infrastructure** (`rag/indexer/`)
   - Indexes markdown documentation into vector database
   - Chunks with overlapping context + metadata
   - MPNet embeddings for semantic search

2. **SBMI Compiler** (`sbmi/`)
   - Compiles framework `.md` → `.compact` files
   - Token optimization for agent navigation
   - Hash-based incremental compilation
   - Comprehensive test coverage

3. **MCP Integration** (`mcp/`)
   - Docker-based Qdrant MCP server
   - Cursor integration for agent memory
   - Unified embeddings across collections

4. **Agent Prompts** (`prompts/`, `templates/`)
   - Development agent persona + workflows
   - Red team agent persona + workflows
   - Init/session-end protocols
   - Behavioral directives

### Key Directories
- `config/` - Compression config, env templates
- `docs/` - User-facing documentation (NOT compressed)
- `local/` - User-specific contexts + framework meta-docs
- `prompts/` - Agent initialization and session prompts
- `sbmi/` - Python package for framework compilation
- `scripts/` - Automation scripts (indexing, setup, analysis)
- `templates/` - Agent personas, workflows, patterns

## Data Flow

```
Documentation (.md)
  ↓
RAG Indexer → Qdrant (full content, semantic search)
  ↓
SBMI Compiler → .compact files (token-optimized, agent navigation)
  ↓
Agent reads .compact → Queries Qdrant → Implements → Stores learnings
  ↓
make sbmi-compact (session end, syncs .compact files)
```

## Agent Workflow Integration

### Session Start
- `/dev` or `/red` loads init prompts from `.compact` files
- Agent queries existing patterns via `qdrant-find`
- Uses `codebase_search` for code, `qdrant-find` for docs/patterns

### Active Session
- Agents modify framework `.md` files (personas, workflows, docs)
- Read `.compact` files for navigation (token-efficient)
- RAG searches use full `.md` content (semantic accuracy)

### Session End
- `/end-dev` or `/end-red` captures learnings
- Reminder to run `make sbmi-compact`
- Only changed files recompiled (~1s)

## Testing

### SBMI Tests (`sbmi/tests/`)
```bash
make test-sbmi              # All tests + coverage
make test-sbmi-unit         # Unit tests only
```

**Test suites:**
- `test_cache.py` - Hash computation, change detection
- `test_compiler.py` - Verbatim copy, incremental compilation
- `test_config.py` - Config loading
- `test_strategies.py` - Compression preservation

### Integration
- `.github/workflows/test-sbmi.yml` - CI pipeline
- `Makefile` - Test execution targets
- `pytest.ini` - Coverage configuration

## Key Commands

### Setup
```bash
make setup-cursor          # Initial framework setup + compilation
make setup-framework       # Just framework compilation
```

### Session Management
```bash
make sbmi-compact          # Incremental: recompile changed files
make sbmi-compact-force    # Full: recompile everything
make sbmi-stats            # Show cache statistics
```

### Optimization
```bash
make sbmi-analyze          # Phrase frequency analysis
make index-framework       # Index framework docs to Qdrant
```

### Development
```bash
make test-sbmi             # Run SBMI tests
make dev-setup             # Install dev dependencies
```

## File Conventions

### Compression Behavior
**Compressed (token-optimized):**
- Workflow indexes (`local/workflow-indexes/*.md`)
- Templates (`templates/*.md` except personas/prompts)
- Design docs (`local/*.md`)

**Verbatim (copied as-is to .compact):**
- Agent personas (`*_agent_persona.md`)
- Init prompts (`*_init_prompt.md`)
- Session-end prompts (`*_session_end_prompt.md`)
- Style & philosophy (`style-and-philosophy/**`)
- Workflows & processes (`workflows-and-processes/**`)

**Excluded (never scanned):**
- User docs (`docs/**`)
- System dirs (`node_modules/`, `.git/`)

### Naming Patterns
- `.md` - Full markdown (human-editable, git-tracked)
- `.compact` - Optimized (agent-readable, gitignored)
- `.md.compact` - Verbatim behavioral context (gitignored)

## Configuration

### SBMI (`config/sbmi-compression.yaml`)
```yaml
scan_directories:           # Where to look
  - templates
  - prompts
  - local

excluded_directories:       # Never scan
  - docs
  - templates/style-and-philosophy

exclusion_patterns:         # Copy verbatim
  - "**/dev_agent_persona.md"
  - "**/*_init_prompt.md"
  - "**/*_session_end_prompt.md"

phrase_mappings:            # Compression mappings
  "cross-project intelligence": "xproj-intel"
  "search patterns": "srch-pat"
  # ... 30 total, empirically optimized
```

### Indexer (`config/env.mpnet`)
- Model: `paraphrase-multilingual-mpnet-base-v2`
- Chunk size: 1000 tokens, 200 overlap
- Collections: Framework docs, project contexts

## Common Tasks

### Adding New Agent Prompt
1. Create `prompts/{agent}/{agent}_new_prompt.md`
2. Add to exclusion patterns in `config/sbmi-compression.yaml`
3. Run `make sbmi-compact-force`
4. Verify verbatim copy: `grep "EXCLUDED from compression" prompts/{agent}/*.compact`

### Optimizing Compression
1. Run `make sbmi-analyze` (phrase frequency)
2. Add high-impact phrases to `config/sbmi-compression.yaml`
3. Rebuild: `make sbmi-compact-force`
4. Check improvement: `make sbmi-stats`

### Adding Framework Documentation
1. Create `.md` file in appropriate directory
2. Run `make sbmi-compact` (incremental)
3. Run `make index-framework` (update RAG)

### Debugging Compilation
```bash
# Check what's in cache
make sbmi-stats

# Force rebuild
rm local/.sbmi-cache.json && make sbmi-compact-force

# Run tests
make test-sbmi
```

## Critical Behaviors

### DO
- Edit `.md` files
- Run `make sbmi-compact` after framework changes
- Use incremental compilation for speed
- Test behavioral changes: `make test-sbmi`
- Check exclusions before compressing sensitive files

### DON'T
- Edit `.compact` files (auto-generated)
- Commit `.compact` files (gitignored)
- Skip session-end compilation
- Compress behavioral files without testing
- Bypass cache without reason

## Integration Points

### Cursor Commands (`.cursor/commands/`)
- `dev.md` → `dev_agent_init_prompt.L2.compact`
- `end-dev.md` → `dev_agent_session_end_prompt.L2.compact`
- `red.md` → `red_team_agent_init_prompt.L1.compact`
- `end-red.md` → `red_team_agent_session_end_prompt.L2.compact`

Uses `{{HISH_ROOT}}` placeholder, replaced during `make setup-cursor`.

### Makefile Targets
- `setup-framework` - Compile framework
- `sbmi-*` - SBMI operations
- `test-sbmi*` - Test execution
- `index-framework` - RAG indexing

### Git Workflow
- `.gitignore` excludes `*.compact` and `.sbmi-cache.json`
- Agents modify `.md` files
- `.compact` files regenerated per-user

## Performance

### Compilation
- Cold start (no cache): Fast for all framework files
- Incremental: Sub-second typical session
- Single file: Near-instant

### Compression
- Workflow indexes: Significant reduction
- Templates: Moderate reduction
- Behavioral files: Verbatim copy (exact preservation)

### Cache
- Storage: JSON in `local/.sbmi-cache.json`
- Algorithm: SHA256 file hashing
- Persistence: Across compiler instances
- Invalidation: Manual or per-file

## Documentation Map

### SBMI System
- **Package docs:** `sbmi/README.md` - Commands, API, hash mechanism
- **User guide:** `docs/agent-management/framework-optimization.md` - Workflows, FAQ
- **System index:** `local/workflow-indexes/sbmi-system-index.md` - Architecture
- **Design doc:** `local/symbolic-budget-index-system-design.md` - Original spec
- **Session workflow:** `local/workflows-and-processes/sbmi-session-workflow.md`
- **Configuration:** `config/sbmi-compression.yaml`

### Testing
- **SBMI tests:** `sbmi/tests/` - All test suites
- **CI:** `.github/workflows/test-sbmi.yml`

### Agent Context
- **Framework index:** `local/workflow-indexes/framework-repository-index.L2.compact`
- **Command index:** `local/workflow-indexes/framework-command-index.L1.compact`
- **Session enforcement:** `local/workflow-indexes/session-workflow-enforcement.L1.compact`

## Documentation

**User-facing:**
- `docs/agent-management/framework-optimization.md` - SBMI user guide
- `docs/setup/getting-started.md` - Initial setup
- `README.md` - Quick start

**Technical:**
- `local/workflow-indexes/sbmi-system-index.md` - System architecture
- `local/workflows-and-processes/sbmi-session-workflow.md` - Workflows
- `local/symbolic-budget-index-system-design.md` - Design document
- `sbmi/README.md` - Package documentation

## Development

### Adding Features
1. Write tests first (`sbmi/tests/`)
2. Implement in appropriate module
3. Update documentation
4. Run full test suite
5. Update `CHANGELOG.md`

### Modifying Compression
1. Update strategies in `sbmi/compiler/strategies.py`
2. Add tests in `sbmi/tests/test_strategies.py`
3. Validate preservation: `make test-sbmi`
4. Update config documentation

### CI/CD
- `.github/workflows/test-sbmi.yml` runs on PR
- Coverage requirement: 85%+
- All tests must pass

## Troubleshooting

**Low compression rates:**
- Run `make sbmi-analyze`
- Update `phrase_mappings` in config
- Target high-frequency phrases

**File not recompiling:**
- Check `make sbmi-stats`
- Clear cache: `rm local/.sbmi-cache.json`
- Force rebuild: `make sbmi-compact-force`

**Behavioral context mangled:**
- Verify exclusion patterns
- Check for "EXCLUDED from compression" header
- Add to `exclusion_patterns` if needed

**Tests failing:**
- Check file paths in tests
- Verify config is valid YAML
- Run with verbose: `pytest -vv sbmi/tests/`

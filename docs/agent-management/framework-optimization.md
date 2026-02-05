# Framework Optimization (SBMI System)

## What is SBMI?

The **Symbolic Budget-Managed Index (SBMI)** system automatically optimizes framework documentation for AI agents, reducing token consumption while preserving full functionality.

**Key benefit:** Agents can navigate the framework efficiently without hitting token limits, while you continue working with normal, readable markdown files.

---

## How It Works

### Two Versions of Each File

Every framework file exists in two versions:

1. **`.md` files** - Full, human-readable markdown
   - You edit these files normally
   - Git tracks these files
   - RAG indexes these for semantic search

2. **`.compact` files** - Token-optimized versions
   - Agents read these files
   - Auto-generated (never edit manually)
   - Git ignores these (regenerated as needed)

**Example:**
```
templates/dev_agent_persona.md        ← You edit this
templates/dev_agent_persona.md.compact ← Agents read this
```

---

## Session Workflow

### 1. Start Your Session

```bash
/dev      # Initialize development agent
# or
/red      # Initialize red team agent
```

The agent loads optimized `.compact` files for fast initialization.

### 2. Work Normally

Edit framework files as usual:
- Modify personas in `templates/`
- Update workflows in `local/workflows-and-processes/`
- Add to workflow indexes in `local/workflow-indexes/`

**The agent reads `.compact` files but you edit `.md` files.**

### 3. End Your Session

```bash
/end-dev  # End development session
# or
/end-red  # End red team session
```

The agent reminds you to sync the compressed files:

```bash
make sbmi-compact
```

**This recompiles only the files you changed** (takes < 1 second).

---

## Commands Reference

### Daily Use

```bash
# After modifying framework files
make sbmi-compact
```
Incrementally recompiles only changed files.

### Setup (First Time)

```bash
# Initial framework setup
make setup-framework
```
Compiles all framework files to `.compact` format.

### Troubleshooting

```bash
# View compilation statistics
make sbmi-stats

# Force rebuild everything
make sbmi-compact-force
```

---

## What Gets Optimized?

### Compressed Files (Token-Optimized)

**Framework indexes:**
- `local/workflow-indexes/framework-command-index.md`
- `local/workflow-indexes/framework-file-index.md`
- `local/workflow-indexes/session-workflow-enforcement.md`

**Templates:**
- `templates/file-synopsis-workflows.md`
- `templates/pattern-taxonomy-guide.md`
- `templates/workflow-guides/*.md`

**Compression techniques:**
- Remove verbose descriptions
- Replace common phrases (`"cross-project intelligence"` → `"xproj-intel"`)
- Strip formatting markup
- Compact whitespace

### Copied Verbatim (No compression)

**These files are copied as-is to maintain behavioral integrity:**

- **Agent personas** (`*_agent_persona.md`)
- **Initialization prompts** (`*_init_prompt.md`)
- **Session-end prompts** (`*_session_end_prompt.md`)
- **Style & philosophy** (`style-and-philosophy/*.md`)
- **Workflows & processes** (`workflows-and-processes/*.md`)

**Why?** Behavioral context must be preserved exactly to maintain agent consistency.

---

## Never Compressed

**User documentation** (`docs/`) is never compressed or scanned.

This ensures all user-facing documentation remains fully readable and is excluded from the optimization system.

---

## Understanding the Output

When you run `make sbmi-compact`:

```bash
⚡ INCREMENTAL MODE: Recompiling changed/new files only

Cache stats:
  Total previously compiled: 56
  Avg reduction: 16.5%
  Last compiled: 2025-12-09T16:25:45

📝 Detected 3 changed/new files:

  CHANGED: local/workflow-indexes/framework-command-index.md
  NEW: templates/new-workflow-guide.md
  CHANGED: templates/dev_agent_persona.md

  ✓ framework-command-index.md → framework-command-index.compact
    [reduced size]

  ✓ new-workflow-guide.md → new-workflow-guide.compact
    [reduced size]

  ≡ dev_agent_persona.md → dev_agent_persona.md.compact (VERBATIM - behavioral)

======================================================================
INCREMENTAL COMPILATION SUMMARY
======================================================================

Total framework files: 56
Changed/new files: 3
Up-to-date files: 53

Files compressed: 2
Files copied verbatim (behavioral context): 1
  ≡ dev_agent_persona.md: preserved in full

✅ Recompiled 3 file(s)
```

**Symbols:**
- `✓` = Compressed successfully
- `≡` = Copied verbatim (behavioral file)
- `CHANGED` = File modified since last compilation
- `NEW` = File never compiled before

---

## FAQ

### Why do I need to run `make sbmi-compact`?

Agents read `.compact` files. When you edit `.md` files, the `.compact` versions become outdated. Running `make sbmi-compact` syncs them.

### What if I forget to run it?

Agents will read stale `.compact` files and won't see your changes. Always run it at session end (the `/end-dev` and `/end-red` commands remind you).

### Can I edit `.compact` files directly?

**No!** They're auto-generated and will be overwritten. Always edit `.md` files.

### How do I know what files will be compressed?

The system scans:
- `templates/`
- `prompts/`
- `local/`

And excludes:
- `docs/` (user documentation)
- Persona files
- Init/session-end prompts
- Style & philosophy docs
- Workflows & processes

See `config/sbmi-compression.yaml` for full configuration.

### What if compression breaks something?

The system has comprehensive automated tests to ensure:
- Commands are preserved exactly
- File paths remain intact
- Environment variables are preserved
- Code syntax is maintained
- Critical context is never lost

If you notice issues:
1. File a bug report
2. The affected file can be added to exclusions
3. It will be copied verbatim instead

### How much faster are agents with compressed files?

Token reduction is significant for navigation files, keeping agents within budget and more responsive across sessions. The hash-based incremental system ensures session-end recompilation remains fast.

### Can I customize compression?

Yes! Edit `config/sbmi-compression.yaml`:

```yaml
# Add files to exclude
exclusion_patterns:
  - "**/my-important-file.md"

# Add phrase abbreviations
phrase_mappings:
  "my frequent phrase": "abbrev"
```

Then rebuild:
```bash
make sbmi-compact-force
```

---

## Optimization Tips

### Analyze Your Framework

```bash
make sbmi-analyze
```

This shows:
- Most frequent words and phrases
- Potential compression opportunities
- Suggested phrase mappings

Use this output to optimize `phrase_mappings` in the config.

### Monitor Performance

```bash
make sbmi-stats
```

Shows:
- Total files compiled
- Average reduction percentage
- Last compilation timestamp

---

## Integration with Agent Sessions

### Agent shortcuts automatically use `.compact` files:

```bash
/dev        # Loads: prompts/dev_agent/dev_agent_init_prompt.L2.compact
/end-dev    # Loads: prompts/dev_agent/dev_agent_session_end_prompt.L2.compact
/red        # Loads: prompts/red_team/red_team_agent_init_prompt.L1.compact
/end-red    # Loads: prompts/red_team/red_team_agent_session_end_prompt.L2.compact
```

This is configured in `.cursor/commands/*.md` and happens automatically.

---

## Best Practices

### ✅ Do

- Run `make sbmi-compact` at session end
- Edit `.md` files normally
- Let the system handle `.compact` files
- Run `make sbmi-stats` periodically to monitor performance

### ❌ Don't

- Edit `.compact` files manually
- Commit `.compact` files to git (they're in `.gitignore`)
- Skip session-end compilation
- Disable compression without understanding impact

---

## Troubleshooting

### Problem: Changes not reflected in agent

**Cause:** Forgot to run `make sbmi-compact`

**Solution:**
```bash
make sbmi-compact
```

### Problem: Compilation fails

**Solution:**
```bash
# Check what changed
git status

# Force rebuild
make sbmi-compact-force

# Check for errors
make test-sbmi
```

### Problem: File shouldn't be compressed

**Solution:**

1. Edit `config/sbmi-compression.yaml`:
   ```yaml
   exclusion_patterns:
     - "**/your-file.md"
   ```

2. Rebuild:
   ```bash
   make sbmi-compact-force
   ```

---

## Documentation

### User Guides
- **This guide:** `docs/agent-management/framework-optimization.md` - User workflow and FAQ
- **Main README:** `README.md` - Quick start overview

### Technical Documentation
- **System index:** `local/workflow-indexes/sbmi-system-index.md` - Architecture details
- **Session workflow:** `local/workflows-and-processes/sbmi-session-workflow.md` - Detailed workflows
- **Package docs:** `sbmi/README.md` - Developer API and commands
- **Design doc:** `local/symbolic-budget-index-system-design.md` - Original design

### Configuration
- **Compression config:** `config/sbmi-compression.yaml` - All settings
- **Exclusion rules:** See config for patterns and directories

### Testing
- **Test suite:** `sbmi/tests/` - All test files
- **CI pipeline:** `.github/workflows/test-sbmi.yml` - Automated testing

## Getting Help

For issues or questions, file a bug report with:
- Output of `make sbmi-stats`
- Files that failed to compile
- Expected vs actual behavior

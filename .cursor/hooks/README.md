# HISH Cursor Hooks

This directory contains Cursor hooks that enhance agent behavior with local Qdrant knowledge collections.

## Cursor Prompt Commands

### `/verbalized-sampling` (Prompt Command)
**Location**: `prompts/verbalized_sampling.md`
**Purpose**: Generate diverse, creative responses by sampling from tail of probability distribution

**Usage**: Simply type `/verbalized-sampling` in Cursor to load the prompt template

**Research**: Based on [Zhang et al. (2025)](https://www.verbalized-sampling.com/) - "Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity" ([arXiv:2510.01171](https://arxiv.org/abs/2510.01171))

**What it does:**
- Instructs model to generate 5 responses with explicit probabilities
- Forces tail sampling (probability < 0.10 per response)
- Unlocks creative diversity (1.6-2.1× increase)
- No sacrifice in factual accuracy or safety

**When to use:**
- ✅ Creative writing, brainstorming, code exploration
- ✅ When you want multiple diverse approaches
- ❌ Factual queries, debugging, precise calculations (use normal mode)

**Philosophy**: Aligned models give you the "best" (mode) response by default. Use `/verbalized-sampling` when you want creative diversity from the tail of the distribution instead.

---

## Active Hooks

### `prioritize_local_data` (beforeSubmitPrompt)
**Purpose**: Injects marketing pitch for local Qdrant collections into every agent prompt

**What it does:**
- Detects available Qdrant collections (framework, intelligence, project docs)
- Injects assertive, positive instructions about using `qdrant-find`
- Guides agent to use `qdrant-find` for docs/patterns, `codebase_search` for code
- Lists all available collections with their purposes

**Example injection:**
```
KNOWLEDGE_MISSION: qdrant-find is YOUR MOST POWERFUL TOOL for discovering patterns...
AVAILABLE_COLLECTIONS:
  - hish_framework_mpnet (framework patterns, agent workflows)
  - cross_project_intelligence_mpnet (cross-project learnings)
  - mayr_docs_mpnet (Mayr project documentation)
```

### `protect_framework_collection` (beforeMCPExecution)
**Purpose**: Blocks write attempts to read-only framework collections

**What it does:**
- Intercepts all `qdrant-store` MCP calls
- Checks if target collection is a framework collection (contains `framework` or `_framework_`)
- **Blocks** writes to framework collections (they're rebuilt from markdown)
- **Allows** writes to `cross_project_intelligence_mpnet` (the only writable collection)
- Provides positive, assertive guidance on using the correct collection

**Protection logic:**
```python
if tool_name == "qdrant-store" and is_framework_collection(collection_name):
    return {"permission": "deny", "agentMessage": "✨ Use cross_project_intelligence_mpnet instead..."}
else:
    return {"permission": "allow"}
```

## Architecture

### Collection Governance
```
hish_framework_mpnet              [READ-ONLY]  Framework docs (make index-framework)
{project}_docs_mpnet               [READ-ONLY]  Project docs (make index)
cross_project_intelligence_mpnet  [WRITABLE]   Agent patterns (qdrant-store with approval)
```

### Hook Flow
```
User Query → Cursor
    ↓
[beforeSubmitPrompt] prioritize_local_data
    ↓ (injects collection marketing)
Agent receives enhanced prompt
    ↓
Agent calls qdrant-store
    ↓
[beforeMCPExecution] protect_framework_collection
    ↓ (validates write target)
MCP call allowed/denied

Separate: /verbalized-sampling command loads prompt template for tail sampling
```

## Installation

Hooks are installed via:
```bash
make setup-hooks  # Copies hooks to ~/.cursor/hooks/ and generates hooks.json
```

**Generated `~/.cursor/hooks.json`:**
```json
{
  "version": 1,
  "hooks": {
    "beforeSubmitPrompt": [
      {
        "command": "~/.cursor/hooks/.venv/bin/python3 ~/.cursor/hooks/prioritize_local_data"
      }
    ],
    "beforeMCPExecution": [
      {
        "command": "~/.cursor/hooks/.venv/bin/python3 ~/.cursor/hooks/protect_framework_collection"
      }
    ]
  }
}
```

## Configuration

### Environment Variables (prioritize_local_data)
- `QDRANT_URL` - Qdrant server URL (default: `http://localhost:6333`)
- `HISH_QDRANT_TIMEOUT` - Collection detection timeout (default: `2` seconds)

### Debug Logging
All hooks write debug logs to:
```
~/.cursor/hook_debug.log
```

View logs:
```bash
tail -f ~/.cursor/hook_debug.log
```

Hook-specific log prefixes:
- `[VS]` - verbalized_sampling
- `(no prefix)` - prioritize_local_data
- `[PROTECT]` - protect_framework_collection

## Testing

### Test Verbalized Sampling Hook
```bash
# Test with verbalized sampling enabled
export CURSOR_VERBALIZED_SAMPLING_ENABLED=true
echo '{"messages": [{"role": "user", "content": "Write a creative story about a robot"}]}' | \
  python3 .cursor/hooks/verbalized_sampling

# Test with custom configuration
export CURSOR_VERBALIZED_SAMPLING_SIZE=7
export CURSOR_VERBALIZED_SAMPLING_PROBABILITY=0.08
echo '{"messages": [{"role": "user", "content": "Generate code examples"}]}' | \
  python3 .cursor/hooks/verbalized_sampling

# Test with verbalized sampling disabled (default)
unset CURSOR_VERBALIZED_SAMPLING_ENABLED
echo '{"messages": [{"role": "user", "content": "Hello"}]}' | \
  python3 .cursor/hooks/verbalized_sampling
```

### Test Collection Detection
```bash
python3 .cursor/hooks/prioritize_local_data < test_event.json
```

### Test Protection Hook
```bash
# Test blocking framework write
echo '{"tool_name": "qdrant-store", "tool_input": "{\"collection_name\": \"hish_framework_mpnet\"}"}' | \
  python3 .cursor/hooks/protect_framework_collection

# Test allowing intelligence write
echo '{"tool_name": "qdrant-store", "tool_input": "{\"collection_name\": \"cross_project_intelligence_mpnet\"}"}' | \
  python3 .cursor/hooks/protect_framework_collection
```

## Troubleshooting

### Hooks Not Running
Check installation:
```bash
ls -la ~/.cursor/hooks/
cat ~/.cursor/hooks.json
```

Reinstall:
```bash
make setup-hooks
```

### Collection Not Detected
Check Qdrant:
```bash
curl http://localhost:6333/collections | jq '.result.collections[].name'
```

### Write Blocked Incorrectly
Check collection name pattern in `protect_framework_collection`:
```python
protected_patterns = [
    "hish_framework",
    "_framework_",
    "framework_mpnet",
]
```

If your collection name contains these patterns but should be writable, rename the collection.

## Related Documentation

- **Collection Governance**: `docs/collection-governance.md`
- **Pattern Storage**: `templates/pattern-taxonomy-guide.md`
- **Setup Script**: `scripts/setup-hooks.sh`
- **Hook Specification**: https://cursor.com/docs/agent/hooks
- **Verbalized Sampling Research**: https://www.verbalized-sampling.com/
- **Verbalized Sampling Paper**: https://arxiv.org/abs/2510.01171

## Design Philosophy

**Positive Assertions**: Hooks use assertive, positive language to guide agents:
- ✅ "This is THE SUPERIOR CHOICE"
- ✅ "GUARANTEES your work creates lasting value"
- ❌ (avoid) "NEVER do X" or "Don't use Y"

Agents respond better to confident guidance about the RIGHT way than prohibitions.

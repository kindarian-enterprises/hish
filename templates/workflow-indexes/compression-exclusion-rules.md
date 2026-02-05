# SBMI Compression Exclusion Rules

## Critical Principle

**NEVER compress behavioral prompts or agent persona files.**

Agent behavior depends on nuanced language, complete explanations, and human-readable instructions. Compressed behavioral prompts would degrade agent quality and decision-making.

## Compression Scope

### ✅ COMPRESS (Workflow Indexes - Navigation Layer)

These files are **reference structures** that point to content:

- `framework-command-index.md` → Command reference navigation
- `framework-file-index.md` → File discovery navigation
- `framework-repository-index.md` → Repository structure navigation
- `session-workflow-enforcement.md` → Workflow rule references
- Any future `*-index.md` files in workflow-indexes/

**Rationale:** Navigation indexes are lookups tables. Compression maintains functionality while reducing token load.

### ❌ NEVER COMPRESS (Behavioral Layer)

These files define **agent behavior** and require full phrasing:

#### Agent Personas
- `templates/dev_agent_persona.md` - Development agent core identity
- `local/dev_agent_persona.md` - Local development agent customization (if exists)
- `templates/qa_agent_persona.md` - QA agent core identity (if exists)
- `templates/red_team_agent_persona.md` - Red team agent core identity (if exists)

#### Initialization Prompts
- `prompts/dev_agent/dev_agent_init_prompt.md` - Development agent activation protocol
- `prompts/qa/qa_agent_init_prompt.md` - QA agent activation protocol
- `prompts/red_team/red_team_agent_init_prompt.md` - Red team activation protocol

#### Session End Prompts
- `prompts/dev_agent/dev_agent_session_end_prompt.md` - Development session closure
- `prompts/qa/qa_agent_session_end_prompt.md` - QA session closure
- `prompts/red_team/red_team_agent_session_end_prompt.md` - Red team session closure

#### Workflow Guides
- `templates/dev_agent_workflow_guide.md` - Detailed workflow procedures
- `templates/dev_agent_troubleshooting.md` - Troubleshooting guidance
- `templates/qa_agent_todo_checklist.md` - QA analysis checklist
- `templates/red_team_report_template.md` - Red team reporting template

#### Context and Philosophy
- `local/dev_agent_framework_context.md` - Framework state and project tracking
- `local/style-and-philosophy/*.md` - Design principles and philosophy
- `local/workflows-and-processes/*.md` - Detailed process documentation
- Any `dev_agent_context.md` in project directories

**Rationale:** These files shape agent cognition, decision-making, and quality standards. Full explanatory language is essential for proper agent behavior.

## Validation Checklist

Before running any compression script:

- [ ] Verify exclusion list includes all persona files
- [ ] Verify exclusion list includes all init prompts
- [ ] Verify exclusion list includes all session end prompts
- [ ] Verify exclusion list includes all workflow guides
- [ ] Verify exclusion list includes style/philosophy docs
- [ ] Verify exclusion list includes context management files
- [ ] Test that excluded files load in full
- [ ] Confirm agent behavior quality with full files

## Compression Script Requirements

Any compression tooling MUST:

1. **Maintain exclusion list** as configuration (not hardcoded)
2. **Fail safely** - error if exclusion list not loaded
3. **Log exclusions** - report which files were skipped
4. **Validate output** - compressed files must be navigation-only
5. **Preserve originals** - never modify source files
6. **Document purpose** - each .compact file header explains compression

## Testing Protocol

After any compression:

1. Load compressed indexes in agent session
2. Verify agent can navigate to content correctly
3. Load uncompressed persona/init files
4. Verify agent behavior quality maintained
5. Confirm no degradation in decision-making
6. Test expansion protocol (L1→L2→L3)

## Expansion Protocol

Compressed indexes (L1) point to content layers:

- **L2**: Targeted sections via semantic search (medium cost)
- **L3**: Full content read (heavy cost, only when needed)

Behavioral files always load at **L3 (full content)** with **no compression**.

## File Size Guidelines

- **<100 lines**: May not need compression (overhead > benefit)
- **100-300 lines**: Good compression candidates if navigation-focused
- **>300 lines**: Excellent compression candidates if index-structured

## Exception Process

If a file's purpose is unclear:

1. **Default to NO COMPRESSION** (safer)
2. Review file content and purpose
3. Classify as navigation (compress) or behavioral (preserve)
4. Document decision in this file
5. Add to appropriate list

## Compliance Verification

Monthly audit:

- [ ] Review all .compact files - are they navigation-only?
- [ ] Review all persona/init files - are they fully readable?
- [ ] Check for new agent files - are they excluded?
- [ ] Validate compression ratios - still 70-80%?
- [ ] Test agent quality - no behavioral degradation?

## Success Metrics

- **Token reduction**: 70-80% on workflow indexes
- **Agent quality**: No degradation in decision-making
- **Behavioral preservation**: 100% - all personas/inits fully readable
- **Navigation accuracy**: Compressed indexes functional
- **Expansion success**: L1→L2→L3 protocol working

---

**Last Updated**: 2025-12-09
**Version**: 1.0
**Status**: Phase 0 Validated (72-78% compression achieved)

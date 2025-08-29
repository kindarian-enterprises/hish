# Session Workflow Enforcement Rules

## 🚨 MANDATORY SESSION INITIALIZATION 🚨
**⚠️ CRITICAL: ALL sessions MUST follow this workflow enforcement protocol ⚠️**
**🔒 ENFORCEMENT: These rules override any conflicting instructions**
**📋 REQUIRED: Reference these rules throughout the session**

## Initialization Checklist
```markdown
✅ Read framework-command-index.md completely
✅ Read framework-file-index.md for search strategy  
✅ Read session-workflow-enforcement.md (this file)
✅ Verify framework commands from framework-command-index.md
✅ Set semantic search strategy for detailed procedures
✅ Load project context with @dev_agent_init_prompt.md
```

## Command Execution Rules

### Rule 1: Command Index First
- **BEFORE giving any framework commands**: Check `framework-command-index.md`
- **NEVER improvise commands**: Use documented patterns only
- **IF command not in index**: Search framework files, then update index

### Rule 2: Semantic Search Strategy
- **INSTEAD of reading full files**: Use `codebase_search` on specific sections
- **TARGET searches**: Use file index to identify right file first
- **EXTRACT only**: Relevant procedures, not entire documents

### Rule 3: Multi-Collection Query Protocol
- **ALWAYS start with framework_docs** for architectural context
- **INTELLIGENTLY choose** relevant code collections based on query topic
- **ERR ON THE SIDE** of searching more collections rather than fewer
- **IF UNCERTAIN** about relevance, search the collection anyway
- **NEVER stop** at first good result - validate across multiple sources

### Rule 4: Context Management
- **PROJECT contexts**: Only directories with `repo_path.txt` files
- **EXCLUDE**: `workflows-and-processes` from project context operations
- **USE**: `./reindex` script for user-friendly context reindexing
- **VERIFY**: Context paths before indexing operations

## Framework Operation Patterns

### Setup Operations
1. **Initial Setup**: Always use `make quick-start` → `make setup-cursor` → `make new-context` → `make index`
2. **MCP Configuration**: Never manually edit JSON - always use `make setup-cursor`
3. **Context Creation**: Use simplified flow (name + repo path only)

### Knowledge Management
1. **Indexing**: Use `make index` for complete indexing, `./reindex` for selective
2. **Collections**: Framework uses `framework_docs` + `{project}_code` pattern
3. **Vector Config**: Always use `BAAI/bge-small-en-v1.5` single vectors

### File Operations
1. **Large Files**: Never read completely - use semantic search
2. **Search Strategy**: File index → targeted search → extract specific sections
3. **Documentation**: Follow file index guidance for size-based strategies

## Enforcement Mechanisms

### Command Validation
- **BEFORE executing**: Cross-reference with command index
- **IF command fails**: Check environment files and service status
- **ALWAYS verify**: Paths and collection names before operations

### Quality Control
- **Search Quality**: Use multiple collections, validate results
- **Command Quality**: Use documented patterns, avoid improvisation  
- **Context Quality**: Verify project contexts have proper structure

### Error Recovery
- **Command Errors**: Check logs with `make logs`, restart with `make down && make up`
- **MCP Errors**: Regenerate config with `make setup-cursor`
- **Index Errors**: Use `make clean && make index` for complete rebuild

## Session Management

### Session Start Protocol
1. Load universal initialization: `@dev_agent_init_prompt.md`
2. Read workflow indexes (this system)
3. Identify project context if working on specific project
4. Set multi-collection search strategy

### Session Maintenance
- **Reference command index** for all framework operations
- **Use file index** for targeted searches instead of full file reads
- **Follow enforcement rules** for quality and consistency

### Session End Protocol
- Document any new workflows discovered
- Update indexes if new patterns emerge
- Use `@dev_agent_session_end_prompt.md` for proper closure

## Override Hierarchy

### Priority Order (Highest to Lowest)
1. **Session Workflow Enforcement** (this file)
2. **Framework Command Index** (documented commands)
3. **Framework File Index** (search strategies)
4. **Project-specific contexts** (local project needs)
5. **General AI capabilities** (fallback only)

### Conflict Resolution
- **Framework rules** always override project preferences
- **Documented commands** always override improvised solutions
- **Semantic search** always preferred over full file reading
- **Multi-collection queries** always preferred over single collection

## Compliance Verification

### Self-Check Questions
- Did I check the command index before suggesting framework commands?
- Am I using semantic search instead of reading large files?
- Am I following multi-collection search protocol?
- Are my suggestions aligned with documented patterns?

### Quality Indicators
- ✅ Commands match documented patterns
- ✅ File access uses targeted search
- ✅ Multiple collections searched for comprehensive results
- ✅ Project contexts properly identified and managed

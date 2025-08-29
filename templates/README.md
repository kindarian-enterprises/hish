# 📋 Templates Directory

**Purpose**: Contains the essential scaffold for creating new project contexts.

## 📁 **What's Here**

### **`context/dev_agent_context_template.md`** - **REQUIRED TEMPLATE**
This is the core template for new project contexts. It contains:

- **Critical Update Protocol** - Mandatory rules for maintaining project continuity
- **Comprehensive Project Structure** - All sections needed for project tracking
- **Standardized Format** - Consistent syntax for cross-project intelligence
- **Protocol Enforcement** - Zero-tolerance rules for data integrity

### **`workflow-indexes/`** - **FRAMEWORK NAVIGATION SYSTEM**
Internal workflow indexes that initialize on first context creation:

- **`framework-command-index.md`** - 🚨 **ALL framework commands** - MUST reference before operations
- **`framework-file-index.md`** - File-to-purpose mapping for targeted searches
- **`session-workflow-enforcement.md`** - Behavioral enforcement rules for agents
- **`framework-repository-index.md`** - Complete repository structure reference

**Usage**: These are automatically copied to `local/workflow-indexes/` on first context creation and provide the navigation system for agents working with the framework.

## 🚫 **What's NOT Here (And Why)**

- **No Persona Templates** - Universal persona is at top level (`dev_agent_persona.md`)
- **No Prompt Templates** - Universal prompts are at top level (`dev_agent_init_prompt.md`, `dev_agent_session_end_prompt.md`)
- **No Workflow Templates** - Workflows are agent-managed in `local/workflows-and-processes/`

## 🎯 **Usage**

**For Users**: You don't need to touch this directory. The `new-project-context.sh` script automatically uses the context template.

**For Framework Development**: This template defines the standard structure for all project contexts. Changes here affect all new contexts created.

## 🔒 **Why This Template Exists**

1. **Consistency**: Every project context follows the same structure
2. **Protocol Enforcement**: Critical update rules are built into the template
3. **Cross-Project Intelligence**: Standardized format enables pattern recognition
4. **Historical Continuity**: Template ensures proper project tracking from day one

---

**Bottom Line**: This is the scaffold that makes cross-project intelligence possible. Don't modify it unless you're updating the framework's project context structure.

# Pattern Taxonomy & Storage Guide

## 🎯 Purpose

This guide defines how to extract, categorize, and store patterns, file synopses, and cross-project intelligence within the Hish framework. **Hish focuses on enriched documentation and knowledge curation, not code indexing** (Cursor handles code natively).

---

## 🏗️ Core Concepts

### **What Belongs in Hish Collections**
✅ **Enriched Documentation**: Architectural decisions, design rationale, context
✅ **Pattern Extraction**: Recurring solutions, anti-patterns, best practices
✅ **File Synopses**: High-level descriptions of what AGENTS.md files contain
✅ **Taxonomy**: Categorized knowledge (auth patterns, error handling, deployment workflows)
✅ **Cross-Project Intelligence**: Learnings applicable to multiple projects

✅ **What Belongs Elsewhere (Optimal Tool Selection)**
→ **Code symbols, function implementations** → Use `codebase_search` (Cursor excels at this)
→ **Implementation details** → Best discovered through `codebase_search`
→ **Confidential data** → Belongs in secure vaults, not documentation
→ **Temporary notes** → Keep in local scratch files, promote to docs when validated

---

## 📊 Pattern Taxonomy Structure

### **1. Architectural Patterns**
```markdown
**Category**: Architecture
**Pattern Name**: [Descriptive name]
**Context**: [When/where applicable]
**Solution**: [High-level approach]
**Evidence**: [Measured outcomes, links to implementations]
**Projects**: [Where successfully applied]
**Success Patterns**: [Proven approaches that deliver results]
```

**Examples:**
- Microservices communication patterns
- Event-driven architecture implementations
- Database migration strategies
- Container orchestration patterns

### **2. Technical Patterns**
```markdown
**Category**: Technical
**Pattern Name**: [Specific technique]
**Technology**: [Language/framework]
**Problem**: [What it solves]
**Implementation**: [High-level steps]
**Gotchas**: [Known issues]
**Related Patterns**: [Connections]
```

**Examples:**
- JWT authentication with refresh tokens
- Redis-based rate limiting
- Graceful shutdown patterns
- Error handling with circuit breakers

### **3. Process Patterns**
```markdown
**Category**: Process
**Pattern Name**: [Workflow name]
**Purpose**: [What it achieves]
**Steps**: [High-level workflow]
**Tools**: [Required tools/scripts]
**Success Criteria**: [How to verify]
**References**: [AGENTS.md files, docs]
```

**Examples:**
- CI/CD pipeline configurations
- Database migration workflows
- Container build optimizations
- Testing strategies

### **4. Security Patterns & Remediation (Vulnerability Taxonomy for Red Team)**
```markdown
**Category**: Security Pattern
**Name**: [Vulnerability type]
**Severity**: [Critical/High/Medium/Low]
**Risk**: [Security, Performance, Reliability]
**Evidence**: [Where observed]
**Effective Remediation**: [Proven fix approaches]
**Detection Methods**: [How to identify]
```

**Examples (focus on solutions):**
- SQL injection → Parameterized queries pattern
- Race conditions → Proper locking patterns
- Memory leaks → Resource management patterns
- Secret management → Vault integration patterns

---

## 📝 File Synopsis Templates

### **AGENTS.md Synopsis Template**
```markdown
# AGENTS.md Synopsis - [Repository Name]

## Overview
[2-3 sentence description of repository and its AGENTS.md ecosystem]

## Discovered Files
- `AGENTS.md` - [Purpose and key content]
- `module/AGENTS.md` - [Purpose and key content]

## Key Technical Patterns
1. **[Pattern 1]**: [Description]
2. **[Pattern 2]**: [Description]
3. **[Pattern 3]**: [Description]

## Essential Commands
\`\`\`bash
# [Category]
make command-name  # Description
docker compose command  # Description
\`\`\`

## Architecture Notes
- [Key architectural decision or constraint]
- [Important deployment consideration]

## File Hashes (Change Detection)
- `AGENTS.md`: [SHA256]
- `module/AGENTS.md`: [SHA256]

**Generated**: [ISO timestamp]
**Last Verified**: [ISO timestamp]
```

### **Project Context Synopsis Template**
```markdown
# Project Context - [Project Name]

## Purpose
[What this project does]

## Architecture
[High-level architecture - components, communication patterns]

## Key Design Decisions
1. **[Decision]**: [Rationale and implications]
2. **[Decision]**: [Rationale and implications]

## Tech Stack
- **Language**: [Primary language + version]
- **Framework**: [Main framework]
- **Database**: [Database + version]
- **Infrastructure**: [Docker, K8s, etc.]

## Development Workflow
\`\`\`bash
# Setup
[Key setup commands]

# Testing
[Test commands]

# Deployment
[Deploy commands]
\`\`\`

## Critical Files
- `[file]`: [Purpose]
- `[file]`: [Purpose]

## Cross-Project Relevance
- **Patterns**: [Which patterns from this project apply elsewhere]
- **Learnings**: [What we learned that's universally applicable]

**Last Updated**: [ISO timestamp]
```

---

## 🎯 Storage Guidelines

### **When to Use qdrant-store**

✅ **Store When:**
- Pattern is validated and working in production
- Solution solves a recurring problem
- Learning has cross-project applicability
- User has explicitly approved storage

✅ **Store in Better Locations:**
- **Unvalidated hypotheses** → Test first, then store validated patterns
- **Project-specific details** → Belong in project docs (more discoverable there)
- **Sensitive information** → Use secure vaults (protects confidentiality)
- **Temporary notes** → Keep local until validated (promotes quality)

### **Storage Workflow**

1. **Extract Pattern**: Identify reusable pattern from implementation
2. **Document**: Create structured documentation using taxonomy
3. **Request Approval**: Present to user for review
4. **Store**: Only after user approval, use `qdrant-store`
5. **Link**: Reference stored pattern in project docs

**Example Workflow:**
```markdown
USER: "We implemented JWT auth with Redis blacklisting"

AGENT:
1. Extracts pattern details
2. Documents in taxonomy format
3. Presents for approval:

PROPOSED KNOWLEDGE STORAGE:

**Category**: Technical Pattern
**Pattern**: JWT Authentication with Redis Token Blacklist
**Technology**: Node.js + Redis
**Problem**: Need to invalidate JWT tokens before expiration
**Solution**:
  - Store invalidated token JTIs in Redis with TTL = token expiration
  - Check Redis on every authenticated request
  - 2ms lookup overhead, prevents token reuse
**Evidence**: Tested in production, 100k RPM, <5ms P99 latency
**Projects**: api-gateway, user-service
**Files**: `src/auth/jwt-middleware.ts`

Please review for accuracy and approve storage.

USER: "Approved"

AGENT: [Stores with qdrant-store in cross_project_intelligence_mpnet collection]
```

---

## 🔍 Querying Patterns

### **Framework Patterns**
```bash
qdrant-find "authentication patterns" hish_framework_mpnet
qdrant-find "error handling best practices" hish_framework_mpnet
```

### **Cross-Project Intelligence**
```bash
qdrant-find "JWT authentication implementations" cross_project_intelligence_mpnet
qdrant-find "database migration strategies" cross_project_intelligence_mpnet
```

### **Project Documentation**
```bash
qdrant-find "system architecture overview" {project}_docs_mpnet
qdrant-find "deployment workflow" {project}_docs_mpnet
```

---

## 📚 Collection Governance

### **hish_framework_mpnet**
- **Content**: Framework documentation, agent workflows, development standards
- **Update Frequency**: When framework docs change
- **Indexed From**: `hish/` repository markdown files

### **cross_project_intelligence_mpnet**
- **Content**: Validated patterns, cross-project learnings, taxonomies
- **Update Frequency**: On-demand via `qdrant-store` (with approval)
- **Lifecycle**: Manual curation, periodic review

### **{project}_docs_mpnet**
- **Content**: Project-specific documentation, context, decisions
- **Update Frequency**: When project docs change
- **Indexed From**: `{project}/docs/`, `{project}/*.md`, AGENTS.md synopses

---

## ✅ Quality Checklist

Before storing any pattern, verify:
- [ ] Pattern is validated (working in production or tests)
- [ ] Documentation is clear and actionable
- [ ] Evidence supports claims (metrics, references)
- [ ] Sensitive information removed
- [ ] User has reviewed and approved
- [ ] Appropriate collection selected
- [ ] Cross-project value is clear

---

**Next Steps:**
- See `templates/file-synopsis-workflows.md` for AGENTS.md synopsis generation workflows
- See `docs/collection-governance.md` for collection maintenance and lifecycle
- See `local/style-and-philosophy/cross-project-intelligence-architecture.md` for advanced usage
- See `docs/collection-governance.md` for maintenance procedures

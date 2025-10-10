# File Synopsis Workflows

## 🎯 Purpose

This guide defines automated workflows for generating and maintaining file synopses, particularly for AGENTS.md ecosystem discovery. **Synopses provide high-level context and pattern extraction without duplicating code.**

---

## 📋 AGENTS.md Synopsis Workflow

### **Automated Discovery Process**

The development agent automatically scans for AGENTS.md files during initialization:

```bash
## For each repository in local/*/repo_path.txt:
1. Scan recursively for all AGENTS.md files
2. Check existing synopsis (local/{repo}/agents_synopsis.md)
3. Compare file hashes (skip if unchanged - EFFICIENCY!)
4. Generate/update synopsis if needed
5. Store as local/{repo}/agents_synopsis.md
```

### **Synopsis Generation Steps**

**1. File Discovery**
```bash
# Find all AGENTS.md files
find /repo/path -type f -name "AGENTS.md"

# Output:
# /repo/path/AGENTS.md
# /repo/path/module/AGENTS.md
# /repo/path/service/AGENTS.md
```

**2. Content Extraction**
For each AGENTS.md file:
- Read file content
- Extract key sections (commands, architecture, patterns)
- Identify technical patterns
- Note important commands/workflows
- Calculate SHA256 hash

**3. Synopsis Generation**
```markdown
# AGENTS.md Synopsis - [Repository Name]

## Overview
[Brief description of repository scope and AGENTS.md ecosystem]

## Discovered Files
- `AGENTS.md` - [Main purpose and key commands]
- `module/AGENTS.md` - [Module-specific workflows]
- `service/AGENTS.md` - [Service-specific patterns]

## Key Technical Patterns
1. **Docker Multi-Stage Builds**: Optimization for Python dependencies
2. **Make-based Workflows**: Consistent command interface across services
3. **Environment-based Configuration**: 12-factor app principles

## Essential Commands
\`\`\`bash
# Build & Deploy
make build          # Build all containers
make deploy         # Deploy to production
make test           # Run full test suite

# Development
make dev            # Start development environment
make logs           # Tail service logs
make shell          # Interactive shell in container
\`\`\`

## Architecture Notes
- Microservices architecture with event-driven communication
- PostgreSQL for persistence, Redis for caching
- Docker Compose for local dev, Kubernetes for production

## File Hashes (for change detection)
- `AGENTS.md`: a1b2c3d4e5f6...
- `module/AGENTS.md`: f6e5d4c3b2a1...
- `service/AGENTS.md`: 123456789abc...

Generated: 2025-10-10T00:00:00Z
Last Verified: 2025-10-10T00:00:00Z
```

**4. Hash-Based Change Detection**
```python
import hashlib

def should_regenerate_synopsis(synopsis_file, agents_files):
    """Check if any AGENTS.md file changed since last synopsis."""
    if not synopsis_file.exists():
        return True

    # Parse existing hashes from synopsis
    existing_hashes = parse_hashes_from_synopsis(synopsis_file)

    # Calculate current hashes
    for agents_file in agents_files:
        current_hash = hashlib.sha256(agents_file.read_bytes()).hexdigest()
        if existing_hashes.get(agents_file.name) != current_hash:
            return True  # File changed

    return False  # No changes, skip regeneration
```

---

## 📝 Project Documentation Synopsis

### **Purpose**
Create high-level context documents that describe project architecture, decisions, and patterns **without duplicating code**.

### **When to Create**
- New project context initialization
- Major architectural changes
- After significant refactoring
- Quarterly documentation reviews

### **Template Usage**

**Location**: `local/{project}/project_context.md`

**Content Focus**:
1. **What** the project does (purpose, scope)
2. **Why** key decisions were made (architectural rationale)
3. **How** systems interact (high-level architecture)
4. **Where** to find things (critical files, entry points)

**Example**:
```markdown
# Project Context - User Authentication Service

## Purpose
Centralized authentication and authorization service for the platform.
Handles user registration, login, JWT token management, and role-based access control.

## Architecture
- **API Layer**: Express.js REST API
- **Auth Logic**: Passport.js strategies (local, OAuth2, JWT)
- **Storage**: PostgreSQL (users, roles), Redis (sessions, token blacklist)
- **External**: Integrates with email service for verification

## Key Design Decisions

### 1. JWT with Refresh Tokens
**Decision**: Use short-lived JWT access tokens (15min) + long-lived refresh tokens (7d)
**Rationale**:
- Balance security (short access token) with UX (fewer re-auths)
- Refresh tokens stored in HTTP-only cookies
- Blacklist implemented in Redis for logout/revocation

**Evidence**: Reduced support tickets for "logged out unexpectedly" by 80%

### 2. Redis Token Blacklist
**Decision**: Use Redis SET with TTL for invalidated tokens
**Rationale**:
- O(1) lookup performance
- Automatic cleanup via TTL (set to access token expiration)
- Handles logout, password reset, admin revocation

**Metrics**: 2ms P99 latency, 100k tokens/day

## Tech Stack
- **Language**: Node.js 20.x (TypeScript)
- **Framework**: Express.js 4.x
- **Database**: PostgreSQL 15
- **Cache**: Redis 7.x
- **Infrastructure**: Docker + Kubernetes

## Development Workflow
\`\`\`bash
# Setup
make setup          # Initialize database, install deps
make dev            # Start dev server with hot reload

# Testing
make test           # Run unit + integration tests
make test-coverage  # Generate coverage report (target: >90%)

# Deployment
make build          # Build production Docker image
make deploy-staging # Deploy to staging environment
\`\`\`

## Critical Files
- `src/auth/strategies/` - Passport.js authentication strategies
- `src/middleware/jwt.ts` - JWT validation + blacklist check
- `src/services/token.service.ts` - Token generation/validation logic
- `migrations/` - Database schema migrations

## Cross-Project Relevance
- **JWT + Refresh Pattern**: Reused in API Gateway, Admin Portal
- **Redis Blacklist**: Applied to rate limiting in other services
- **Role-Based Access**: Pattern adapted for multi-tenancy in SaaS platform

**Last Updated**: 2025-10-10T00:00:00Z
```

---

## 🔄 Maintenance Workflows

### **Weekly: Hash Verification**
```bash
# Run during agent initialization
# Automatically checks all repos for AGENTS.md changes
# Regenerates only if hashes don't match
```

### **Monthly: Context Review**
```bash
# Agent prompts:
"Review local/{project}/project_context.md for accuracy.
Check for outdated information, missing decisions, or new patterns."
```

### **Quarterly: Taxonomy Extraction**
```bash
# Extract patterns from all project contexts
# Identify cross-project patterns
# Update cross_project_intelligence collection
```

---

## ✅ Quality Standards

### **Synopsis Quality Checklist**
- [ ] Concise overview (2-3 sentences)
- [ ] All AGENTS.md files discovered and listed
- [ ] 3-5 key technical patterns extracted
- [ ] Essential commands documented with descriptions
- [ ] File hashes included for change detection
- [ ] Timestamp for tracking staleness

### **Context Quality Checklist**
- [ ] Clear purpose statement
- [ ] High-level architecture (no implementation details)
- [ ] Key decisions documented with rationale + evidence
- [ ] Tech stack versions specified
- [ ] Critical files identified with purpose
- [ ] Cross-project learnings extracted
- [ ] No sensitive information (API keys, passwords)

---

## 🚀 Automation Opportunities

### **Git Hook Integration** (Future Enhancement)
```bash
# .git/hooks/post-merge
# Trigger synopsis regeneration when AGENTS.md changes
if git diff --name-only HEAD@{1} HEAD | grep -q "AGENTS.md"; then
  echo "AGENTS.md changed, mark for synopsis regeneration"
  touch .agents-md-changed
fi
```

### **CI/CD Integration** (Future Enhancement)
```yaml
# .github/workflows/docs-sync.yml
# Automatically index documentation changes
on:
  push:
    paths:
      - 'docs/**'
      - '*.md'
      - 'AGENTS.md'
jobs:
  reindex-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Trigger Hish reindex
        run: make index-framework
```

---

**Next Steps:**
- See `templates/pattern-taxonomy-guide.md` for pattern extraction guidelines
- See `docs/collection-governance.md` for collection lifecycle management
- See `prompts/dev_agent/dev_agent_init_prompt.md` for AGENTS.md discovery automation

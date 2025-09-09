# Collection Governance Guide

## Overview

The Hish framework uses three distinct types of knowledge collections, each with specific purposes and governance rules. This document establishes clear boundaries to maintain collection integrity and effectiveness.

## Collection Types & Governance

### 1. Framework Collection (`hish_framework_mpnet`)

**Purpose**: Vectorized framework documentation only

**Content Rules**:
- ✅ **INCLUDE**: Official framework documentation (README.md, setup guides, configuration docs)
- ✅ **INCLUDE**: Framework templates and examples
- ✅ **INCLUDE**: Agent prompts and personas
- ❌ **EXCLUDE**: Learnings, patterns, or insights (these belong in cross-project intelligence)
- ❌ **EXCLUDE**: Project-specific knowledge
- ❌ **EXCLUDE**: Debugging workflows or operational procedures

**Governance**:
- Content is automatically vectorized from framework documentation files
- Use `make index-framework` for updates
- PRESERVES existing data (non-destructive)
- Only framework maintainers should modify source documentation

### 2. Cross-Project Intelligence (`cross_project_intelligence_mpnet`)

**Purpose**: Validated patterns and insights applicable to the framework OR 2+ projects

**Content Rules**:
- ✅ **INCLUDE**: Architecture patterns observed across multiple projects
- ✅ **INCLUDE**: Infrastructure debugging methodologies
- ✅ **INCLUDE**: Deployment patterns and best practices
- ✅ **INCLUDE**: Performance optimization techniques
- ✅ **INCLUDE**: Framework improvement insights
- ❌ **EXCLUDE**: Project-specific solutions (unless pattern applies to 2+ projects)
- ❌ **EXCLUDE**: One-off fixes or configurations
- ❌ **EXCLUDE**: Unvalidated hypotheses

**Governance**:
- Manual curation required - use `qdrant-store` tool
- Each entry must demonstrate cross-project applicability
- Include evidence and validation status
- Pattern format: Solution → Context → Implementation → Performance → Cross-Project Observations → Evidence → Validation Needed

### 3. Project Code Collections (`{project}_code_mpnet`)

**Purpose**: Searchable codebase content for specific projects

**Content Rules**:
- ✅ **INCLUDE**: Source code files (.py, .scala, .java, .ts, etc.)
- ✅ **INCLUDE**: Configuration files and infrastructure code
- ✅ **INCLUDE**: Project documentation and READMEs
- ❌ **EXCLUDE**: Test files and test data (performance optimization)
- ❌ **EXCLUDE**: Build artifacts and dependencies
- ❌ **EXCLUDE**: Large data files and logs

**Governance**:
- Automated via `make index` or `./reindex {project}`
- DESTRUCTIVE updates (collections are recreated)
- Managed per-project by context owners

## Collection Boundaries

### Framework vs Cross-Project Intelligence

**Question**: "Should this go in framework docs or cross-project intelligence?"

- **Framework**: If it's documentation about how to use the framework
- **Cross-Project**: If it's a validated pattern or insight that improves how we work

**Examples**:
- Framework setup instructions → **Framework**
- Authentication flow documentation → **Framework**
- Performance optimization pattern observed across projects → **Cross-Project Intelligence**
- Infrastructure debugging methodology → **Cross-Project Intelligence**

### Cross-Project vs Project-Specific

**Question**: "Is this insight applicable beyond one project?"

- **Cross-Project**: Pattern applies to framework improvement OR observed in 2+ projects
- **Project-Specific**: Solution only applies to one specific project or context

**Examples**:
- Docker optimization technique used in 3 projects → **Cross-Project Intelligence**
- Specific service configuration for one project → **Project Code Collection**
- AWS authentication pattern used across infrastructure → **Cross-Project Intelligence**

## Enforcement

### Automated Enforcement
- Framework collection: Automatically enforced via file patterns in `config/env.mpnet`
- Code collections: Automatically enforced via exclusion patterns in `config/env.mpnet.code`

### Manual Review Required
- Cross-project intelligence entries require manual validation before storage
- Each entry should include evidence of cross-project applicability
- Validation status should be documented

### Tools
- **Framework**: `make index-framework`
- **Cross-Project**: `qdrant-store` tool with manual curation
- **Code**: `make index` or `./reindex {project}`

## Migration Guidelines

When existing content doesn't follow these rules:

1. **Framework collection cleanup**: Remove any learnings/patterns, migrate to cross-project intelligence
2. **Cross-project validation**: Review existing entries, remove project-specific items
3. **Documentation updates**: Ensure all references reflect new governance model

This governance model ensures clean separation of concerns and maintains the quality and relevance of each knowledge collection.

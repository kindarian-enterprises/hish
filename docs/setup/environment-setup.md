# 🔧 Environment Setup for Kindarian Framework

**Complete guide to configuring environment variables for the framework.**

## 📁 **Required Environment Files**

**⚠️ IMPORTANT: These exact filenames are required by the framework and cannot be changed.**

The framework requires these exact environment files to function properly:

### **`env.framework` - Main Configuration**
**Purpose:** Primary configuration for framework operation and knowledge indexing.

**File location:** `kindarian-cursor-context/env.framework`

**Required values:**
```bash
# Qdrant Vector Database Configuration
QDRANT_URL=http://qdrant:6333          # Vector database URL (Docker internal)
QDRANT_API_KEY=                        # API key if authentication enabled (empty = no auth)
QDRANT_STORAGE=.data/qdrant            # Local storage path for Qdrant data

# Knowledge Collection Configuration
COLLECTION_NAME=kindarian_framework    # Default collection name for framework content
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2  # Text embedding model

# File Indexing Configuration
INDEX_INCLUDE=**/*.md,**/*.mdx,**/*.txt,contexts/**/*,docs/**/*,workflows-and-processes/**/*
# What gets indexed:
# - All markdown files in any directory
# - All context files (personas, project contexts)
# - All documentation files
# - All workflow and process files

INDEX_EXCLUDE=**/.git/**,**/.data/**,**/node_modules/**,**/.venv/**,**/dist/**,**/build/**,**/__pycache__/**,**/venv/**,**/.pytest_cache/**
# What gets excluded:
# - Git metadata
# - Framework data directories
# - Node.js dependencies
# - Python virtual environments
# - Build artifacts
# - Python cache files

# Text Chunking Configuration
CHUNK_MAX_TOKENS=300                   # Maximum tokens per knowledge chunk
CHUNK_MIN_CHARS=200                    # Minimum characters per chunk
CHUNK_OVERLAP_TOKENS=40                # Token overlap between chunks for context

# MCP Server Configuration
MCP_SSE_PORT=8000                      # Port for MCP server (if using SSE mode)
```

### **`env.code` - Code Repository Indexing**
**Purpose:** Configuration for indexing external code repositories and projects.

**File location:** `kindarian-cursor-context/env.code`

**Required filename:** Must be exactly `env.code`

**Note:** The Docker Compose file (`compose.rag.yml`) references this exact filename for the code indexing service.

**Required values:**
```bash
# Collection Configuration
COLLECTION_NAME=external_code           # Collection name for external code repositories

# File Indexing Configuration
INDEX_INCLUDE=**/*.py,**/*.yaml,**/*.yml,**/*.json,**/*.md,**/*.js,**/*.ts,**/*.go,**/*.rs,**/*.scala,**/*.java,**/*.c,**/*.cpp,**/*.cc,**/*.cxx,**/*.h,**/*.hpp
# What gets indexed:
# - Python source files
# - YAML/JSON configuration files
# - Markdown documentation
# - JavaScript/TypeScript files
# - Go source files
# - Rust source files
# - Scala source files
# - Java source files
# - C source files
# - C++ source files (cpp, cc, cxx)
# - Header files (h, hpp)

INDEX_EXCLUDE=**/.git/**,**/node_modules/**,**/__pycache__/**,**/target/**,**/dist/**,**/build/**,**/out/**,**/bin/**,**/obj/**
# What gets excluded:
# - Git metadata
# - Node.js dependencies
# - Python cache files
# - Rust/Java build artifacts (target/)
# - Distribution files (dist/)
# - Build directories (build/, out/, bin/, obj/)
```

### **`env.example` - Template**
**Purpose:** Template file showing all required environment variables with example values.

**File location:** `kindarian-cursor-context/env.example`

**Required filename:** Must be exactly `env.example`

**Note:** This file is referenced by the framework setup scripts and must exist for proper operation.

**Usage:** Copy this file to `env.framework` and modify values as needed.
```bash
cp env.example env.framework
```

## 🎯 **How Environment Variables Are Used**

### **Collection Names**
**`COLLECTION_NAME`** determines where indexed content is stored:

- **`kindarian_framework`** - Framework documentation, contexts, and workflows
- **`external_code`** - External code repositories and projects
- **`{project_name}_code`** - Specific project source code (e.g., `my_webapp_code`)
- **`{project_name}_docs`** - Specific project documentation (e.g., `my_webapp_docs`)

**Example:** Setting `COLLECTION_NAME=react_patterns` will store all indexed content in a collection called "react_patterns"

### **Indexing Patterns**
**`INDEX_INCLUDE`** controls which files get processed:

- **`**/*.md`** - All markdown files in any directory
- **`contexts/**/*`** - All context files (personas, project contexts)
- **`docs/**/*`** - All documentation files
- **`workflows-and-processes/**/*`** - All workflow and process files

**`INDEX_EXCLUDE`** controls which files are ignored:

- **`**/.git/**`** - Git metadata and history
- **`**/node_modules/**`** - Node.js dependencies
- **`**/__pycache__/**`** - Python cache files
- **`**/.venv/**`** - Python virtual environments

**Pattern syntax:** Uses glob patterns where `**` means "any directory depth" and `*` means "any filename"

### **Embedding Models**
**`EMBEDDING_MODEL`** controls the AI model used to convert text to vectors:

- **`sentence-transformers/all-MiniLM-L6-v2`** - Fast, good quality (default, 384 dimensions)
- **`BAAI/bge-small-en-v1.5`** - Higher quality, slower (768 dimensions)
- **Custom models** - Any sentence-transformers compatible model

**Performance trade-offs:**
- **Smaller models** (384d): Faster indexing, lower memory usage, good for most use cases
- **Larger models** (768d+): Better quality embeddings, slower indexing, higher memory usage

## 🚀 **Step-by-Step Setup**

### **1. Copy Environment Template**
```bash
cd kindarian-cursor-context
cp env.example env.framework
```

### **2. Review and Customize**
```bash
# View current settings
cat env.framework

# Edit with your preferred text editor
nano env.framework
# or
code env.framework
```

### **3. Verify Configuration**
```bash
# Check if services can start
make health

# Test indexing with a small collection
make index-repo REPO_PATH=. COLLECTION_NAME=test_collection
```

### **4. Start Framework**
```bash
# Launch all services
make up

# Check service status
make health
```

## 🔍 **Complete Environment Variables Reference**

| Variable | Default | Purpose | When to Change |
|----------|---------|---------|----------------|
| `QDRANT_URL` | `http://qdrant:6333` | Vector database connection | Only if using external Qdrant |
| `QDRANT_API_KEY` | (empty) | Database authentication | If Qdrant has auth enabled |
| `QDRANT_STORAGE` | `.data/qdrant` | Local data storage path | If you want different storage location |
| `COLLECTION_NAME` | `kindarian_framework` | Default knowledge collection | For different knowledge domains |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | AI model for text vectors | For different quality/speed trade-offs |
| `INDEX_INCLUDE` | `**/*.md,contexts/**/*,docs/**/*` | Files to process | To include/exclude specific file types |
| `INDEX_EXCLUDE` | `**/.git/**,**/.data/**` | Files to ignore | To ignore additional directories |
| `CHUNK_MAX_TOKENS` | `300` | Maximum chunk size | For different context window sizes |
| `CHUNK_MIN_CHARS` | `200` | Minimum chunk size | To avoid tiny, useless chunks |
| `CHUNK_OVERLAP_TOKENS` | `40` | Chunk overlap | For better context continuity |
| `MCP_SSE_PORT` | `8000` | MCP server port | If port 8000 is already in use |

## 🎯 **Collection Naming Strategy**

**Collections are created automatically during indexing:**

- **`kindarian_framework`** - Framework documentation, contexts, and workflows
- **`external_code`** - External code repositories (default for env.code)
- **`{project_name}_code`** - Project source code (e.g., `my_webapp_code`)
- **`{project_name}_docs`** - Project documentation (e.g., `my_webapp_docs`)
- **`{technology}_patterns`** - Technology-specific patterns (e.g., `react_patterns`)

**Example:** Indexing a React project with `COLLECTION_NAME=my_webapp_code` creates a collection called "my_webapp_code"

## 🔧 **Common Customization Scenarios**

### **Web Development Focus**
```bash
# Include frontend file types
INDEX_INCLUDE=**/*.md,**/*.js,**/*.ts,**/*.jsx,**/*.tsx,**/*.css,**/*.html,contexts/**/*,docs/**/*
COLLECTION_NAME=web_development_patterns
```

### **API Development Focus**
```bash
# Include backend file types
INDEX_INCLUDE=**/*.md,**/*.py,**/*.go,**/*.java,**/*.scala,**/*.c,**/*.cpp,**/*.cs,**/*.rb,contexts/**/*,docs/**/*
COLLECTION_NAME=api_development_patterns
```

### **Mobile Development Focus**
```bash
# Include mobile file types
INDEX_INCLUDE=**/*.md,**/*.swift,**/*.kt,**/*.dart,**/*.js,contexts/**/*,docs/**/*
COLLECTION_NAME=mobile_development_patterns
```

### **JVM Development Focus**
```bash
# Include JVM languages
INDEX_INCLUDE=**/*.md,**/*.java,**/*.scala,**/*.kt,**/*.groovy,contexts/**/*,docs/**/*
COLLECTION_NAME=jvm_development_patterns
```

### **Systems Programming Focus**
```bash
# Include systems programming languages
INDEX_INCLUDE=**/*.md,**/*.c,**/*.cpp,**/*.cc,**/*.cxx,**/*.h,**/*.hpp,**/*.rs,**/*.go,contexts/**/*,docs/**/*
COLLECTION_NAME=systems_programming_patterns
```

## 🚨 **Important Notes**

- **No configuration files needed** - agents discover context automatically
- **Collections are created** during indexing based on `COLLECTION_NAME`
- **Environment variables** control indexing behavior and scope
- **Indexing patterns** determine what content gets processed
- **Chunking settings** affect knowledge retrieval quality

## 🔍 **Troubleshooting Common Issues**

### **Indexing Too Many Files**
**Problem:** Indexing takes forever or includes unwanted files
**Solution:** Make `INDEX_INCLUDE` more specific
```bash
# Instead of indexing everything
INDEX_INCLUDE=**/*.md,**/*.py,**/*.js

# Be specific about what you want
INDEX_INCLUDE=src/**/*.py,tests/**/*.py,docs/**/*.md
```

### **Poor Search Results**
**Problem:** Queries return irrelevant or incomplete results
**Solution:** Adjust chunking parameters
```bash
# Smaller chunks for precise results
CHUNK_MAX_TOKENS=200
CHUNK_MIN_CHARS=100

# Larger chunks for context
CHUNK_MAX_TOKENS=500
CHUNK_MIN_CHARS=300
```

### **Slow Indexing**
**Problem:** Indexing takes hours instead of minutes
**Solution:** Use smaller embedding model or reduce scope
```bash
# Faster model (384 dimensions)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Reduce file scope
INDEX_INCLUDE=**/*.md,contexts/**/*  # Only markdown and contexts
```

### **Memory Issues**
**Problem:** Indexer crashes with out-of-memory errors
**Solution:** Reduce chunk size and batch processing
```bash
# Smaller chunks
CHUNK_MAX_TOKENS=150
CHUNK_MIN_CHARS=100

# The indexer automatically handles batching
```

### **Debug Mode**
```bash
# Enable debug logging for troubleshooting
make index-repo REPO_PATH=. COLLECTION_NAME=debug --debug
```

---

## 📋 **Quick Reference**

**Required files with exact names:**
1. **`env.framework`** - Main framework configuration
2. **`env.code`** - Code repository indexing (referenced by `compose.rag.yml`)
3. **`env.example`** - Template file (referenced by framework scripts)

**Essential files to configure:**
- **`env.framework`** - Main framework configuration
- **`env.code`** - External code repository indexing
- **`env.example`** - Template with all variables

**Key variables to understand:**
- **`COLLECTION_NAME`** - Where knowledge gets stored
- **`INDEX_INCLUDE`** - What files get processed
- **`EMBEDDING_MODEL`** - AI model for text understanding

## 🔒 **Why Filenames Are Fixed**

**The framework requires exact filenames because:**

1. **Docker Compose references** - `compose.rag.yml` expects `env.framework` for framework indexing and `env.code` for code indexing
2. **Framework scripts** - Setup and indexing scripts reference specific filenames
3. **Service configuration** - Different services use different environment files
4. **Consistency** - Prevents configuration errors and ensures proper operation

**Do not rename these files** - the framework will not work with different filenames.

---

**The environment configuration controls indexing behavior and knowledge organization. Start with the defaults, then customize based on your specific needs.**

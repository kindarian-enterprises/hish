# Environment Setup

## Required Files

### `config/env.framework`
```bash
QDRANT_URL=http://qdrant:6333
COLLECTION_NAME=hish_framework
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
INDEX_INCLUDE=**/*.md,contexts/**/*,docs/**/*
INDEX_EXCLUDE=**/.git/**,**/node_modules/**,**/.venv/**
CHUNK_MAX_TOKENS=350
CHUNK_MIN_CHARS=150
CHUNK_OVERLAP_TOKENS=70
```

### `config/env.code`
```bash
COLLECTION_NAME=external_code
INDEX_INCLUDE=**/*.py,**/*.js,**/*.ts,**/*.go,**/*.rs,**/*.java,**/*.md
INDEX_EXCLUDE=**/.git/**,**/node_modules/**,**/__pycache__/**,**/target/**,**/dist/**
```

### `config/env.mcp`
```bash
QDRANT_URL=http://localhost:6333
VECTOR_NAME=BAAI/bge-small-en-v1.5
```

## Setup

1. **Copy template**: `cp config/env.example config/env.framework`
2. **Edit values**: Modify `config/env.framework` as needed

**Note**: Services start automatically with Cursor integration. File names are fixed - referenced by MCP configuration.
# Data Management (Local-first Defaults)

<!-- 
Repo Scan Results - Existing Local/State Directories:
- ../.data/qdrant/ — Qdrant vector database storage (ignored, parent dir)
- mcp/ — MCP server configuration (tracked, code/config)
- rag/ — RAG indexer code (tracked, code)
-->

## Local-only (ignored) data
The following directories are intended for machine/user-specific or ephemeral data and are ignored by Git:

- `../.data/qdrant/` — Qdrant vector database storage (parent directory, not in repo)
- `local/` — Machine-specific overrides and configurations
- `overrides/` — User-specific configuration overrides
- `private/` — Private keys, tokens, and sensitive data
- `tmp/` — Temporary files and caches
- `scratch/` — Development scratch work and experiments

Keep private caches, runtime state, or throwaway files here. They will not be pushed or pulled.

## Optional: Version large/shared data with Git LFS
Use LFS only if you need to share large data (models, datasets, artifacts) via Git.
```bash
# one-time (per machine)
git lfs install

# example: track large artifacts under data/
git lfs track "data/**"
git add .gitattributes
git commit -m "Track large files under data/ with LFS"
```

**Use LFS when** files are large (>100MB) and shared.
**Keep local when** files are private, machine-specific, or cache-like.

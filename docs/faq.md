# FAQ

**Do I need Git LFS?**  
No. It's optional. Use it only to share large files (models/datasets). Otherwise keep data in ignored folders.

**Where do I put machine-specific or private files?**  
Use the ignored paths listed in `docs/data-management.md` (e.g., `local/`, `overrides/`, `private/`), which match this repo's conventions.

**How do I get updates from the main repo?**  
Since you cloned directly from the main repo, just:
```bash
git fetch origin
git merge origin/main
```

Or run `./scripts/sync-upstream.sh`.

**I keep getting conflicts on my local tweaks.**
Move those tweaks into an ignored local folder so they won't collide with upstream updates.

**Where is the Qdrant data stored?**
Qdrant data is stored in `../.data/qdrant/` (parent directory) and is not tracked by this repository. This keeps the vector database separate from the framework code.

**Can I customize the MCP server configuration?**
Yes, the `mcp/` directory contains configuration files that are tracked. For runtime state or local overrides, use the ignored paths like `local/` or `overrides/`.

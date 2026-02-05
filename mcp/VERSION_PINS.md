# MCP Server Version Pins

## Why Version Pinning?

The MCP server Docker image uses pinned versions to prevent breaking changes from upstream dependencies. This ensures the MCP server initialization is reliable across fresh installations.

## Pinned Versions (as of 2024-12-17)

### Core Dependencies

| Package | Version | Reason |
|---------|---------|--------|
| `qdrant-llamaindex-mcp-server` | 0.1.2 | Base MCP server |
| `fastmcp` | 2.12.5 | **CRITICAL** - Breaking changes in 2.13+ cause `KeyError: 'ctx'` on Mac |
| `pydantic` | 2.12.3 | Compatibility with fastmcp 2.12.5 |
| `pydantic-core` | 2.41.4 | Compatibility with pydantic 2.12.3 |

### Embedding Model
- `fastembed` - Latest compatible version (installed system-wide)
- Model: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (pre-warmed in image)

## Known Issues

### fastmcp >= 2.13.0 Breaking Changes

**Error:**
```
KeyError: 'ctx'
  File "fastmcp/tools/tool.py", line 463, in from_function
  File "pydantic/_internal/_generate_schema.py", line 1986, in _arguments_schema
    annotation = type_hints[name]
```

**Root Cause:**
fastmcp 2.13+ changed how it handles function parameter type hints, specifically around context (`ctx`) parameters. This breaks compatibility with the current qdrant-llamaindex-mcp-server implementation.

**Platform Impact:**
- **Linux (working)**: Local build with fastmcp 2.12.5
- **macOS (failing)**: Fresh installs pull fastmcp >= 2.13.0

**Symptoms if unpinned:**
- MCP server fails to start with JSON-RPC protocol errors
- Cursor shows "MCP server failed to initialize" errors
- Users with fresh clones cannot use `qdrant-find` tool

**Resolution:**
Pin to `fastmcp==2.12.5` which is the last known stable version.

## Installation Approach

**Current:** uv tool install + uv pip install system-wide dependencies + uv tool run invocation

**Why:**
- `uv tool install` creates the qdrant-llamaindex-mcp-server tool
- `uv pip install --system` installs pinned dependencies (fastmcp, pydantic) system-wide
- The tool must be invoked via `uv tool run` (not direct binary) to ensure correct environment
- Container CMD and compose command both use `uv tool run` to ensure proper execution

**Critical:** Running `qdrant-llamaindex-mcp-server` directly will use PATH resolution and may bypass pinned dependencies. Always invoke via `uv tool run`.

**Implementation:**
- Dockerfile CMD: `["uv", "tool", "run", "qdrant-llamaindex-mcp-server", "--transport", "stdio"]`
- compose.rag.yml command: `["uv", "tool", "run", "qdrant-llamaindex-mcp-server", "--transport", "stdio"]`

## Testing Version Pins

**Verify installed versions:**
```bash
# Check installed versions in tool venv
docker run --rm hish-mcp-unified:latest \
  /root/.local/share/uv/tools/qdrant-llamaindex-mcp-server/bin/python -m pip list | \
  grep -E 'qdrant|fastmcp|pydantic'

# Test MCP server starts via uv tool run
docker compose -f deploy/compose.rag.yml run --rm mcp-qdrant-unified
```

## Testing New Versions

Before upgrading any pinned version:

1. **Build new image:**
   ```bash
   docker compose -f deploy/compose.rag.yml build mcp-qdrant-unified
   ```

2. **Test MCP server initialization:**
   ```bash
   echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | \
     docker compose -f deploy/compose.rag.yml run --rm -i mcp-qdrant-unified
   ```

3. **Verify response includes:**
   - `"result"` with protocol version
   - Server info with capabilities
   - No errors or warnings

4. **Test in Cursor:**
   - Restart Cursor after rebuilding image
   - Run `qdrant-find "test query" hish_framework_mpnet`
   - Verify results return successfully

5. **Test on both platforms:**
   - Linux (current dev environment)
   - macOS (user's Mac)

## Updating Pins

If you need to update versions:

1. Check upstream issues:
   - https://github.com/qdrant/qdrant-llamaindex-mcp-server
   - https://github.com/jlowin/fastmcp

2. Update `mcp/Dockerfile.llamaindex` with new versions

3. Test in isolated environment:
   ```bash
   docker build -t test-mcp -f mcp/Dockerfile.llamaindex .
   docker run --rm test-mcp qdrant-llamaindex-mcp-server --version
   ```

4. Test thoroughly using steps above

5. Update this file with rationale and date

6. Document any new known issues

## History

- **2024-12-17**: Initial version pins added to prevent fastmcp 2.13+ breaking changes and ensure reliable MCP initialization across fresh installations
- **2024-10-22**: Working Linux build versions identified and validated

# MCP Server Version Pins

## Why Version Pinning?

The MCP server Docker image uses pinned versions to prevent breaking changes from upstream dependencies. This ensures the MCP server initialization is reliable across fresh installations.

## Pinned Versions (as of 2024-12-17)

### Core Dependencies
- `qdrant-llamaindex-mcp-server==0.1.2` - MCP server implementation
- `pydantic==2.12.3` - Data validation (fastmcp dependency)
- `pydantic-core==2.41.4` - Pydantic core library
- `fastmcp==2.12.5` - **CRITICAL PIN** - fastmcp 2.13+ has breaking changes

### Embedding Model
- `fastembed` - Latest compatible version (installed system-wide)
- Model: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (pre-warmed in image)

## Known Issues

### fastmcp 2.13+ Breaking Changes
**Problem:** fastmcp versions 2.13 and newer introduce breaking API changes that cause MCP server initialization failures.

**Solution:** Pin to `fastmcp==2.12.5` which is the last known stable version.

**Symptoms if unpinned:**
- MCP server fails to start with JSON-RPC protocol errors
- Cursor shows "MCP server failed to initialize" errors
- Users with fresh clones cannot use `qdrant-find` tool

### UV Tool Wrapper Required
**Problem:** Direct command `qdrant-llamaindex-mcp-server` doesn't always use the correct virtual environment with pinned dependencies.

**Solution:** Use `uv tool run qdrant-llamaindex-mcp-server` wrapper which ensures the correct venv is activated.

**Implementation:**
- Dockerfile CMD: `["uv", "tool", "run", "qdrant-llamaindex-mcp-server", "--transport", "stdio"]`
- compose.rag.yml command: `["uv", "tool", "run", "qdrant-llamaindex-mcp-server", "--transport", "stdio"]`

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

## Updating Pins

If you need to update versions:

1. Update `mcp/Dockerfile.llamaindex` with new versions
2. Update this file with rationale and date
3. Test thoroughly using steps above
4. Document any new known issues

## History

- **2024-12-17**: Initial version pins added to prevent fastmcp 2.13+ breaking changes and ensure reliable MCP initialization across fresh installations
- **2024-10-22**: Working Linux build versions identified and validated

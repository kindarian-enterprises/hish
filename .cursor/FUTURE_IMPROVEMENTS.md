# Future Improvements for Dual MCP Server Setup

## Current Approach (Working)

We use TWO instances of `qdrant-llamaindex-mcp-server` with:
- **Server namespacing**: `qdrant-mpnet:qdrant-find` vs `qdrant-jina:qdrant-find`
- **Cursor Rules (.mdc)**: Automatic routing heuristics
- **Hook**: Reinforces routing with collection list and examples

**Status**: This SHOULD work - Cursor's documentation confirms tools are namespaced by server name.

## Optimal Approach (If Current Doesn't Work Perfectly)

### Option 1: Custom Tool Names (Most Reliable)

Create a thin wrapper around `qdrant-llamaindex-mcp-server` that renames tools:

**qdrant-mpnet server exposes:**
- `text.search` instead of `qdrant-find`
- `text.store` instead of `qdrant-store`

**qdrant-jina server exposes:**
- `code.search` instead of `qdrant-find`
- `code.store` instead of `qdrant-store`

**Benefits:**
- Zero ambiguity - tool names themselves indicate purpose
- Agent can't accidentally call wrong server
- More intuitive for users too

**Implementation:**
- Fork `qdrant-llamaindex-mcp-server` OR
- Create thin proxy MCP server that wraps it OR
- Submit PR to upstream to support configurable tool names

### Option 2: Single MCP Server with Model Selection

Modify one server instance to:
- Accept `model: "mpnet" | "jina"` parameter in tool calls
- Route internally to correct embedding model
- Still use separate collections

**Benefits:**
- Simpler configuration (one server)
- No namespace confusion

**Drawbacks:**
- Requires significant modification to server
- Less clear separation of concerns

## Why We're Not Doing This Now

1. **Pre-built server**: `qdrant-llamaindex-mcp-server` is maintained upstream
2. **Should work as-is**: Cursor's MCP implementation supports server namespacing
3. **Testing first**: Want to verify current approach before adding complexity
4. **Maintenance burden**: Wrapper/fork adds maintenance overhead

## When to Revisit

If after testing we see:
- Agent frequently calls wrong server despite rules
- "Wrong input: Vector" errors persist
- Confusion in agent responses about which tool to use

Then implement Option 1 (custom tool names) as it's the most robust solution per Cursor's best practices.

## References

- [Cursor MCP - Building an MCP Server](https://docs.cursor.com/en/guides/tutorials/building-mcp-server)
- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- [Optimizing Tool Selection with Cursor Rules](https://github.com/hyperskill/enlighter-content/blob/main/project_11_how_to_build_your_first_mcp_server/18_187_optimizing_tool_selection_with_cursor_rules.html)
- [qdrant-llamaindex-mcp-server GitHub](https://github.com/your-repo-here)

## Testing Checklist

Before considering improvements, verify:

1. ✅ Both servers show up in Cursor Tools pane
2. ✅ Tools appear with server prefixes (`qdrant-mpnet:*`, `qdrant-jina:*`)
3. ✅ Rules file (`.mdc`) is loaded (check Cursor settings)
4. ✅ Hook is injecting preamble correctly (check logs)
5. ✅ Agent attempts server-namespaced calls
6. ✅ No "Wrong input: Vector" errors
7. ✅ Code queries use Jina, docs queries use MPNet

If all ✅, current approach is optimal!
If some ❌, consider implementing Option 1.

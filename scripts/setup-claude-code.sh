#!/bin/bash
# Setup Hish integration for Claude Code
# Usage: ./scripts/setup-claude-code.sh [project-path]
#        ./scripts/setup-claude-code.sh --install-only   (create venv + install MCP bridge only)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get Hish root (where this script lives)
HISH_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$HISH_ROOT/.venv-claude-mcp"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# --- Optional: install-only mode (venv + pip install, no project setup) ---
if [ "${1:-}" = "--install-only" ]; then
    echo -e "${GREEN}📦 Hish Claude Code MCP – install into virtualenv${NC}"
    echo "=========================================="
    echo "Hish Root: $HISH_ROOT"
    echo "Venv:      $VENV_DIR"
    echo ""

    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}Creating virtualenv...${NC}"
        python3 -m venv "$VENV_DIR"
        echo "  ✅ Created $VENV_DIR"
    else
        echo "  ✅ Virtualenv exists: $VENV_DIR"
    fi

    echo -e "${YELLOW}Installing hish-bridge-mcp...${NC}"
    "$VENV_DIR/bin/pip" install -e "$HISH_ROOT/mcp/hish-bridge"
    echo "  ✅ hish_bridge_mcp installed"

    if "$VENV_DIR/bin/python" -c "import hish_bridge_mcp" 2>/dev/null; then
        echo ""
        echo -e "${GREEN}✅ Done. Use this Python for MCP: $VENV_DIR/bin/python${NC}"
    else
        echo -e "${RED}Import check failed.${NC}"
        exit 1
    fi
    exit 0
fi

# Get project path (default to current directory)
PROJECT_PATH="${1:-.}"
PROJECT_PATH="$(cd "$PROJECT_PATH" && pwd)"
PROJECT_NAME="$(basename "$PROJECT_PATH")"

echo -e "${GREEN}🧠 Hish Claude Code Setup${NC}"
echo "=========================="
echo "Hish Root: $HISH_ROOT"
echo "Project:   $PROJECT_PATH"
echo "Project:   $PROJECT_NAME"
echo ""

# --- Step 0: Ensure virtualenv and MCP bridge ---
echo -e "${YELLOW}Step 0: Ensuring MCP bridge virtualenv${NC}"

if [ ! -d "$VENV_DIR" ]; then
    echo "  Creating virtualenv at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
    echo "  ✅ Virtualenv created"
fi

if ! "$VENV_DIR/bin/python" -c "import hish_bridge_mcp" 2>/dev/null; then
    echo "  Installing hish-bridge-mcp into venv ..."
    "$VENV_DIR/bin/pip" install -e "$HISH_ROOT/mcp/hish-bridge"
    echo "  ✅ hish_bridge_mcp installed"
else
    echo "  ✅ hish_bridge_mcp available in venv"
fi

# Absolute path to venv Python so .mcp.json invokes the server with this env only
PYTHON_CMD="$(cd "$HISH_ROOT" && pwd)/.venv-claude-mcp/bin/python"

# --- Step 1: Create CLAUDE.md ---
echo -e "${YELLOW}Step 1: Creating CLAUDE.md${NC}"

CLAUDE_MD_TEMPLATE="$HISH_ROOT/templates/claude-code/CLAUDE.md.template"
CLAUDE_MD_TARGET="$PROJECT_PATH/CLAUDE.md"

if [ ! -f "$CLAUDE_MD_TEMPLATE" ]; then
    echo -e "${RED}Error: Template not found: $CLAUDE_MD_TEMPLATE${NC}"
    exit 1
fi

# Replace placeholders
sed -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
    -e "s|{{HISH_ROOT}}|$HISH_ROOT|g" \
    -e "s|{{TIMESTAMP}}|$TIMESTAMP|g" \
    -e "s|{{QDRANT_URL}}|http://localhost:6333|g" \
    "$CLAUDE_MD_TEMPLATE" > "$CLAUDE_MD_TARGET"

echo "  ✅ Created: $CLAUDE_MD_TARGET"

# --- Step 2: Create .claude/commands/ ---
echo -e "${YELLOW}Step 2: Installing commands${NC}"

COMMANDS_DIR="$PROJECT_PATH/.claude/commands"
mkdir -p "$COMMANDS_DIR"

for template in "$HISH_ROOT/templates/claude-code/commands/"*.template; do
    if [ -f "$template" ]; then
        filename=$(basename "$template" .template)
        target="$COMMANDS_DIR/$filename"

        sed -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
            -e "s|{{HISH_ROOT}}|$HISH_ROOT|g" \
            -e "s|{{TIMESTAMP}}|$TIMESTAMP|g" \
            "$template" > "$target"

        echo "  ✅ Created: $target"
    fi
done

# --- Step 3: Create .mcp.json (use venv Python) ---
echo -e "${YELLOW}Step 3: Creating MCP configuration${NC}"

MCP_CONFIG="$PROJECT_PATH/.mcp.json"

# Use absolute path to venv Python so Claude Code runs the server with the correct env
cat > "$MCP_CONFIG" << EOF
{
  "mcpServers": {
    "hish-knowledge": {
      "command": "$PYTHON_CMD",
      "args": ["-m", "hish_bridge_mcp.server"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "HISH_ROOT": "$HISH_ROOT"
      }
    }
  }
}
EOF

echo "  ✅ Created: $MCP_CONFIG (server: venv Python)"

# --- Step 4: Verify Qdrant is running ---
echo -e "${YELLOW}Step 4: Checking Qdrant${NC}"

if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    echo "  ✅ Qdrant is running"
else
    echo -e "  ${YELLOW}⚠️  Qdrant not responding on localhost:6333${NC}"
    echo "  Start with: cd $HISH_ROOT && docker compose -f deploy/compose.rag.yml up -d qdrant"
fi

# --- Summary ---
echo ""
echo -e "${GREEN}✅ Hish Claude Code setup complete!${NC}"
echo ""
echo "Files created:"
echo "  - $CLAUDE_MD_TARGET"
echo "  - $COMMANDS_DIR/*.md"
echo "  - $MCP_CONFIG"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Code to load MCP configuration"
echo "  2. Use /dev command to initialize Hish agent"
echo "  3. Use hish_find() to query knowledge collections"
echo ""
echo "MCP server runs with: $PYTHON_CMD (virtualenv at $VENV_DIR)"
echo ""
echo "Add to .gitignore (optional):"
echo "  CLAUDE.md"
echo "  .mcp.json"

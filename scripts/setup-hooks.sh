#!/usr/bin/env bash
set -euo pipefail

# HISH Cursor Hooks Setup Script
# Installs cursor hooks with proper configuration paths

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HISH_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$HISH_ROOT/config"
HOOKS_SOURCE_DIR="$HISH_ROOT/.cursor/hooks"
HOOKS_INSTALL_DIR="$HOME/.cursor/hooks"

echo "🔧 HISH Cursor Hooks Setup"
echo "=========================="
echo "HISH Root: $HISH_ROOT"
echo "Config Dir: $CONFIG_DIR"
echo "Hooks Source: $HOOKS_SOURCE_DIR"
echo "Install Target: $HOOKS_INSTALL_DIR"
echo ""

# Verify config directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    echo "❌ Config directory not found: $CONFIG_DIR"
    exit 1
fi

# Verify required config files exist
if [ ! -f "$CONFIG_DIR/env.mpnet" ]; then
    echo "⚠️  Warning: env.mpnet not found in config directory"
fi

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_INSTALL_DIR"

# Ensure venv exists for hooks
if [ ! -d "$HOOKS_INSTALL_DIR/.venv" ]; then
    echo "📦 Creating Python virtual environment for hooks..."
    python3 -m venv "$HOOKS_INSTALL_DIR/.venv"
    "$HOOKS_INSTALL_DIR/.venv/bin/pip" install --quiet --upgrade pip
fi

# Copy hook scripts
echo "📋 Copying hook scripts..."
cp "$HOOKS_SOURCE_DIR/prioritize_local_data" "$HOOKS_INSTALL_DIR/prioritize_local_data"
cp "$HOOKS_SOURCE_DIR/protect_framework_collection" "$HOOKS_INSTALL_DIR/protect_framework_collection"
chmod +x "$HOOKS_INSTALL_DIR/prioritize_local_data"
chmod +x "$HOOKS_INSTALL_DIR/protect_framework_collection"

# Generate hooks.json
echo "⚙️  Generating hooks.json..."
cat > "$HOME/.cursor/hooks.json" <<EOF
{
  "version": 1,
  "hooks": {
    "beforeSubmitPrompt": [
      {
        "command": "~/.cursor/hooks/.venv/bin/python3 ~/.cursor/hooks/prioritize_local_data"
      }
    ],
    "beforeMCPExecution": [
      {
        "command": "~/.cursor/hooks/.venv/bin/python3 ~/.cursor/hooks/protect_framework_collection"
      }
    ]
  }
}
EOF

echo "✅ hooks.json generated"
echo ""

# Display generated hooks.json
echo "📄 Generated hooks.json:"
cat "$HOME/.cursor/hooks.json"
echo ""

echo "✅ Hooks setup complete!"
echo ""
echo "Installed hooks:"
echo "  • prioritize_local_data - Instructs agent to use local Qdrant collections"
echo "  • protect_framework_collection - Blocks writes to framework collections (read-only)"
echo ""

echo "🔌 MCP Architecture:"
echo "  • qdrant-unified server: Documentation/framework collections (MPNet embeddings)"
echo "  • Framework collections are READ-ONLY (rebuilt from markdown via 'make index-framework')"
echo "  • cross_project_intelligence is WRITABLE (agent-curated patterns with approval)"
echo ""
echo "To verify installation:"
echo "  ls -la $HOOKS_INSTALL_DIR/"
echo "  ls -la $HOME/.cursor/rules/"
echo "  cat $HOME/.cursor/hooks.json"
echo ""
echo "Debug logs will be written to: $HOME/.cursor/hook_debug.log"

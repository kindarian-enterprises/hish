#!/usr/bin/env bash
set -euo pipefail

# HISH Cursor Commands Setup Script
# Installs HISH custom commands to user's global Cursor commands directory
# Replaces {{HISH_ROOT}} placeholder with absolute path during installation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HISH_ROOT="$(dirname "$SCRIPT_DIR")"
COMMANDS_SOURCE_DIR="$HISH_ROOT/.cursor/commands"

echo "Installing commands..."

# Verify source directory exists
if [ ! -d "$COMMANDS_SOURCE_DIR" ]; then
    echo "❌ Commands source directory not found: $COMMANDS_SOURCE_DIR"
    exit 1
fi

# Use standard ~/.cursor/commands directory (per Cursor documentation)
COMMANDS_INSTALL_DIR="$HOME/.cursor/commands"

echo "Detected OS: $(uname -s)"
echo "Install Target: $COMMANDS_INSTALL_DIR"
echo ""

# Create commands directory if it doesn't exist
if [ ! -d "$COMMANDS_INSTALL_DIR" ]; then
    echo "📁 Creating commands directory..."
    mkdir -p "$COMMANDS_INSTALL_DIR"
    echo "✅ Directory created: $COMMANDS_INSTALL_DIR"
else
    echo "✅ Commands directory exists: $COMMANDS_INSTALL_DIR"
fi
echo ""

# Function to install a command with path substitution
install_command() {
    local source_file="$1"
    local command_name=$(basename "$source_file")
    local target_file="$COMMANDS_INSTALL_DIR/$command_name"

    echo "📋 Installing command: $command_name"

    # Replace {{HISH_ROOT}} with actual path and copy
    sed "s|{{HISH_ROOT}}|$HISH_ROOT|g" "$source_file" > "$target_file"

    # Verify installation
    if [ -f "$target_file" ]; then
        echo "   ✅ Installed: $target_file"
    else
        echo "   ❌ Failed to install: $command_name"
        return 1
    fi
}

# Install all command files
echo "📦 Installing commands..."
echo ""

install_command "$COMMANDS_SOURCE_DIR/dev.md"
install_command "$COMMANDS_SOURCE_DIR/red.md"
install_command "$COMMANDS_SOURCE_DIR/end-dev.md"
install_command "$COMMANDS_SOURCE_DIR/end-red.md"
install_command "$COMMANDS_SOURCE_DIR/verbalized-sampling.md"

echo ""
echo "✅ Commands setup complete!"
echo ""

echo "📝 Available Commands:"
echo "  Session Initialization:"
echo "    • /dev                  - Initialize Development Agent"
echo "    • /red                  - Initialize Red Team Agent"
echo ""
echo "  Session Management:"
echo "    • /end-dev              - End development session"
echo "    • /end-red              - End red team session"
echo ""
echo "  Creative Tools:"
echo "    • /verbalized-sampling  - Generate diverse tail-sampled responses"
echo ""

echo "🎯 Usage:"
echo "  1. Open Cursor (in any project)"
echo "  2. Open chat panel"
echo "  3. Type '/' to see all commands"
echo "  4. Select HISH command or type name"
echo "  5. Press Enter to execute"
echo "✅ Commands installed to ~/.cursor/commands/"

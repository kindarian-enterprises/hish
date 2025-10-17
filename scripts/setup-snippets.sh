#!/usr/bin/env bash
set -euo pipefail

# HISH Cursor Snippets Setup Script
# Installs HISH snippets to user's Cursor snippets directory
# Automatically detects OS and uses correct path

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HISH_ROOT="$(dirname "$SCRIPT_DIR")"
SNIPPETS_SOURCE="$HISH_ROOT/.cursor/snippets/hish.code-snippets"

echo "🎨 HISH Cursor Snippets Setup"
echo "============================="
echo "HISH Root: $HISH_ROOT"
echo "Source: $SNIPPETS_SOURCE"
echo ""

# Verify source file exists
if [ ! -f "$SNIPPETS_SOURCE" ]; then
    echo "❌ Source snippet file not found: $SNIPPETS_SOURCE"
    exit 1
fi

# Detect OS and set appropriate snippets directory
detect_snippets_dir() {
    case "$(uname -s)" in
        Darwin*)
            # macOS
            echo "$HOME/Library/Application Support/Cursor/User/snippets"
            ;;
        Linux*)
            # Linux
            echo "$HOME/.config/Cursor/User/snippets"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            # Windows (Git Bash, WSL, etc.)
            echo "$APPDATA/Cursor/User/snippets"
            ;;
        *)
            # Unknown OS - try Linux path as fallback
            echo "$HOME/.config/Cursor/User/snippets"
            ;;
    esac
}

SNIPPETS_INSTALL_DIR="$(detect_snippets_dir)"
SNIPPETS_INSTALL_FILE="$SNIPPETS_INSTALL_DIR/hish.code-snippets"

echo "Detected OS: $(uname -s)"
echo "Install Target: $SNIPPETS_INSTALL_DIR"
echo ""

# Create snippets directory if it doesn't exist
if [ ! -d "$SNIPPETS_INSTALL_DIR" ]; then
    echo "📁 Creating snippets directory..."
    mkdir -p "$SNIPPETS_INSTALL_DIR"
    echo "✅ Directory created: $SNIPPETS_INSTALL_DIR"
else
    echo "✅ Snippets directory exists: $SNIPPETS_INSTALL_DIR"
fi
echo ""

# Check if file already exists (update scenario)
if [ -f "$SNIPPETS_INSTALL_FILE" ]; then
    echo "🔄 Existing snippet file found - will overwrite"
    echo "   (This is normal when updating snippets)"
fi

# Copy snippet file
echo "📋 Copying snippet file..."
cp "$SNIPPETS_SOURCE" "$SNIPPETS_INSTALL_FILE"

# Set file permissions (read-only recommended to prevent accidental edits)
chmod 444 "$SNIPPETS_INSTALL_FILE"

echo "✅ Snippet file installed: $SNIPPETS_INSTALL_FILE"
echo ""

# Verify installation
if [ -f "$SNIPPETS_INSTALL_FILE" ]; then
    file_size=$(wc -c < "$SNIPPETS_INSTALL_FILE" | tr -d ' ')
    echo "✅ Installation verified! (${file_size} bytes)"
else
    echo "❌ Installation verification failed!"
    exit 1
fi

echo ""
echo "✅ Snippets setup complete!"
echo ""

echo "📝 Available Snippet Prefixes:"
echo "  Agent Initialization:"
echo "    • hdev      - Initialize Development Agent"
echo "    • hred      - Initialize Red Team Agent"
echo "    • hdevend   - End development session"
echo "    • hredend   - End red team session"
echo ""
echo "  Knowledge Discovery:"
echo "    • hinit     - All 4 mandatory initialization queries"
echo "    • hfw       - Search framework documentation"
echo "    • hint      - Search cross-project intelligence"
echo "    • hproj     - Search project documentation"
echo "    • hq        - Quick framework search (shortest)"
echo ""
echo "  Pattern Storage:"
echo "    • hstore    - Store pattern (after user approval)"
echo "    • hpattern  - Pattern storage review template"
echo "    • huuid     - Generate UUID for storage"
echo ""
echo "  Advanced:"
echo "    • hsession  - Full session template"
echo "    • hdiscover - Multi-collection discovery"
echo "    • hachieve  - Achievement entry template"
echo "    • hsearch   - Search with collection dropdown"
echo ""
echo "  Maintenance:"
echo "    • hcol      - List all collections"
echo "    • hreindex  - Reindex project documentation"
echo ""

echo "🎯 Usage:"
echo "  1. Restart Cursor to load snippets"
echo "  2. Type any prefix (e.g., 'hdev') in chat or editor"
echo "  3. Press Tab or Enter to expand"
echo "  4. Navigate placeholders with Tab"
echo ""

echo "🔄 To Update Snippets:"
echo "  cd $HISH_ROOT"
echo "  git pull"
echo "  make setup-cursor"
echo ""

echo "⚠️  IMPORTANT:"
echo "  • DO NOT manually edit: $SNIPPETS_INSTALL_FILE"
echo "  • Snippets are managed by HISH framework"
echo "  • Updates will overwrite your changes"
echo "  • Custom snippets should go in a separate file"
echo ""

echo "📚 Documentation: $HISH_ROOT/.cursor/snippets/README.md"
echo "🐛 Issues? Check file permissions and Cursor version"

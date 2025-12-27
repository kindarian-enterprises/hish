#!/bin/bash
# Hish - Link Local Portable Context
# Links an existing local portable context directory to local/

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

CONTEXT_PATH="$1"

if [[ -z "$CONTEXT_PATH" ]]; then
    print_error "Usage: $0 <context-path>"
    echo "Example: $0 ~/Dropbox/hish-context"
    echo "Example: $0 /mnt/nas/hish-context"
    exit 1
fi

# Expand ~ if present
CONTEXT_PATH="${CONTEXT_PATH/#\~/$HOME}"

echo "🔗 Hish - Link Local Portable Context"
echo "======================================"
echo ""
echo "Context path: $CONTEXT_PATH"
echo ""

# Verify context directory exists
if [[ ! -d "$CONTEXT_PATH" ]]; then
    print_error "Context directory not found: $CONTEXT_PATH"
    exit 1
fi

if [[ ! -d "$CONTEXT_PATH/.git" ]]; then
    print_warning "Not a git repository: $CONTEXT_PATH"
    print_warning "Consider initializing with: git init $CONTEXT_PATH"
fi

# Check if local/ already exists
if [[ -L "local" ]]; then
    existing_target=$(readlink "local")
    print_warning "local/ is already a symlink to: $existing_target"
    read -p "Replace with new path? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Aborted."
        exit 0
    fi
    rm local
elif [[ -d "local" ]]; then
    print_warning "local/ directory exists. This will be backed up."
    BACKUP_DIR="local.backup.$(date +%Y%m%d_%H%M%S)"
    mv local "$BACKUP_DIR"
    print_success "Backup created: $BACKUP_DIR"
fi

# Create symlink
print_info "Creating symlink: local -> $CONTEXT_PATH"
ln -sf "$CONTEXT_PATH" local
echo "$CONTEXT_PATH" > .hish-portable-context
print_success "Symlink created"

# Verify
if [[ -L "local" ]] && [[ -d "local" ]]; then
    print_success "✅ Local context linked successfully!"

    if [[ -d "$CONTEXT_PATH/.git" ]]; then
        echo ""
        echo "📝 Git repository detected. You can:"
        echo "   make context-push     # Commit and push changes"
        echo "   make context-pull     # Pull updates"
        echo "   make context-sync     # Bidirectional sync"
    fi
else
    print_error "Symlink verification failed!"
    exit 1
fi

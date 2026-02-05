#!/bin/bash
# Hish - Link Remote Portable Context
# Links an existing remote portable context repository to local/

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

REMOTE_URL="$1"
CONTEXT_REPO="${2:-$HOME/.hish-context}"

if [[ -z "$REMOTE_URL" ]]; then
    print_error "Usage: $0 <remote-url> [local-path]"
    echo "Example: $0 git@github.com:user/hish-context.git"
    exit 1
fi

echo "🔗 Hish - Link Remote Portable Context"
echo "======================================="
echo ""
echo "Remote URL: $REMOTE_URL"
echo "Local path: $CONTEXT_REPO"
echo ""

# Check if local/ already exists
if [[ -L "local" ]]; then
    existing_target=$(readlink "local")
    print_warning "local/ is already a symlink to: $existing_target"
    read -p "Replace with new remote? [y/N]: " -n 1 -r
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

# Clone remote repository
print_info "Cloning remote context repository..."
if [[ -d "$CONTEXT_REPO" ]]; then
    print_warning "Directory exists: $CONTEXT_REPO"
    read -p "Remove and clone fresh? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$CONTEXT_REPO"
    else
        print_error "Cannot proceed. Aborted."
        exit 1
    fi
fi

git clone "$REMOTE_URL" "$CONTEXT_REPO"
print_success "Cloned: $REMOTE_URL -> $CONTEXT_REPO"

# Create symlink
print_info "Creating symlink: local -> $CONTEXT_REPO"
ln -sf "$CONTEXT_REPO" local
echo "$CONTEXT_REPO" > .hish-portable-context
print_success "Symlink created"

# Verify
if [[ -L "local" ]] && [[ -d "local" ]]; then
    print_success "✅ Remote context linked successfully!"
    echo ""
    echo "📝 To sync changes:"
    echo "   make context-pull     # Pull updates from remote"
    echo "   make context-push     # Push local changes"
    echo "   make context-sync     # Bidirectional sync"
else
    print_error "Symlink verification failed!"
    exit 1
fi

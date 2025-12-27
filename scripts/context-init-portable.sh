#!/bin/bash
# Hish - Initialize Portable Context Repository
# Converts local/ directory to a separate git repository for cross-environment synchronization

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

echo "🔗 Hish - Portable Context Initialization"
echo "=========================================="
echo ""
echo "This converts your local/ directory into a separate git repository"
echo "that can be synchronized across multiple environments."
echo ""
echo "⚠️  IMPORTANT: This is OPTIONAL. Most users don't need this."
echo "   Only use if you work across multiple machines and want to sync context."
echo ""

# Check if local/ exists
if [[ ! -d "local" ]]; then
    print_error "local/ directory not found. Run 'make setup-framework' first."
    exit 1
fi

# Check if local/ is already a symlink
if [[ -L "local" ]]; then
    link_target=$(readlink "local")
    print_warning "local/ is already a symlink to: $link_target"
    echo ""
    read -p "Re-initialize portable context? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Aborted."
        exit 0
    fi
fi

# Get context repository location
echo "Where should the portable context repository be stored?"
echo "  1) ~/.hish-context (recommended - local to this machine)"
echo "  2) Custom path (e.g., ~/Dropbox/hish-context for cloud sync)"
echo "  3) Remote git repository (e.g., git@github.com:user/hish-context.git)"
echo ""
read -p "Choice [1-3]: " -n 1 -r choice
echo ""

case $choice in
    1)
        CONTEXT_REPO="$HOME/.hish-context"
        REPO_TYPE="local"
        ;;
    2)
        read -p "Enter custom path: " custom_path
        CONTEXT_REPO="${custom_path/#\~/$HOME}"  # Expand ~
        REPO_TYPE="local"
        ;;
    3)
        read -p "Enter git repository URL: " git_url
        CONTEXT_REPO="$HOME/.hish-context"
        REPO_TYPE="remote"
        REMOTE_URL="$git_url"
        ;;
    *)
        print_error "Invalid choice. Aborted."
        exit 1
        ;;
esac

echo ""
print_info "Context repository: $CONTEXT_REPO"
if [[ "$REPO_TYPE" == "remote" ]]; then
    print_info "Remote URL: $REMOTE_URL"
fi
echo ""
read -p "Continue? [y/N]: " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Aborted."
    exit 0
fi

# Step 1: Backup existing local/ directory
print_info "Backing up existing local/ directory..."
BACKUP_DIR="local.backup.$(date +%Y%m%d_%H%M%S)"
cp -r local "$BACKUP_DIR"
print_success "Backup created: $BACKUP_DIR"

# Step 2: Initialize context repository
if [[ "$REPO_TYPE" == "remote" ]]; then
    # Clone from remote
    print_info "Cloning remote repository..."
    if [[ -d "$CONTEXT_REPO" ]]; then
        print_warning "Directory exists: $CONTEXT_REPO"
        read -p "Remove and clone fresh? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$CONTEXT_REPO"
        else
            print_error "Cannot proceed with existing directory. Aborted."
            exit 1
        fi
    fi
    git clone "$REMOTE_URL" "$CONTEXT_REPO"
    print_success "Cloned remote repository"

    # If remote is empty, copy local content
    if [[ ! -f "$CONTEXT_REPO/.git/HEAD" ]] || [[ $(git -C "$CONTEXT_REPO" rev-parse --verify HEAD 2>/dev/null) == "" ]]; then
        print_info "Remote repository is empty. Copying local content..."
        rsync -av --exclude=.git local/ "$CONTEXT_REPO/"
    fi
else
    # Local repository
    if [[ -d "$CONTEXT_REPO" ]]; then
        print_warning "Directory already exists: $CONTEXT_REPO"
        if [[ ! -d "$CONTEXT_REPO/.git" ]]; then
            print_info "Initializing git repository in existing directory..."
            git -C "$CONTEXT_REPO" init
        fi
    else
        print_info "Creating context repository..."
        mkdir -p "$CONTEXT_REPO"
        git -C "$CONTEXT_REPO" init
        print_success "Initialized git repository: $CONTEXT_REPO"

        # Copy existing local/ content
        print_info "Copying existing local/ content to context repository..."
        rsync -av --exclude=.git local/ "$CONTEXT_REPO/"
        print_success "Content copied"
    fi
fi

# Step 3: Create .gitignore in context repo for secrets
print_info "Creating .gitignore for secrets protection..."
cat > "$CONTEXT_REPO/.gitignore" << 'EOF'
# Hish Context Repository - Security Protection
# This .gitignore ensures secrets never get committed to portable context

# SBMI cache (local compilation cache)
.sbmi-cache.json

# Secrets and credentials
**/secrets/
**/credentials/
**/*.key
**/*.pem
**/*.p12
**/*.pfx
**/.env.local
**/.env.*.local

# Tokens and passwords (by pattern)
**/*_token.txt
**/*_password.txt
**/*_secret.txt
**/*_credential.txt

# SSH keys
**/.ssh/
**/id_rsa
**/id_ed25519
**/known_hosts

# API keys and sensitive config
**/api_keys/
**/auth_tokens/

# Compiled bytecode
**/__pycache__/
**/*.pyc
**/*.pyo

# OS files
.DS_Store
Thumbs.db

# Editor temporary files
**/*~
**/*.swp
**/*.swo

# Note: repo_path.txt is TRACKED (contains paths, not secrets)
# Note: *.md files are TRACKED (context documentation)
# Note: .compact files should be TRACKED (part of context)
EOF

print_success "Created security .gitignore in context repository"

# Step 4: Initial commit in context repo
print_info "Creating initial commit in context repository..."
git -C "$CONTEXT_REPO" add -A
if git -C "$CONTEXT_REPO" diff --cached --quiet; then
    print_info "No changes to commit (repository up to date)"
else
    git -C "$CONTEXT_REPO" commit -m "Initial commit: Hish portable context

Migrated from local/ directory to standalone git repository.
This enables cross-environment context synchronization.

Security: .gitignore prevents secrets from being committed.
"
    print_success "Initial commit created"
fi

# If remote, push initial commit
if [[ "$REPO_TYPE" == "remote" ]]; then
    print_info "Pushing to remote..."
    git -C "$CONTEXT_REPO" branch -M main
    git -C "$CONTEXT_REPO" push -u origin main
    print_success "Pushed to remote repository"
fi

# Step 5: Replace local/ with symlink
print_info "Replacing local/ directory with symlink..."
rm -rf local
ln -sf "$CONTEXT_REPO" local
print_success "Created symlink: local -> $CONTEXT_REPO"

# Verify
if [[ -L "local" ]] && [[ -d "local" ]]; then
    print_success "Symlink verified and working"
else
    print_error "Symlink creation failed!"
    print_error "Restoring backup..."
    mv "$BACKUP_DIR" local
    exit 1
fi

echo ""
echo "=========================================="
print_success "✅ Portable context initialized successfully!"
echo "=========================================="
echo ""
echo "📁 Context repository: $CONTEXT_REPO"
echo "🔗 Symlink: local -> $CONTEXT_REPO"
echo "💾 Backup: $BACKUP_DIR (safe to delete after verification)"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Verify everything works:"
echo "   ./reindex        # Reindex framework"
echo "   /dev             # Test agent initialization"
echo ""
echo "2. On other machines, run:"
if [[ "$REPO_TYPE" == "remote" ]]; then
    echo "   make context-link-remote REPO=$REMOTE_URL"
else
    echo "   # Copy $CONTEXT_REPO to other machine"
    echo "   make context-link-local CONTEXT_PATH=<path>"
fi
echo ""
echo "3. Synchronize context changes:"
echo "   make context-push     # Push changes to context repo"
echo "   make context-pull     # Pull changes from context repo"
echo "   make context-sync     # Bidirectional sync"
echo ""
echo "🔒 Security: Secrets are protected by .gitignore in context repo"
echo "⚠️  Always review 'git status' before committing context changes"
echo ""

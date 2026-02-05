#!/bin/bash
# Hish - Sync Portable Context
# Commits and syncs changes to/from portable context repository

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

OPERATION="${1:-status}"  # push, pull, status

# Verify local/ is a symlink
if [[ ! -L "local" ]]; then
    print_error "local/ is not a symlink. Portable context not configured."
    echo ""
    echo "To set up portable context:"
    echo "  make context-init-portable    # Initialize new portable context"
    echo "  make context-link-remote      # Link existing remote context"
    echo "  make context-link-local       # Link existing local context"
    exit 1
fi

CONTEXT_REPO=$(readlink "local")

# Verify it's a git repository
if [[ ! -d "$CONTEXT_REPO/.git" ]]; then
    print_error "Context directory is not a git repository: $CONTEXT_REPO"
    print_info "Initialize with: git init $CONTEXT_REPO"
    exit 1
fi

cd "$CONTEXT_REPO"

echo "🔄 Hish - Context Sync"
echo "======================"
echo ""
echo "Repository: $CONTEXT_REPO"
echo "Operation: $OPERATION"
echo ""

# Function to commit changes
commit_changes() {
    if git diff --quiet && git diff --cached --quiet; then
        print_info "No changes to commit"
        return 0
    fi

    print_info "Changes detected. Committing..."
    git add -A

    # Show what will be committed
    echo ""
    echo "Files to be committed:"
    git status --short
    echo ""

    # Get commit message
    if [[ -n "$COMMIT_MSG" ]]; then
        git commit -m "$COMMIT_MSG"
    else
        # Auto-generate commit message
        timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
        hostname=$(hostname)
        git commit -m "Context update from $hostname

Timestamp: $timestamp
Auto-committed by Hish context sync.
"
    fi

    print_success "Changes committed"
    return 1  # Return 1 to indicate changes were committed
}

# Function to push changes
push_changes() {
    # Check if remote exists
    if ! git remote get-url origin &>/dev/null; then
        print_warning "No remote repository configured"
        print_info "Add remote with: git remote add origin <url>"
        return 0
    fi

    print_info "Pushing to remote..."

    # Get current branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)

    # Push
    if git push origin "$current_branch"; then
        print_success "Pushed to origin/$current_branch"
    else
        print_error "Push failed. You may need to pull first."
        return 1
    fi
}

# Function to pull changes
pull_changes() {
    # Check if remote exists
    if ! git remote get-url origin &>/dev/null; then
        print_warning "No remote repository configured"
        return 0
    fi

    print_info "Pulling from remote..."

    # Get current branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)

    # Check for uncommitted changes
    if ! git diff --quiet || ! git diff --cached --quiet; then
        print_warning "Uncommitted changes detected. Stashing..."
        git stash push -m "Auto-stash before pull ($(date -u +"%Y-%m-%d %H:%M:%S"))"
        STASHED=true
    else
        STASHED=false
    fi

    # Pull with rebase
    if git pull --rebase origin "$current_branch"; then
        print_success "Pulled from origin/$current_branch"

        # Pop stash if we stashed
        if [[ "$STASHED" == "true" ]]; then
            print_info "Restoring stashed changes..."
            if git stash pop; then
                print_success "Stashed changes restored"
            else
                print_error "Stash pop failed - resolve conflicts manually"
                print_info "Your changes are in: git stash list"
                return 1
            fi
        fi
    else
        print_error "Pull failed"
        return 1
    fi
}

# Execute operation
case "$OPERATION" in
    push)
        commit_changes
        push_changes
        ;;
    pull)
        pull_changes
        ;;
    status)
        echo "Git Status:"
        git status
        echo ""
        echo "Remote:"
        if git remote get-url origin &>/dev/null; then
            echo "  Origin: $(git remote get-url origin)"
            echo "  Branch: $(git rev-parse --abbrev-ref HEAD)"
        else
            echo "  No remote configured"
        fi
        ;;
    *)
        print_error "Unknown operation: $OPERATION"
        echo "Valid operations: push, pull, status"
        exit 1
        ;;
esac

echo ""
if [[ "$OPERATION" != "status" ]]; then
    print_success "✅ Context $OPERATION complete!"
fi

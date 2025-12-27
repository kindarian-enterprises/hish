# Portable Context - Cross-Environment Synchronization

## Overview

**Portable Context** enables you to synchronize your Hish `local/` directory across multiple machines using Git. This is **completely optional** - most users work on a single machine and don't need this feature.

### When to Use Portable Context

✅ **Use portable context if you:**
- Work on multiple machines (desktop + laptop)
- Want to sync agent context, personas, and project contexts
- Use cloud storage (Dropbox, Google Drive) or private git repos
- Need consistent development environment across machines

❌ **Don't use portable context if you:**
- Work on a single machine only
- Prefer local-only context (default behavior)
- Have security concerns about syncing context

## How It Works

### Architecture

```
# Default Setup (No Portable Context)
~/projects/hish/
├── .git/                    # Hish framework repository
├── local/                   # Real directory (gitignored)
│   ├── project-a/
│   ├── dev_agent_persona.md
│   └── workflow-indexes/
└── .gitignore               # Contains: local/

# Portable Context Setup
~/projects/hish/
├── .git/                    # Hish framework repository
├── local -> ~/.hish-context # Symlink to external repo
└── .gitignore               # Still contains: local/

~/.hish-context/             # Separate git repository
├── .git/
├── project-a/
│   ├── dev_agent_context.md
│   └── agents_synopsis.md
├── dev_agent_persona.md
├── workflow-indexes/
└── .gitignore               # Protects secrets
```

**Key Insight**: The entire `local/` directory becomes a symlink pointing to a separate git repository. The main Hish framework repository never tracks `local/` content.

## Setup Options

### Option 1: Local Portable Context (Recommended for Cloud Sync)

Store your context in a local directory that's synced by Dropbox, Google Drive, etc.

```bash
# Initialize portable context in Dropbox
make context-init-portable
# Choose option 2: Custom path
# Enter: ~/Dropbox/hish-context

# On second machine (after Dropbox syncs)
make context-link-local CONTEXT_PATH=~/Dropbox/hish-context
```

**Benefits:**
- Automatic sync via cloud provider
- No git commands needed
- Works offline

### Option 2: Remote Git Repository (Recommended for Privacy)

Store your context in a private git repository (GitHub, GitLab, self-hosted).

```bash
# Machine 1: Initialize and push to remote
make context-init-portable
# Choose option 3: Remote git repository
# Enter: git@github.com:yourusername/hish-context-private.git

# Machine 2: Clone from remote
make context-link-remote REPO=git@github.com:yourusername/hish-context-private.git
```

**Benefits:**
- Full version control history
- Works anywhere with git access
- Can use private repositories

### Option 3: Local Path (Advanced)

Link to an existing local directory (e.g., NAS, external drive).

```bash
make context-link-local CONTEXT_PATH=/mnt/nas/hish-context
```

## Daily Workflow

### With Remote Git Repository

```bash
# Start of day: Pull latest context
make context-pull

# Work normally...
/dev                         # Initialize dev agent
# ... make changes to context ...
/end-dev                     # End session

# End of day: Push context changes
make context-push

# Or do both at once
make context-sync            # Pull + commit + push
```

### With Cloud Sync (Dropbox/Google Drive)

No commands needed! Cloud provider handles sync automatically.

```bash
# Just work normally
/dev
# ... context changes happen ...
/end-dev

# Dropbox/Drive syncs in background
```

## Security

### What Gets Protected

The portable context repository includes a `.gitignore` that prevents secrets from being committed:

```gitignore
# Secrets and credentials
**/secrets/
**/credentials/
**/*.key
**/*.pem
**/.env.local

# Tokens and passwords
**/*_token.txt
**/*_password.txt
**/*_secret.txt
```

### What Gets Synced

✅ **Safe to sync:**
- Agent personas (`dev_agent_persona.md`)
- Project contexts (`project-name/dev_agent_context.md`)
- AGENTS.md synopses
- Workflow indexes
- Framework context
- `.compact` files (SBMI compiled)

❌ **Never synced (protected by .gitignore):**
- API tokens
- Passwords
- Private keys
- `.env` files with secrets

### Best Practices

1. **Use private repositories** for git-based sync
2. **Review before committing**: Always check `make context-status` before pushing
3. **Separate secrets**: Keep secrets in a different location (password manager, vault)
4. **Encrypt cloud storage**: Enable encryption for Dropbox/Drive if using cloud sync

## Commands Reference

### Setup Commands

```bash
make context-init-portable                    # Initialize new portable context
make context-link-remote REPO=<git-url>       # Link existing remote context
make context-link-local CONTEXT_PATH=<path>   # Link existing local context
```

### Sync Commands

```bash
make context-status    # Show git status of context repo
make context-pull      # Pull changes from remote
make context-push      # Commit and push changes
make context-sync      # Bidirectional sync (pull + commit + push)
```

### Info Commands

```bash
make list-contexts     # Shows if portable context is enabled
```

## Troubleshooting

### "local/ is not a symlink" Error

**Problem**: You're trying to sync but portable context isn't configured.

**Solution**:
```bash
make context-init-portable
```

### Merge Conflicts

**Problem**: Changes on both machines conflict.

**Solution**:
```bash
cd ~/.hish-context  # Or wherever your context repo is
git status
git diff
# Resolve conflicts manually
git add .
git commit -m "Resolved merge conflicts"
make context-push
```

### Lost Symlink

**Problem**: `local/` is a real directory again (symlink broken).

**Solution**:
```bash
# Backup current local/
mv local local.backup

# Re-link to context repo
make context-link-local CONTEXT_PATH=~/.hish-context

# Merge any changes from backup if needed
```

### Accidental Secret Commit

**Problem**: Committed a secret to context repository.

**Solution**:
```bash
cd ~/.hish-context

# Remove file from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (if using remote)
git push --force --all
git push --force --tags

# Rotate the compromised secret immediately!
```

## Migration

### Converting Existing Local Context to Portable

```bash
# Your existing local/ directory will be backed up automatically
make context-init-portable

# Choose your preferred storage location
# The script will:
# 1. Backup local/ to local.backup.<timestamp>
# 2. Copy content to new context repository
# 3. Create symlink: local -> context repository
# 4. Commit initial state

# Verify everything works
./reindex
/dev

# After verification, delete backup
rm -rf local.backup.*
```

### Reverting to Non-Portable Context

```bash
# Get current context repo location
CONTEXT_REPO=$(readlink local)

# Remove symlink
rm local

# Copy content back to real directory
cp -r "$CONTEXT_REPO" local

# Now local/ is a real directory again (gitignored)
```

## Advanced Usage

### Multiple Context Repositories

You can have different context repos for different purposes:

```bash
# Work context
make context-link-local CONTEXT_PATH=~/work-contexts/hish-context

# Personal context
make context-link-local CONTEXT_PATH=~/personal-contexts/hish-context
```

Switch by re-running the link command with different paths.

### Selective Sync

If you want to sync only specific projects:

```bash
cd ~/.hish-context

# Add specific paths to .gitignore
echo "sensitive-project/" >> .gitignore
git add .gitignore
git commit -m "Exclude sensitive-project from sync"

# Now sensitive-project/ won't be synced
```

### Automated Sync with Cron

For git-based sync, automate pulls:

```bash
# Add to crontab
crontab -e

# Pull context every hour
0 * * * * cd /home/user/projects/hish && make context-pull > /dev/null 2>&1
```

## FAQ

### Q: Does this affect the main Hish repository?

**A:** No. The main Hish repository never tracks `local/` (it's gitignored). Portable context is a completely separate git repository.

### Q: Can I use this with the framework itself in a git submodule?

**A:** Yes! The two are independent. You can have:
- Main project repo (contains Hish as submodule)
- Hish framework repo (main repo)
- Portable context repo (separate, linked via symlink)

### Q: What happens if I forget to push before switching machines?

**A:** You'll have divergent changes. When you pull on the other machine, git will try to merge. If there are conflicts, you'll need to resolve them manually.

### Q: Can multiple people share a context repository?

**A:** Technically yes, but **not recommended**. Context contains personal development history and preferences. Each developer should have their own context repository.

### Q: Does SBMI compilation work with symlinked local/?

**A:** Yes! SBMI follows symlinks transparently. `make sbmi-compact` works exactly the same whether `local/` is a real directory or a symlink.

## Related Documentation

- [Getting Started](getting-started.md) - Initial framework setup
- [Agent Workflows](../agent-management/agent-workflows.md) - How agents use context
- [Multi-Project Workflow](../examples/multi-project-workflow.md) - Working with multiple projects

---

**Remember**: Portable context is **optional**. The default local-only setup works great for most users!

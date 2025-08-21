# 🚀 **Getting Started with Simple Collaboration Workflow**

**The simplest way to collaborate on Kindarian Cursor Context - no complex Git knowledge required!**

## 🎯 **What This Means for You**

- **`origin`** = The main repository (you clone this directly)
- **`main`** = Your local working copy where you make changes
- **Local overrides** = Your machine-specific files (automatically ignored)

**Result**: Clean collaboration, no merge conflicts, easy updates from the main repo.

---

## 🚀 **Quick Start (5 minutes)**

### **Step 1: Clone the Repository**
```bash
# Clone your fork or the main repo
git clone https://github.com/your-username/kindarian-cursor-context.git
cd kindarian-cursor-context
```

### **Step 2: Set Up Local Customization (One-time setup)**
```bash
# Create directories for your local customizations
mkdir -p local overrides private tmp

# These directories are automatically ignored by Git
# Put your machine-specific files here to avoid conflicts

# Verify your setup
git remote -v
# Should show:
# origin    https://github.com/kindarian-enterprises/kindarian-cursor-context.git (fetch)
# origin    https://github.com/kindarian-enterprises/kindarian-cursor-context.git (push)
```

### **Step 3: Get the Latest Updates**
```bash
# Get updates from the official repo
git fetch upstream

# Merge updates into your main branch
git merge upstream/main

# If there are conflicts, resolve them and commit
git add .
git commit -m "Merge upstream updates"
```

**🎉 That's it! You're now set up for seamless collaboration.**

---

## 🔄 **Daily Workflow**

### **Getting Updates (When you want the latest features)**
```bash
# Option 1: Manual commands (recommended)
git fetch origin
git merge origin/main

# Option 2: Use the helper script
./scripts/sync-upstream.sh
```

### **Making Your Changes**
```bash
# Work on your changes as normal
git add .
git commit -m "Your changes"
git push origin main
```

### **Sharing Your Changes**
```bash
# Create a pull request to contribute back
# GitHub will show you exactly what to do
```

---

## 🛡️ **Local Overrides (Your Machine-Specific Files)**

**Put these in ignored folders to avoid conflicts:**

- `local/` - Your personal configurations
- `overrides/` - Machine-specific settings  
- `private/` - Keys, tokens, sensitive data
- `tmp/` - Temporary files and caches

**Example**: Want to customize the framework for your team?
```bash
# Create your custom config
mkdir local
cp env.framework local/env.framework.custom

# Edit local/env.framework.custom with your changes
# This file won't conflict with upstream updates!
```

---

## 🚨 **What Happens If...**

### **You Get Merge Conflicts**
```bash
# Don't panic! This usually means you edited a tracked file
# Solution: Move your changes to a local folder

# Example: You edited README.md
mkdir local
cp README.md local/README.md.my-version
git checkout -- README.md  # Restore original
git merge upstream/main     # Now it should work!

# Your changes are safe in local/README.md.my-version
```

### **You Want to Share Your Local Changes**
```bash
# Move changes from local/ to tracked location
cp local/env.framework.custom env.framework.team

# Commit and push
git add env.framework.team
git commit -m "Add team configuration"
git push origin main
```

### **You're Not Sure What to Do**
```bash
# Check what's happening
git status

# See what changed upstream
git log upstream/main --oneline -5

# Get help
./scripts/sync-upstream.sh --help
```

---

## 🎯 **Pro Tips**

### **Use the Helper Script**
```bash
# The sync-upstream.sh script does everything for you
./scripts/sync-upstream.sh

# It's safe to run multiple times
./scripts/sync-upstream.sh  # Won't break anything
```

### **Check Before You Start**
```bash
# Always check your status before making changes
git status
git remote -v

# Make sure you're on main branch
git branch
```

### **Keep Local Stuff Local**
```bash
# Good: Machine-specific files in local/
local/my-config.txt
local/team-settings.json

# Bad: Machine-specific files in tracked locations
README.md  # Don't edit this for personal use
env.framework  # Don't customize this directly
```

---

## 🔍 **Troubleshooting**

### **"Remote origin already exists"**
```bash
# You already have the main repo set up - that's fine!
# Just proceed to getting updates
```

### **"Permission denied" on push**
```bash
# You're trying to push to upstream (read-only)
# Push to origin instead:
git push origin main
```

### **"Merge conflicts"**
```bash
# Usually means you edited a tracked file
# Move your changes to local/ and try again
# See "What Happens If..." section above
```

### **"Branch is behind"**
```bash
# Just means you need to get updates
./scripts/sync-upstream.sh
```

---

## 📚 **Next Steps**

1. **Start using the framework**: `make quick-start`
2. **Create your first project context**: `make new-context`
3. **Index your code**: `make index-repo REPO_PATH=/path/to/code COLLECTION_NAME=my_project`
4. **Configure Cursor**: `make setup-cursor`

---

## 🆘 **Need Help?**

- **Check this guide first** - Most questions are answered here
- **Use the helper script** - `./scripts/sync-upstream.sh` handles most cases
- **Look at the examples** - `contexts/example-*` show real usage
- **Check the FAQ** - `docs/faq.md` has common questions

**Remember**: This workflow is designed to be simple. If something feels complicated, you're probably doing it the hard way! 🎯

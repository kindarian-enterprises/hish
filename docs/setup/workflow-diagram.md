# 🔄 **Upstream + Main Workflow Diagram**

**Visual guide to the zero-conflict collaboration workflow**

---

## 📊 **Workflow Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Main          │    │   Your Local    │    │   Local        │
│   Repository    │    │   Working      │    │   Customization│
│   (origin/main) │    │   Branch       │    │   (ignored)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
    Framework code          Your changes            Machine-specific
    (get updates)          (commit here)          (ignored folders)
         │                       │                       │
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                         Pull Request
                         (contribute back)
```

---

## 🔄 **Daily Workflow Steps**

### **1. Get Updates (When you want new features)**
```bash
# Switch to main branch
git checkout main

# Get latest updates
git fetch origin
git merge origin/main

# Switch back to your working branch
git checkout my-team-customization

# Merge updates into your branch
git merge main
```

**What happens:**
- Gets latest from main repo
- Merges updates into your working branch
- No conflicts (your changes are separate)

### **2. Make Your Changes**
```bash
# Work normally on your main branch
git add .
git commit -m "Your changes"
git push origin main
```

### **3. Keep Local Stuff Local**
```bash
# Put machine-specific files here (automatically ignored):
local/           # Your personal configs
overrides/       # Team customizations  
private/         # Keys and secrets
tmp/             # Temporary files
```

---

## 🚨 **Conflict Prevention**

### **✅ Good: Local Overrides**
```
local/
├── env.framework.my-team
├── team-settings.json
└── custom-config.txt
```

### **❌ Bad: Editing Tracked Files**
```
README.md          # Don't edit for personal use
env.framework      # Don't customize directly
docs/setup/...    # Don't modify for local needs
```

---

## 🎯 **Key Benefits**

- **🔄 Zero Merge Conflicts** - Your local changes never conflict with upstream
- **📥 Easy Updates** - One command gets all new features
- **🛡️ Safe Localization** - Customize without breaking anything
- **🤝 Clean Collaboration** - Contribute back via pull requests
- **⚡ Fast Setup** - 2 minutes to full collaboration

---

## 🚀 **Quick Commands**

```bash
# One-time setup
git clone https://github.com/kindarian-enterprises/kindarian-cursor-context.git
git checkout -b my-team-customization
mkdir -p local overrides private tmp

# Daily updates
git checkout main
git fetch origin
git merge origin/main
git checkout my-team-customization
git merge main

# Check status
git branch
git status
```

---

**🎯 Remember: Keep local stuff local, and you'll never have merge conflicts again!**

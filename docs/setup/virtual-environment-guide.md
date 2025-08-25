# 🐍 Virtual Environment Setup for Host-Based Indexing

Host-based indexing provides **2-4x better performance** than container-based indexing but requires Python dependencies in a virtual environment.

## 🚀 **Quick Setup (Recommended)**

### **virtualenvwrapper (Best Option)**

```bash
# One-time setup
pip install virtualenvwrapper
echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.bashrc
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
source ~/.bashrc

# Create environment
mkvirtualenv hish-indexing --python=python3.12
cd /path/to/hish
pip install -r rag/indexer/requirements.txt

# Use it
make index-host
```

**Daily usage:**
```bash
workon hish-indexing
make index-framework  # Quick updates
deactivate
```

### **Standard venv (Alternative)**

```bash
# One-time setup
cd /path/to/hish
python3 -m venv .venv
source .venv/bin/activate
pip install -r rag/indexer/requirements.txt

# Use it
make index-host
```

**Daily usage:**
```bash
cd /path/to/hish && source .venv/bin/activate
make index-framework
deactivate
```

## 📊 **Performance Benefits**

| Repository Size | Container | Host-Based | Improvement |
|-----------------|-----------|------------|-------------|
| Small (<10MB)   | 30s       | 15s        | 2x faster   |
| Medium (50MB)   | 2-3 min   | 1 min      | 2-3x faster |
| Large (200MB+)  | 10-15 min | 3-5 min    | 3-4x faster |

## 🔧 **Dependencies**

Install manually: `pip install -r rag/indexer/requirements.txt`

Includes: qdrant-client, fastembed, torch, transformers, sentence-transformers, rich, pathspec

## 🚨 **Troubleshooting**

**Environment issues:**
```bash
# Recreate if needed
rmvirtualenv hish-indexing
mkvirtualenv hish-indexing --python=python3.12
```

**Dependency issues:**
```bash
pip install --upgrade pip
pip install -r rag/indexer/requirements.txt
```

## 💡 **Tips**

**Auto-activation alias:**
```bash
# Add to ~/.bashrc
alias hish='workon hish-indexing && cd /path/to/hish'
```

**Multiple projects:**
```bash
mkvirtualenv hish-work --python=python3.12
mkvirtualenv hish-personal --python=python3.12
```

---

**Recommendation:** Use virtualenvwrapper for best experience. It provides centralized environment management and easy switching between projects.
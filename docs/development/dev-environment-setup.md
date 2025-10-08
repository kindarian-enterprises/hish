# Hish Development Environment Setup

Quick guide for setting up the Hish development environment.

## Prerequisites

- Python 3.12+ (recommended)
- virtualenvwrapper installed
- Git

## Setup Steps

### 1. Create Development Virtualenv

```bash
# Create hish-dev virtualenv
mkvirtualenv hish-dev --python=python3.12

# Activate it
workon hish-dev
```

### 2. Install All Dependencies

```bash
cd /path/to/hish
make dev-setup
```

This will:
- ✅ Verify you're in a virtual environment
- ✅ Install all development dependencies (linting, testing, etc.)
- ✅ Install all runtime dependencies (qdrant-client, fastembed, numpy, etc.)
- ✅ Install pre-commit hooks
- ✅ Upgrade pip to latest version

### 3. Verify Installation

```bash
# Run tests
make test

# Check code quality
make lint

# Test optimization features
python3 scripts/test-qdrant-optimizations.py
```

## What Gets Installed

**Development Tools:**
- `ruff`, `black`, `isort`, `mypy` - Code quality
- `pytest`, `pytest-cov`, `pytest-mock` - Testing
- `pre-commit` - Git hooks

**Runtime Dependencies:**
- `qdrant-client>=1.8.0` - Vector database client
- `fastembed==0.7.1` - Fast embedding generation
- `numpy>=1.21.0` - Vector operations
- `sentence-transformers>=2.2.0` - MPNet model
- `torch>=1.12.0` - PyTorch backend
- `transformers>=4.21.0` - Transformer models
- `rich>=13.7.1` - Terminal formatting
- And more...

## Daily Workflow

### Activate Environment

```bash
workon hish-dev
```

### Run Commands

```bash
# Format code before committing
make format

# Run linting
make lint

# Auto-fix issues
make lint-fix

# Run tests
make test

# Index framework
make index-framework

# Index code repositories
make index-code
```

### Deactivate

```bash
deactivate
```

## Troubleshooting

### "No module named X" errors

Run `make dev-setup` again to reinstall all dependencies.

### Virtual environment issues

```bash
# Delete and recreate
rmvirtualenv hish-dev
mkvirtualenv hish-dev --python=python3.12
workon hish-dev
make dev-setup
```

### Pre-commit hook issues

```bash
pre-commit uninstall
make dev-setup
```

## Configuration Files

- `requirements-dev.txt` - Development dependencies
- `rag/indexer/requirements.txt` - Runtime dependencies
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `pyproject.toml` - Tool configurations (black, isort, etc.)

---

**Quick Setup:**
```bash
mkvirtualenv hish-dev --python=python3.12 && workon hish-dev && make dev-setup
```

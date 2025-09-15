# Code Quality & Linting

## Overview

The Hish framework maintains high code quality standards through automated linting, formatting, and type checking. This document explains the development workflow and tools.

## Quick Start

```bash
# One-time setup
make dev-setup

# Before committing (automatic with pre-commit hooks)
make lint-fix

# Manual checks
make lint
```

## Development Setup

### Install Development Dependencies

```bash
# Install all development tools and pre-commit hooks
make dev-setup

# Or manually:
pip install -r requirements-dev.txt
pre-commit install
```

### Pre-commit Hooks

Pre-commit hooks automatically run before each commit to ensure code quality:

- **Trailing whitespace removal**
- **End-of-file fixing**
- **YAML/TOML validation**
- **Python formatting** (black, isort)
- **Linting** (ruff)
- **Type checking** (mypy)

## Available Commands

### Linting Commands

```bash
# Run all quality checks (read-only)
make lint

# Fix auto-fixable issues
make lint-fix

# Format code only
make format

# Type checking only
make type-check
```

### Manual Tool Usage

```bash
# Ruff (fast Python linter)
cd rag/indexer
ruff check .                    # Check only
ruff check . --fix             # Fix issues

# Black (code formatter)
black .                        # Format
black --check --diff .         # Check only

# isort (import sorting)
isort .                        # Sort imports
isort --check-only --diff .    # Check only

# mypy (type checking)
mypy . --ignore-missing-imports
```

## Configuration

### Ruff Configuration
Ruff settings are in `rag/indexer/pyproject.toml` (if it exists) or use defaults.

### Black Configuration
- Line length: 88 characters (default)
- Target Python version: 3.12

### isort Configuration
- Profile: black (for compatibility)
- Multi-line output: 3

### mypy Configuration
- Ignore missing imports: enabled
- No strict optional: enabled

## CI Integration

The GitHub Actions workflow automatically:
1. Installs development dependencies
2. Runs all linting tools
3. Reports any issues
4. Fails the build on linting errors

## Workflow

### Daily Development

1. **Before starting work**: `make dev-setup` (one-time)
2. **While coding**: Pre-commit hooks run automatically
3. **Before pushing**: `make lint` to verify everything passes
4. **If issues found**: `make lint-fix` to auto-fix what's possible

### Handling Linting Failures

1. **Auto-fixable issues**: Run `make lint-fix`
2. **Manual fixes required**: Follow the tool's suggestions
3. **Type errors**: Add type hints or use `# type: ignore`
4. **Complex cases**: Discuss with the team

## Excluding Files

To exclude files from linting, update `.pre-commit-config.yaml`:

```yaml
- id: ruff
  files: ^rag/indexer/
  exclude: ^rag/indexer/generated/
```

## Best Practices

1. **Run `make lint-fix`** before committing
2. **Add type hints** to new functions
3. **Follow Black's formatting** decisions
4. **Use descriptive variable names** for mypy
5. **Keep line length ≤ 88 characters**
6. **Sort imports** with isort profile

## Troubleshooting

### Pre-commit hooks not running
```bash
pre-commit install
```

### Linting tools not found
```bash
pip install -r requirements-dev.txt
```

### Type checking failures
- Add missing type hints
- Use `# type: ignore` sparingly
- Install missing type stubs

### Performance issues
Ruff is very fast; if linting is slow, check for large generated files being included.

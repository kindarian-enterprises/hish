# Hish Framework GitHub Actions

This directory contains GitHub Actions workflows for the Hish framework continuous integration.

## Workflows

### `test-indexer.yml`

**Purpose**: Tests the Hish indexer and related components on every push/PR to ensure code quality and functionality.

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests targeting `main` or `develop` branches
- Only runs when indexer-related files change

**What it tests**:
- **Python 3.12**: Tests on recommended Python version for optimal performance
- **Indexer Functionality**: Unit and integration tests for the embedding indexer
- **MPNet Model**: Verifies the unified MPNet embedding model is available
- **Host Indexer Script**: Tests the performance-optimized host indexing script
- **Configuration Validation**: Ensures all environment files are valid
- **MCP Docker Setup**: Validates Dockerfile and Docker Compose configurations
- **Makefile Integration**: Tests framework commands and help system
- **Code Quality**: Linting, formatting, and type checking with ruff, black, isort, and mypy

**Coverage**:
- Maintains 80%+ test coverage requirement
- Uploads coverage reports to Codecov for tracking

**Performance**:
- Uses pip caching to speed up dependency installation
- Single Python version testing for faster CI execution

## Local Testing

To run the same tests locally:

```bash
# Run indexer tests
cd rag/indexer
python -m pytest tests/ -v --cov=. --cov-report=term-missing

# Test MCP Docker configuration
python -c "
with open('mcp/Dockerfile.llamaindex', 'r') as f:
    content = f.read()
# Basic Dockerfile validation
assert 'FROM ' in content and 'CMD ' in content
print('✅ Dockerfile syntax valid')
"
docker compose -f deploy/compose.rag.yml config --quiet

# Test Makefile commands
make help

# Run linting
ruff check rag/indexer/
black --check rag/indexer/
isort --check-only rag/indexer/
mypy rag/indexer/ --ignore-missing-imports
```

## Configuration

The workflow automatically:
- Installs system dependencies (build tools)
- Caches pip dependencies for faster runs
- Validates that the MPNet model is available in FastEmbed
- Tests configuration file syntax
- Provides detailed error reporting

## Adding New Tests

When adding new functionality:
1. Add corresponding unit tests in `rag/indexer/tests/unit/`
2. Add integration tests in `rag/indexer/tests/integration/`
3. Ensure tests use the `TEST_MODEL_NAME` constant for consistency
4. Maintain 80%+ test coverage
5. Follow existing test patterns and naming conventions

The workflow will automatically run on your PR and provide feedback on any issues.

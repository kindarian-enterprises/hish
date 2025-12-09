# SBMI - Symbolic Budget-Managed Index System

Python package for compiling framework documentation into token-optimized `.compact` files while preserving behavioral context integrity.

## What It Does

**Dual-file system:**
- Agents READ → `.compact` files (token-optimized)
- You EDIT → `.md` files (human-readable)
- RAG indexes → `.md` files (full semantic search)

**Smart compilation:**
- Hash-based change detection (SHA256)
- Incremental recompilation (only changed files)
- Compression for navigation indexes (significant token reduction)
- Verbatim copy for behavioral context (exact preservation)

## Key Features

### 1. Config-Driven Compression
- **Scan directories**: Define where to look
- **Exclusions**: Pattern-based or directory-based
- **Phrase mappings**: Empirically optimized via frequency analysis

### 2. Hash-Based Incremental Compilation
- **Algorithm**: SHA256 on file contents
- **Cache**: `.sbmi-cache.json` tracks compilation state
- **Performance**: Fast session-end recompilation (sub-second)

### 3. Verbatim Copy for Behavioral Files
- Agent personas copied exactly with `.compact` extension
- Uniform interface: agents always read `*.compact`
- Zero risk of mangling behavioral directives

### 4. Robust Testing
- Comprehensive test suite with high coverage
- Validates command preservation, context integrity
- CI integration via GitHub Actions

## Commands

### Session-End Workflow (Primary)
```bash
make sbmi-compact              # Incremental: recompile only changed files
```
**When**: After agent session that modified framework `.md` files
**Performance**: <0.5s typical (hash-based change detection)

### Initial Setup
```bash
make setup-framework           # Force compile all framework docs
```
**When**: First-time repo setup, after config changes
**Performance**: ~2s for 56 files

### Maintenance
```bash
make sbmi-compact-force        # Force recompile everything
make sbmi-stats                # Show cache statistics
make sbmi-analyze              # Phrase frequency analysis
```

### Testing
```bash
make test-sbmi                 # Run all tests with coverage
make test-sbmi-unit            # Unit tests only
```

## Hash-Based Change Detection

**How it works:**
1. **Compute hash**: SHA256 of each `.md` file
2. **Check cache**: Compare against stored hash in `.sbmi-cache.json`
3. **Compile if changed**: Hash differs or file is new
4. **Update cache**: Store new hash and metadata

**Cache structure:**
```json
{
  "/path/to/file.md": {
    "hash": "a3f5b2c...",
    "output": "/path/to/file.compact",
    "compiled_at": "2025-12-09T17:07:58",
    "reduction_pct": 26.4
  }
}
```

**Benefits:**
- Skip unchanged files (instant)
- Detect modifications (reliable)
- Persist across runs (JSON file)
- Survive cache corruption (loads empty)

## Python API

### Basic Usage
```python
from sbmi.compiler import IndexCompiler, CompressionConfig

# Load config
config = CompressionConfig()  # Uses config/sbmi-compression.yaml

# Create compiler with cache enabled
compiler = IndexCompiler(
    hish_root="/path/to/hish",
    config=config,
    use_cache=True  # Enable incremental compilation
)

# Incremental compilation (session-end workflow)
results = compiler.compile_changed_indexes(level="level2")

# Force full compilation
compiler = IndexCompiler(hish_root, config, use_cache=False)
results = compiler.compile_all_indexes(level="level2")
```

### Cache Operations
```python
from sbmi.compiler.cache import CompilationCache
from pathlib import Path

# Initialize cache
cache = CompilationCache(Path("/path/to/.sbmi-cache.json"))

# Check if file changed
changed = cache.has_changed(Path("file.md"))

# Mark as compiled
cache.mark_compiled(
    source_file=Path("file.md"),
    output_file=Path("file.compact"),
    reduction_pct=reduction
)

# Get statistics
stats = cache.get_stats()
# Returns: {'total_compiled', 'avg_reduction', 'last_compiled'}

# Invalidate cache
cache.invalidate()  # Clear all
cache.invalidate(Path("specific-file.md"))  # Clear specific
```

### Phrase Frequency Analysis
```python
from sbmi.analyzer import PhraseFrequencyAnalyzer
from pathlib import Path

# Create analyzer
analyzer = PhraseFrequencyAnalyzer([
    Path("templates/"),
    Path("prompts/"),
    Path("local/")
])

# Run analysis
analyzer.analyze()

# Get top phrases
top_bigrams = analyzer.get_top_bigrams(limit=30)
top_trigrams = analyzer.get_top_trigrams(limit=20)

# Generate optimized mappings
mappings = analyzer.generate_phrase_mappings(top_n=30)
# Returns: [(phrase, abbrev, count, savings), ...]

# Print report
analyzer.print_report(top_n=50)
```

## Configuration

See `config/sbmi-compression.yaml`:
- `exclusion_patterns`: Files never compressed (personas, inits, guides)
- `phrase_mappings`: Term abbreviations for Level 2
- `levels`: Compression level definitions

## Package Structure

```
sbmi/
├── __init__.py
├── compiler/
│   ├── compiler.py      # Main IndexCompiler class
│   ├── config.py        # Configuration loading
│   ├── cache.py         # Hash-based change detection
│   └── strategies.py    # Compression strategies
├── analyzer/
│   └── frequency.py     # Phrase frequency analysis
├── tests/              # Comprehensive test suite
├── requirements.txt
├── requirements-test.txt
└── pyproject.toml
```

## Testing

```bash
make test-sbmi              # Run all tests with coverage
make test-sbmi-unit         # Unit tests only
```

**Test suites:**
- `test_cache.py` - Hash computation, change detection
- `test_compiler.py` - Verbatim copy, incremental compilation
- `test_config.py` - Configuration loading
- `test_strategies.py` - Compression preservation

**CI integration:** `.github/workflows/test-sbmi.yml`

## Documentation Links

### For Users
- **Quick start:** `../README.md` (main README, Framework Optimization section)
- **User guide:** `../docs/agent-management/framework-optimization.md`
- **Session workflow:** `../local/workflows-and-processes/sbmi-session-workflow.md`

### For Developers
- **This file:** `sbmi/README.md` - Package API and commands
- **System architecture:** `../local/workflow-indexes/sbmi-system-index.md`
- **Original design:** `../local/symbolic-budget-index-system-design.md`
- **AGENTS.md:** `../AGENTS.md` - Framework synopsis

### Configuration
- **Compression settings:** `../config/sbmi-compression.yaml`
- **CI workflow:** `../.github/workflows/test-sbmi.yml`
- **Test config:** `pytest.ini`

### Testing
- **All tests:** `tests/` directory
- **Run tests:** `make test-sbmi` from hish root

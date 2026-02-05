"""Test index compiler integration."""

import shutil
import tempfile
from pathlib import Path

import pytest

from sbmi.compiler import CompressionConfig, IndexCompiler


class TestIndexCompiler:
    """Test the main IndexCompiler class."""

    @pytest.fixture
    def temp_hish_root(self):
        """Create temporary hish directory structure for testing."""
        temp_dir = Path(tempfile.mkdtemp())

        # Create workflow-indexes directory
        workflow_indexes = temp_dir / "local" / "workflow-indexes"
        workflow_indexes.mkdir(parents=True)

        # Create sample index file
        sample_index = workflow_indexes / "test-index.md"
        sample_index.write_text(
            """# Test Command Index

## 🚨 MANDATORY SESSION BEHAVIOR 🚨
**⚠️ CRITICAL: Test commands**

## Setup Commands

```bash
# Install dependencies
make install

# Run tests - Execute all test suites
make test
```

### Context Management
make new-context - Create new project context
make list-contexts - List all contexts
"""
        )

        yield temp_dir

        # Cleanup
        shutil.rmtree(temp_dir)

    def test_compiler_initialization(self, temp_hish_root):
        """Test compiler initializes correctly."""
        config = CompressionConfig()
        compiler = IndexCompiler(temp_hish_root, config=config)

        assert compiler.hish_root == temp_hish_root
        assert compiler.workflow_indexes.exists()

    def test_compress_index_preserves_commands(self, temp_hish_root):
        """Test that compression preserves essential commands."""
        config = CompressionConfig()
        compiler = IndexCompiler(temp_hish_root, config=config)

        source_file = temp_hish_root / "local" / "workflow-indexes" / "test-index.md"
        output_file = compiler.compress_index(source_file, level="level2")

        assert output_file.exists()

        compressed_content = output_file.read_text()

        # Essential commands must be preserved
        assert "make install" in compressed_content
        assert "make test" in compressed_content
        assert (
            "make new-context" in compressed_content or "newctx" in compressed_content
        )
        assert (
            "make list-contexts" in compressed_content
            or "make list-ctx" in compressed_content
        )

        # Emojis should be removed but text preserved
        assert "🚨" not in compressed_content
        assert "⚠️" not in compressed_content
        # Verbose descriptions should be stripped
        assert "Execute all test suites" not in compressed_content

    def test_exclusion_patterns_create_verbatim_copy(self, temp_hish_root):
        """Test that excluded files are copied verbatim with .compact extension."""
        # Create a file that should be excluded
        excluded_file = (
            temp_hish_root / "local" / "workflow-indexes" / "dev_agent_persona.md"
        )
        original_content = "# Agent Persona\nThis should not be compressed.\nBehavioral directive: Stay focused."
        excluded_file.write_text(original_content)

        config = CompressionConfig()
        compiler = IndexCompiler(temp_hish_root, config=config, use_cache=False)

        result = compiler.compress_index(excluded_file, level="level2")

        # Should create .L{weight}.compact file (weight determined by size)
        assert result.exists()
        assert result.name.endswith(".compact")
        assert ".L" in result.name  # Has weight indicator

        # File should be in excluded set
        assert excluded_file in compiler.excluded_files

        # Content should be verbatim (plus header)
        compact_content = result.read_text()
        assert "Behavioral Context - Uncompressed" in compact_content
        assert "EXCLUDED from compression" in compact_content
        assert original_content in compact_content
        assert "Behavioral directive: Stay focused." in compact_content

    def test_compile_all_indexes(self, temp_hish_root):
        """Test compiling all indexes in directory."""
        config = CompressionConfig()
        compiler = IndexCompiler(temp_hish_root, config=config)

        results = compiler.compile_all_indexes(level="level2")

        assert len(results) > 0
        assert "test-index.md" in results

        # Check that compilation completed
        stats = results["test-index.md"]
        assert "output" in stats
        assert stats["output"].exists()

        # For small files, header overhead may increase size
        # Just verify the output file was created correctly
        output_content = stats["output"].read_text()
        assert "AUTOMATICALLY GENERATED" in output_content


class TestEssentialContextIntegrity:
    """Critical end-to-end tests for context preservation."""

    @pytest.fixture
    def sample_command_index(self):
        """Real-world command index sample."""
        return """# Framework Command Index

## Setup and Configuration Commands

### Initial Framework Setup
```bash
# 1. Quick setup guide
make quick-start

# 2. Configure Cursor MCP integration
make setup-cursor

# 3. Create new project context
make new-context

# 4. Index everything
make index
```

### Context Management
```bash
# Create new project context
make new-context

# List all project contexts
make list-contexts

# Reindex specific contexts
./reindex context1 context2

# Reindex all contexts
./reindex all
```

### Knowledge Management
```bash
# Index everything
make index

# Index framework documentation only
make index-framework

# Setup cross-project intelligence collection
make setup-intelligence

# Index specific repository
make index-repo REPO_PATH=/path/to/repo COLLECTION_NAME=repo_name_code
```

### Cross-Project Intelligence Storage
```bash
# Generate UUID
python3 -c "import uuid; print(uuid.uuid4())"

# Store cross-project observations
text.store "Pattern observation..." cross_project_intelligence_mpnet [UUID]

# Search intelligence collection
text.search "query" cross_project_intelligence_mpnet
```
"""

    def test_all_commands_preserved(self, sample_command_index):
        """Ensure all unique commands are preserved after compression."""
        from sbmi.compiler.config import CompressionConfig
        from sbmi.compiler.strategies import (
            CombinedCompressionStrategy,
            PhraseCompressionStrategy,
            StructuralCompressionStrategy,
        )

        config = CompressionConfig()
        structural = StructuralCompressionStrategy()
        phrase = PhraseCompressionStrategy()
        strategy = CombinedCompressionStrategy([structural, phrase])

        result = strategy.compress(sample_command_index, config.as_dict())

        # All make commands must be present
        assert "make quick-start" in result
        assert "make setup-cursor" in result
        assert "make new-context" in result or "newctx" in result
        assert "make index" in result
        assert "make list-contexts" in result or "make list-ctx" in result
        assert "./reindex" in result
        assert "make index-framework" in result or "make index-fw" in result
        assert "make setup-intelligence" in result or "make setup-intel" in result
        assert "make index-repo" in result

        # Complex commands must be intact
        assert 'python3 -c "import uuid; print(uuid.uuid4())"' in result
        assert "text.store" in result
        assert "text.search" in result
        assert "REPO_PATH=/path/to/repo" in result
        assert "COLLECTION_NAME=repo_name_code" in result
        assert "cross_project_intelligence_mpnet" in result or "xproj" in result


class TestCacheAndIncrementalCompilation:
    """Test hash-based caching and incremental compilation."""

    @pytest.fixture
    def temp_hish_root_with_config(self):
        """Create temporary hish directory with proper structure."""
        temp_dir = Path(tempfile.mkdtemp())

        # Create directory structure matching config
        (temp_dir / "templates").mkdir(parents=True)
        (temp_dir / "prompts").mkdir(parents=True)
        (temp_dir / "local" / "workflow-indexes").mkdir(parents=True)
        (temp_dir / "config").mkdir(parents=True)

        # Create sample files
        (temp_dir / "local" / "workflow-indexes" / "test-index.md").write_text(
            "# Test Index\n\nmake test\nmake build\n"
        )
        (temp_dir / "templates" / "workflow-guide.md").write_text(
            "# Workflow Guide\n\nStep 1: Setup\nStep 2: Execute\n"
        )

        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_cache_initialization(self, temp_hish_root_with_config):
        """Test that cache is initialized correctly."""
        from sbmi.compiler.cache import CompilationCache

        cache_file = temp_hish_root_with_config / "local" / ".sbmi-cache.json"
        cache = CompilationCache(cache_file)

        assert cache.cache_file == cache_file
        assert cache.cache == {}

    def test_hash_computation(self, temp_hish_root_with_config):
        """Test that file hash is computed correctly."""
        from sbmi.compiler.cache import CompilationCache

        test_file = (
            temp_hish_root_with_config / "local" / "workflow-indexes" / "test-index.md"
        )
        cache_file = temp_hish_root_with_config / "local" / ".sbmi-cache.json"
        cache = CompilationCache(cache_file)

        hash1 = cache.compute_hash(test_file)
        assert len(hash1) == 64  # SHA256 hex digest

        # Same file should have same hash
        hash2 = cache.compute_hash(test_file)
        assert hash1 == hash2

        # Modified file should have different hash
        test_file.write_text("# Modified Content\n")
        hash3 = cache.compute_hash(test_file)
        assert hash1 != hash3

    def test_cache_detects_new_files(self, temp_hish_root_with_config):
        """Test that cache identifies new files correctly."""
        from sbmi.compiler.cache import CompilationCache

        test_file = (
            temp_hish_root_with_config / "local" / "workflow-indexes" / "test-index.md"
        )
        cache_file = temp_hish_root_with_config / "local" / ".sbmi-cache.json"
        cache = CompilationCache(cache_file)

        # New file should be marked as changed
        assert cache.has_changed(test_file) is True

        # After marking as compiled, should not be changed
        output_file = test_file.with_suffix(".compact")
        cache.mark_compiled(test_file, output_file, 25.0)
        assert cache.has_changed(test_file) is False

    def test_cache_detects_modifications(self, temp_hish_root_with_config):
        """Test that cache detects file modifications."""
        from sbmi.compiler.cache import CompilationCache

        test_file = (
            temp_hish_root_with_config / "local" / "workflow-indexes" / "test-index.md"
        )
        cache_file = temp_hish_root_with_config / "local" / ".sbmi-cache.json"
        cache = CompilationCache(cache_file)

        # Mark as compiled
        output_file = test_file.with_suffix(".compact")
        cache.mark_compiled(test_file, output_file, 25.0)
        assert cache.has_changed(test_file) is False

        # Modify file
        test_file.write_text("# Modified Index\n\nmake different-command\n")

        # Should detect change
        assert cache.has_changed(test_file) is True

    def test_incremental_compilation(self, temp_hish_root_with_config):
        """Test that incremental compilation only processes changed files."""
        config = CompressionConfig()
        compiler = IndexCompiler(
            temp_hish_root_with_config, config=config, use_cache=True
        )

        # First compilation - all files are new
        results1 = compiler.compile_changed_indexes(level="level2")
        assert len(results1) > 0

        # Second compilation - no changes
        compiler2 = IndexCompiler(
            temp_hish_root_with_config, config=config, use_cache=True
        )
        results2 = compiler2.compile_changed_indexes(level="level2")
        assert len(results2) == 0  # No files recompiled

        # Modify one file
        test_file = (
            temp_hish_root_with_config / "local" / "workflow-indexes" / "test-index.md"
        )
        test_file.write_text("# Modified Index\n\nmake new-command\n")

        # Third compilation - only modified file
        compiler3 = IndexCompiler(
            temp_hish_root_with_config, config=config, use_cache=True
        )
        results3 = compiler3.compile_changed_indexes(level="level2")
        assert len(results3) == 1
        assert "test-index.md" in results3

    def test_cache_persistence(self, temp_hish_root_with_config):
        """Test that cache persists across compiler instances."""
        from sbmi.compiler.cache import CompilationCache

        cache_file = temp_hish_root_with_config / "local" / ".sbmi-cache.json"
        test_file = (
            temp_hish_root_with_config / "local" / "workflow-indexes" / "test-index.md"
        )

        # Create cache and mark file
        cache1 = CompilationCache(cache_file)
        output_file = test_file.with_suffix(".compact")
        cache1.mark_compiled(test_file, output_file, 30.5)

        # New cache instance should load existing data
        cache2 = CompilationCache(cache_file)
        assert cache2.has_changed(test_file) is False

        stats = cache2.get_stats()
        assert stats["total_compiled"] == 1
        assert stats["avg_reduction"] == 30.5


class TestConfigDrivenScanning:
    """Test config-driven directory scanning and exclusions."""

    @pytest.fixture
    def temp_hish_with_structure(self):
        """Create full directory structure for testing."""
        temp_dir = Path(tempfile.mkdtemp())

        # Create all directories
        (temp_dir / "templates").mkdir(parents=True)
        (temp_dir / "templates" / "style-and-philosophy").mkdir(parents=True)
        (temp_dir / "prompts").mkdir(parents=True)
        (temp_dir / "local").mkdir(parents=True)
        (temp_dir / "docs").mkdir(parents=True)

        # Create files in scanned directories
        (temp_dir / "templates" / "workflow.md").write_text("# Workflow\nContent")
        (temp_dir / "prompts" / "init.md").write_text("# Init\nContent")
        (temp_dir / "local" / "notes.md").write_text("# Notes\nContent")

        # Create files in excluded directories
        (temp_dir / "docs" / "user-guide.md").write_text("# User Guide\nContent")
        (temp_dir / "templates" / "style-and-philosophy" / "principles.md").write_text(
            "# Principles\nContent"
        )

        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_scan_directories_from_config(self, temp_hish_with_structure):
        """Test that compiler scans configured directories."""
        config = CompressionConfig()
        compiler = IndexCompiler(
            temp_hish_with_structure, config=config, use_cache=False
        )

        # Compiler should have scan_dirs from config
        assert len(compiler.scan_dirs) == 3
        scan_dir_names = [d.name for d in compiler.scan_dirs]
        assert "templates" in scan_dir_names
        assert "prompts" in scan_dir_names
        assert "local" in scan_dir_names

    def test_excluded_directories_not_scanned(self, temp_hish_with_structure):
        """Test that excluded directories are not scanned."""
        config = CompressionConfig()
        compiler = IndexCompiler(
            temp_hish_with_structure, config=config, use_cache=False
        )

        # Find all markdown files
        all_files = compiler._find_all_markdown_files()

        # Files from scanned directories should be present
        file_names = [f.name for f in all_files]
        assert "workflow.md" in file_names
        assert "init.md" in file_names
        assert "notes.md" in file_names

        # Files from excluded directories should NOT be present
        assert "user-guide.md" not in file_names
        assert "principles.md" not in file_names

    def test_is_excluded_checks_directories(self, temp_hish_with_structure):
        """Test that is_excluded() checks both patterns and directories."""
        config = CompressionConfig()
        compiler = IndexCompiler(
            temp_hish_with_structure, config=config, use_cache=False
        )

        # File in excluded directory
        docs_file = temp_hish_with_structure / "docs" / "user-guide.md"
        assert compiler.is_excluded(docs_file) is True

        # File in style-and-philosophy (excluded subdirectory)
        style_file = (
            temp_hish_with_structure
            / "templates"
            / "style-and-philosophy"
            / "principles.md"
        )
        assert compiler.is_excluded(style_file) is True

        # Regular file should not be excluded
        regular_file = temp_hish_with_structure / "templates" / "workflow.md"
        assert compiler.is_excluded(regular_file) is False


class TestVerbatimCopyBehavior:
    """Test verbatim copy for excluded files."""

    @pytest.fixture
    def temp_hish_root(self):
        """Create temporary hish directory."""
        temp_dir = Path(tempfile.mkdtemp())
        (temp_dir / "templates").mkdir(parents=True)
        (temp_dir / "local").mkdir(parents=True)
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_verbatim_copy_preserves_exact_content(self, temp_hish_root):
        """Test that verbatim copy preserves content exactly."""
        # Create persona file (should be excluded)
        persona_file = temp_hish_root / "templates" / "dev_agent_persona.md"
        persona_content = """# Development Agent Persona

You are a focused, methodical development agent.

## Core Principles
1. Write clean, maintainable code
2. Test thoroughly
3. Document clearly

**Critical:** Never skip validation steps.
"""
        persona_file.write_text(persona_content)

        config = CompressionConfig()
        compiler = IndexCompiler(temp_hish_root, config=config, use_cache=False)

        output_file = compiler.compress_index(persona_file, level="level2")

        # Should create .L{weight}.compact file
        assert output_file.exists()
        assert output_file.name.startswith("dev_agent_persona.L")
        assert output_file.name.endswith(".compact")

        # Read compact content
        compact_content = output_file.read_text()

        # Original content should be preserved exactly
        assert persona_content in compact_content
        assert "focused, methodical development agent" in compact_content
        assert "Write clean, maintainable code" in compact_content
        assert "Never skip validation steps" in compact_content

        # Should have verbatim header
        assert "Behavioral Context - Uncompressed" in compact_content
        assert "EXCLUDED from compression" in compact_content

    def test_verbatim_vs_compressed_distinction(self, temp_hish_root):
        """Test that verbatim files are tracked separately from compressed."""
        # Create one regular file and one excluded file
        regular_file = temp_hish_root / "local" / "notes.md"
        regular_file.write_text(
            "# Notes\n\n## Long verbose section\nThis contains many words that could be compressed.\n"
        )

        excluded_file = temp_hish_root / "templates" / "dev_agent_persona.md"
        excluded_file.write_text("# Persona\n\nAgent behavior defined here.\n")

        config = CompressionConfig()
        compiler = IndexCompiler(temp_hish_root, config=config, use_cache=False)

        # Compile both
        compiler.compress_index(regular_file, level="level2")
        compiler.compress_index(excluded_file, level="level2")

        # Check processed files
        assert len(compiler.processed_files) == 2

        # Regular file should have compressed strategy
        assert (
            compiler.processed_files["notes.md"]["strategy"]
            == "combined[structural,phrase]"
        )

        # Excluded file should have verbatim strategy
        assert (
            compiler.processed_files["dev_agent_persona.md"]["strategy"]
            == "verbatim_copy"
        )
        assert compiler.processed_files["dev_agent_persona.md"]["reduction_pct"] == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""Test compilation cache functionality."""

import pytest
from pathlib import Path
import tempfile
import shutil
import json
from sbmi.compiler.cache import CompilationCache


class TestCompilationCache:
    """Test the CompilationCache class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def cache_file(self, temp_dir):
        """Create cache file path."""
        return temp_dir / ".sbmi-cache.json"

    @pytest.fixture
    def test_file(self, temp_dir):
        """Create test markdown file."""
        test_file = temp_dir / "test.md"
        test_file.write_text("# Test Content\n")
        return test_file

    def test_cache_initialization_empty(self, cache_file):
        """Test cache initializes with empty dict when file doesn't exist."""
        cache = CompilationCache(cache_file)
        assert cache.cache == {}
        assert cache.cache_file == cache_file

    def test_cache_saves_to_disk(self, cache_file, test_file):
        """Test cache saves to disk correctly."""
        cache = CompilationCache(cache_file)
        output_file = test_file.with_suffix('.compact')

        cache.mark_compiled(test_file, output_file, 25.5)

        # Cache file should exist
        assert cache_file.exists()

        # Should be valid JSON
        data = json.loads(cache_file.read_text())
        assert str(test_file) in data
        assert data[str(test_file)]['reduction_pct'] == 25.5

    def test_cache_loads_from_disk(self, cache_file, test_file):
        """Test cache loads existing data from disk."""
        # Create cache and save data
        cache1 = CompilationCache(cache_file)
        output_file = test_file.with_suffix('.compact')
        cache1.mark_compiled(test_file, output_file, 30.0)

        # Create new cache instance - should load existing data
        cache2 = CompilationCache(cache_file)
        assert str(test_file) in cache2.cache
        assert cache2.cache[str(test_file)]['reduction_pct'] == 30.0

    def test_compute_hash_deterministic(self, test_file):
        """Test that hash computation is deterministic."""
        cache_file = test_file.parent / ".cache.json"
        cache = CompilationCache(cache_file)

        hash1 = cache.compute_hash(test_file)
        hash2 = cache.compute_hash(test_file)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex digest

    def test_compute_hash_changes_with_content(self, test_file):
        """Test that hash changes when file content changes."""
        cache_file = test_file.parent / ".cache.json"
        cache = CompilationCache(cache_file)

        hash1 = cache.compute_hash(test_file)

        # Modify file
        test_file.write_text("# Different Content\n")
        hash2 = cache.compute_hash(test_file)

        assert hash1 != hash2

    def test_has_changed_new_file(self, cache_file, test_file):
        """Test that new file is detected as changed."""
        cache = CompilationCache(cache_file)
        assert cache.has_changed(test_file) is True

    def test_has_changed_unchanged_file(self, cache_file, test_file):
        """Test that unchanged file is not detected as changed."""
        cache = CompilationCache(cache_file)
        output_file = test_file.with_suffix('.compact')

        # Mark as compiled
        cache.mark_compiled(test_file, output_file, 25.0)

        # Should not be changed
        assert cache.has_changed(test_file) is False

    def test_has_changed_modified_file(self, cache_file, test_file):
        """Test that modified file is detected as changed."""
        cache = CompilationCache(cache_file)
        output_file = test_file.with_suffix('.compact')

        # Mark as compiled
        cache.mark_compiled(test_file, output_file, 25.0)
        assert cache.has_changed(test_file) is False

        # Modify file
        test_file.write_text("# Modified Content\n")

        # Should be changed
        assert cache.has_changed(test_file) is True

    def test_mark_compiled_updates_cache(self, cache_file, test_file):
        """Test that mark_compiled updates cache correctly."""
        cache = CompilationCache(cache_file)
        output_file = test_file.with_suffix('.compact')

        cache.mark_compiled(test_file, output_file, 42.5)

        key = str(test_file)
        assert key in cache.cache
        assert cache.cache[key]['hash'] is not None
        assert cache.cache[key]['output'] == str(output_file)
        assert cache.cache[key]['reduction_pct'] == 42.5
        assert 'compiled_at' in cache.cache[key]

    def test_get_changed_files(self, cache_file, temp_dir):
        """Test getting set of changed files."""
        # Create multiple test files
        file1 = temp_dir / "file1.md"
        file2 = temp_dir / "file2.md"
        file3 = temp_dir / "file3.md"

        file1.write_text("Content 1")
        file2.write_text("Content 2")
        file3.write_text("Content 3")

        all_files = {file1, file2, file3}

        cache = CompilationCache(cache_file)

        # All files should be changed (new)
        changed = cache.get_changed_files(all_files)
        assert len(changed) == 3
        assert file1 in changed
        assert file2 in changed
        assert file3 in changed

        # Mark file1 and file2 as compiled
        cache.mark_compiled(file1, file1.with_suffix('.compact'), 10.0)
        cache.mark_compiled(file2, file2.with_suffix('.compact'), 20.0)

        # Only file3 should be changed
        changed = cache.get_changed_files(all_files)
        assert len(changed) == 1
        assert file3 in changed

        # Modify file1
        file1.write_text("Modified content 1")

        # file1 and file3 should be changed
        changed = cache.get_changed_files(all_files)
        assert len(changed) == 2
        assert file1 in changed
        assert file3 in changed

    def test_get_stats_empty_cache(self, cache_file):
        """Test stats for empty cache."""
        cache = CompilationCache(cache_file)
        stats = cache.get_stats()

        assert stats['total_compiled'] == 0
        assert stats['avg_reduction'] == 0.0
        assert stats['last_compiled'] is None

    def test_get_stats_with_data(self, cache_file, temp_dir):
        """Test stats with compiled files."""
        file1 = temp_dir / "file1.md"
        file2 = temp_dir / "file2.md"
        file1.write_text("Content 1")
        file2.write_text("Content 2")

        cache = CompilationCache(cache_file)
        cache.mark_compiled(file1, file1.with_suffix('.compact'), 20.0)
        cache.mark_compiled(file2, file2.with_suffix('.compact'), 40.0)

        stats = cache.get_stats()

        assert stats['total_compiled'] == 2
        assert stats['avg_reduction'] == 30.0  # (20 + 40) / 2
        assert stats['last_compiled'] is not None

    def test_invalidate_specific_file(self, cache_file, test_file):
        """Test invalidating specific file from cache."""
        cache = CompilationCache(cache_file)
        output_file = test_file.with_suffix('.compact')

        cache.mark_compiled(test_file, output_file, 25.0)
        assert str(test_file) in cache.cache

        # Invalidate specific file
        cache.invalidate(test_file)
        assert str(test_file) not in cache.cache

    def test_invalidate_entire_cache(self, cache_file, temp_dir):
        """Test invalidating entire cache."""
        file1 = temp_dir / "file1.md"
        file2 = temp_dir / "file2.md"
        file1.write_text("Content 1")
        file2.write_text("Content 2")

        cache = CompilationCache(cache_file)
        cache.mark_compiled(file1, file1.with_suffix('.compact'), 20.0)
        cache.mark_compiled(file2, file2.with_suffix('.compact'), 30.0)

        assert len(cache.cache) == 2

        # Invalidate all
        cache.invalidate()
        assert len(cache.cache) == 0

    def test_corrupted_cache_loads_empty(self, cache_file):
        """Test that corrupted cache file loads as empty."""
        # Write invalid JSON
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text("{ invalid json }")

        cache = CompilationCache(cache_file)
        assert cache.cache == {}

    def test_cache_survives_reload(self, cache_file, test_file):
        """Test cache data survives multiple load/save cycles."""
        # First cache instance
        cache1 = CompilationCache(cache_file)
        cache1.mark_compiled(test_file, test_file.with_suffix('.compact'), 35.5)

        # Second cache instance
        cache2 = CompilationCache(cache_file)
        assert cache2.has_changed(test_file) is False

        # Modify and re-mark
        test_file.write_text("# New content\n")
        cache2.mark_compiled(test_file, test_file.with_suffix('.compact'), 40.0)

        # Third cache instance
        cache3 = CompilationCache(cache_file)
        assert cache3.has_changed(test_file) is False
        assert cache3.cache[str(test_file)]['reduction_pct'] == 40.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

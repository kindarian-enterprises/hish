"""Unit tests for util module."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open
from util import compile_globs, iter_files, read_text

class TestCompileGlobs:
    """Test the compile_globs function."""

    @pytest.mark.unit
    def test_compile_globs_basic(self):
        """Test basic glob compilation."""
        includes = "*.py,*.md"
        excludes = "__pycache__/**,*.pyc"
        
        inc_spec, exc_spec = compile_globs(includes, excludes)
        
        # Test include patterns
        assert inc_spec.match_file("test.py")
        assert inc_spec.match_file("README.md")
        assert not inc_spec.match_file("test.txt")
        
        # Test exclude patterns  
        assert exc_spec.match_file("__pycache__/test.pyc")
        assert exc_spec.match_file("test.pyc")
        assert not exc_spec.match_file("test.py")

    @pytest.mark.unit 
    def test_compile_globs_empty(self):
        """Test with empty glob patterns."""
        inc_spec, exc_spec = compile_globs("", "")
        
        # Empty includes should not match anything
        assert not inc_spec.match_file("test.py")
        
        # Empty excludes should not exclude anything
        assert not exc_spec.match_file("test.py")

    @pytest.mark.unit
    def test_compile_globs_whitespace(self):
        """Test handling of whitespace in patterns."""
        includes = " *.py , *.md "
        excludes = " __pycache__/** , *.pyc "
        
        inc_spec, exc_spec = compile_globs(includes, excludes)
        
        assert inc_spec.match_file("test.py")
        assert inc_spec.match_file("README.md")
        assert exc_spec.match_file("__pycache__/test.pyc")

    @pytest.mark.unit
    def test_compile_globs_complex_patterns(self):
        """Test complex glob patterns."""
        includes = "**/*.md,src/**/*.py,docs/**"
        excludes = "**/test_*,**/.git/**,**/node_modules/**"
        
        inc_spec, exc_spec = compile_globs(includes, excludes)
        
        # Test complex includes
        assert inc_spec.match_file("docs/README.md")
        assert inc_spec.match_file("src/module/file.py") 
        assert inc_spec.match_file("docs/subdir/file.txt")
        
        # Test complex excludes
        assert exc_spec.match_file("test_something.py")
        assert exc_spec.match_file(".git/config")
        assert exc_spec.match_file("node_modules/package/index.js")


class TestIterFiles:
    """Test the iter_files function."""

    @pytest.mark.unit
    def test_iter_files_basic(self):
        """Test basic file iteration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            (Path(tmpdir) / "test.py").write_text("python code")
            (Path(tmpdir) / "README.md").write_text("markdown")
            (Path(tmpdir) / "ignore.txt").write_text("text")
            
            # Create subdirectory
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            (subdir / "nested.py").write_text("nested python")
            
            inc_spec, exc_spec = compile_globs("*.py,*.md", "*.txt")
            
            files = list(iter_files(tmpdir, inc_spec, exc_spec))
            
            # Should include .py and .md, exclude .txt
            assert "test.py" in files
            assert "README.md" in files
            assert "subdir/nested.py" in files
            assert "ignore.txt" not in files

    @pytest.mark.unit
    def test_iter_files_empty_directory(self):
        """Test with empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            inc_spec, exc_spec = compile_globs("*.py", "")
            
            files = list(iter_files(tmpdir, inc_spec, exc_spec))
            
            assert files == []

    @pytest.mark.unit
    def test_iter_files_no_matches(self):
        """Test when no files match the patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "test.txt").write_text("text")
            (Path(tmpdir) / "data.json").write_text("json")
            
            inc_spec, exc_spec = compile_globs("*.py", "")
            
            files = list(iter_files(tmpdir, inc_spec, exc_spec))
            
            assert files == []

    @pytest.mark.unit
    def test_iter_files_exclude_priority(self):
        """Test that exclude patterns take priority."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "test.py").write_text("python")
            (Path(tmpdir) / "test_excluded.py").write_text("excluded python")
            
            inc_spec, exc_spec = compile_globs("*.py", "test_excluded.py")
            
            files = list(iter_files(tmpdir, inc_spec, exc_spec))
            
            assert "test.py" in files
            assert "test_excluded.py" not in files


class TestReadText:
    """Test the read_text function."""

    @pytest.mark.unit
    def test_read_text_basic(self):
        """Test basic text reading."""
        content = "Hello, World!\nThis is a test file."
        
        with patch("builtins.open", mock_open(read_data=content)):
            result = read_text("test.txt")
            
            assert result == content

    @pytest.mark.unit
    def test_read_text_unicode(self):
        """Test reading unicode content."""
        content = "Hello, 世界! 🌍\nUnicode test file."
        
        with patch("builtins.open", mock_open(read_data=content)):
            result = read_text("unicode.txt")
            
            assert result == content

    @pytest.mark.unit
    def test_read_text_empty_file(self):
        """Test reading empty file."""
        with patch("builtins.open", mock_open(read_data="")):
            result = read_text("empty.txt")
            
            assert result == ""

    @pytest.mark.unit
    @patch("builtins.open")
    def test_read_text_encoding_errors(self, mock_file):
        """Test handling of encoding errors."""
        # Simulate encoding error that gets ignored
        mock_file.side_effect = lambda *args, **kwargs: mock_open(read_data="content")()
        
        result = read_text("problematic.txt")
        
        # Should handle errors gracefully
        assert isinstance(result, str)
        mock_file.assert_called_once_with("problematic.txt", "r", encoding="utf-8", errors="ignore")

    @pytest.mark.unit
    def test_read_text_real_file(self):
        """Test reading a real temporary file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            test_content = "Real file content\nwith multiple lines."
            f.write(test_content)
            f.flush()
            temp_path = f.name
        
        try:
            result = read_text(temp_path)
            assert result == test_content
        finally:
            os.unlink(temp_path)

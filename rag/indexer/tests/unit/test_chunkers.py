"""Unit tests for chunkers module."""

import pytest
from unittest.mock import patch, Mock
from chunkers import chunk_text, prefer_md_splits
from tests.conftest import (
    CHUNK_MAX_TOKENS_TEST, 
    CHUNK_OVERLAP_TOKENS_TEST,
    SAMPLE_MARKDOWN_TEXT,
    SAMPLE_PYTHON_CODE
)

class TestChunkText:
    """Test the chunk_text function."""

    @pytest.mark.unit
    def test_chunk_text_basic(self):
        """Test basic text chunking functionality."""
        text = "This is a simple test text that should be chunked properly."
        
        with patch('chunkers.tiktoken.get_encoding') as mock_encoding:
            # Mock tokenizer behavior
            mock_enc = Mock()
            mock_enc.encode.return_value = list(range(50))  # 50 tokens
            mock_enc.decode.side_effect = lambda tokens: " ".join([f"token{i}" for i in tokens])
            mock_encoding.return_value = mock_enc
            
            chunks = chunk_text(text, max_tokens=20, overlap=5)
            
            assert len(chunks) > 0
            assert all(chunk.strip() for chunk in chunks)  # No empty chunks

    @pytest.mark.unit
    def test_chunk_text_small_text(self):
        """Test chunking with text smaller than max tokens."""
        text = "Short text."
        
        with patch('chunkers.tiktoken.get_encoding') as mock_encoding:
            mock_enc = Mock()
            mock_enc.encode.return_value = [1, 2, 3]  # 3 tokens
            mock_enc.decode.return_value = text
            mock_encoding.return_value = mock_enc
            
            chunks = chunk_text(text, max_tokens=20, overlap=5)
            
            assert len(chunks) == 1
            assert chunks[0] == text

    @pytest.mark.unit
    def test_chunk_text_overlap_handling(self):
        """Test that overlap is handled correctly."""
        text = "A longer piece of text for testing overlap behavior."
        
        with patch('chunkers.tiktoken.get_encoding') as mock_encoding:
            mock_enc = Mock()
            mock_enc.encode.return_value = list(range(100))  # 100 tokens
            mock_enc.decode.side_effect = lambda tokens: f"chunk_{min(tokens)}_{max(tokens)}"
            mock_encoding.return_value = mock_enc
            
            chunks = chunk_text(text, max_tokens=30, overlap=10)
            
            assert len(chunks) > 1
            # Should have multiple chunks due to overlap
            expected_chunks = 4  # 100 tokens / (30-10) overlap = ~4 chunks
            assert len(chunks) >= expected_chunks - 1

    @pytest.mark.unit
    def test_chunk_text_edge_cases(self):
        """Test edge cases for chunking."""
        # Empty text
        assert chunk_text("") == []
        
        # Whitespace only
        assert chunk_text("   \n\t   ") == []
        
        # Single character
        with patch('chunkers.tiktoken.get_encoding') as mock_encoding:
            mock_enc = Mock()
            mock_enc.encode.return_value = [1]
            mock_enc.decode.return_value = "a"
            mock_encoding.return_value = mock_enc
            
            chunks = chunk_text("a", max_tokens=10)
            assert chunks == ["a"]


class TestPreferMdSplits:
    """Test the prefer_md_splits function."""

    @pytest.mark.unit
    def test_prefer_md_splits_with_headings(self):
        """Test splitting on markdown headings."""
        text = SAMPLE_MARKDOWN_TEXT
        
        splits = prefer_md_splits(text)
        
        assert len(splits) > 1
        # Should have content sections
        content_splits = [s for s in splits if s and len(s.strip()) > 0]
        assert len(content_splits) >= 3  # At least a few meaningful sections

    @pytest.mark.unit
    def test_prefer_md_splits_with_lists(self):
        """Test splitting on markdown lists."""
        text = """
Some introduction text.

- First item
- Second item  
- Third item

Conclusion text.
"""
        
        splits = prefer_md_splits(text)
        
        # Should split on list items and blank lines
        assert len(splits) > 1
        content_splits = [s for s in splits if s and len(s.strip()) > 0]
        assert any("introduction" in s.lower() for s in content_splits)
        assert any("conclusion" in s.lower() for s in content_splits)

    @pytest.mark.unit
    def test_prefer_md_splits_plain_text(self):
        """Test with plain text (no markdown)."""
        text = "This is just plain text without any markdown formatting."
        
        splits = prefer_md_splits(text)
        
        # Should return the text as a single split (after filtering)
        content_splits = [s for s in splits if s and len(s.strip()) > 0]
        assert len(content_splits) >= 1

    @pytest.mark.unit
    def test_prefer_md_splits_empty_input(self):
        """Test with empty or whitespace input."""
        assert prefer_md_splits("") == []
        assert prefer_md_splits("   \n\t   ") == []

    @pytest.mark.unit
    def test_prefer_md_splits_code_content(self):
        """Test with code-like content."""
        text = SAMPLE_PYTHON_CODE
        
        splits = prefer_md_splits(text)
        
        # Should handle code content gracefully
        content_splits = [s for s in splits if s and len(s.strip()) > 0]
        assert len(content_splits) >= 1

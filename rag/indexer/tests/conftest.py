"""Test configuration and fixtures."""

import pytest
from typing import Dict, Any, List
from unittest.mock import Mock, MagicMock

# Test constants following Mayr standards - no magic numbers
CHUNK_MAX_TOKENS_TEST = 100
CHUNK_MIN_CHARS_TEST = 50
CHUNK_OVERLAP_TOKENS_TEST = 20
EXPECTED_EMBEDDING_DIMENSION = 384
BATCH_SIZE_TEST = 2
TEST_COLLECTION_NAME = "test_collection"

# Sample test data
SAMPLE_MARKDOWN_TEXT = """# Test Document

This is a test document with multiple sections.

## Section 1

Some content in the first section with enough text to create meaningful chunks.

## Section 2

More content in the second section that should be processed correctly.

- List item 1
- List item 2
- List item 3

The end of the document.
"""

SAMPLE_PYTHON_CODE = '''"""A sample Python file for testing."""

def hello_world():
    """Print hello world."""
    print("Hello, World!")
    return "success"

class TestClass:
    """A test class."""
    
    def __init__(self):
        self.value = 42
    
    def method(self):
        """A test method."""
        return self.value * 2
'''

@pytest.fixture
def sample_files():
    """Sample files for testing file processing."""
    return {
        "docs/test.md": SAMPLE_MARKDOWN_TEXT,
        "src/test.py": SAMPLE_PYTHON_CODE,
        "README.md": "# Test Repository\n\nA simple test repository.",
        "config.json": '{"setting": "value", "number": 42}',
    }

@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client for testing."""
    client = Mock()
    client.get_collection.side_effect = Exception("Collection not found")
    client.recreate_collection.return_value = None
    client.upsert.return_value = None
    return client

@pytest.fixture
def mock_text_embedding():
    """Mock text embedding model."""
    model = Mock()
    # Return consistent embeddings for testing
    def mock_embed(texts):
        return [[0.1] * EXPECTED_EMBEDDING_DIMENSION for _ in texts]
    
    model.embed.side_effect = mock_embed
    return model

@pytest.fixture
def test_environment_vars():
    """Environment variables for testing."""
    return {
        "QDRANT_URL": "http://localhost:6333",
        "QDRANT_API_KEY": "",
        "COLLECTION_NAME": TEST_COLLECTION_NAME,
        "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2",
        "INDEX_INCLUDE": "**/*.md,**/*.py",
        "INDEX_EXCLUDE": "**/.git/**,**/.data/**",
        "CHUNK_MAX_TOKENS": str(CHUNK_MAX_TOKENS_TEST),
        "CHUNK_MIN_CHARS": str(CHUNK_MIN_CHARS_TEST),
        "CHUNK_OVERLAP_TOKENS": str(CHUNK_OVERLAP_TOKENS_TEST),
    }

"""Integration tests for app.py."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock
from app import ensure_collection, embedder, guess_dim, index_repo, main
from tests.conftest import (
    EXPECTED_EMBEDDING_DIMENSION,
    TEST_COLLECTION_NAME,
    TEST_MODEL_NAME,
    CHUNK_MAX_TOKENS_TEST,
    CHUNK_MIN_CHARS_TEST,
    CHUNK_OVERLAP_TOKENS_TEST,
    SAMPLE_MARKDOWN_TEXT,
    SAMPLE_PYTHON_CODE
)


class TestEnsureCollection:
    """Test the ensure_collection function."""

    @pytest.mark.integration
    def test_ensure_collection_exists(self, mock_qdrant_client):
        """Test when collection already exists."""
        # Reset the side_effect and set return_value to mock successful collection response
        mock_qdrant_client.get_collection.side_effect = None
        # Mock a collection info object that has vectors_count attribute
        mock_collection_info = Mock()
        mock_collection_info.vectors_count = 100
        mock_qdrant_client.get_collection.return_value = mock_collection_info

        # Should not raise exception
        ensure_collection(mock_qdrant_client, TEST_COLLECTION_NAME,
                          EXPECTED_EMBEDDING_DIMENSION, "BAAI/bge-small-en-v1.5")

        mock_qdrant_client.get_collection.assert_called_once_with(
            TEST_COLLECTION_NAME)
        mock_qdrant_client.recreate_collection.assert_not_called()

    @pytest.mark.integration
    def test_ensure_collection_create_new(self, mock_qdrant_client):
        """Test creating new collection when it doesn't exist."""
        mock_qdrant_client.get_collection.side_effect = Exception("Not found")

        ensure_collection(mock_qdrant_client, TEST_COLLECTION_NAME,
                          EXPECTED_EMBEDDING_DIMENSION, "BAAI/bge-small-en-v1.5")

        mock_qdrant_client.get_collection.assert_called_once_with(
            TEST_COLLECTION_NAME)
        mock_qdrant_client.recreate_collection.assert_called_once()


class TestEmbedder:
    """Test the embedder function."""

    @pytest.mark.integration
    @patch('app.TextEmbedding')
    def test_embedder_initialization(self, mock_text_embedding):
        """Test embedder model initialization."""
        model_name = "BAAI/bge-small-en-v1.5"
        mock_model = Mock()
        mock_text_embedding.return_value = mock_model

        result = embedder(model_name)

        mock_text_embedding.assert_called_once_with(model_name=model_name)
        assert result == mock_model


class TestGuessDim:
    """Test the guess_dim function."""

    @pytest.mark.integration
    def test_guess_dim_returns_384(self):
        """Test that guess_dim returns expected dimension."""
        # Test various model names
        assert guess_dim(
            "BAAI/bge-small-en-v1.5") == EXPECTED_EMBEDDING_DIMENSION
        assert guess_dim("custom-model") == EXPECTED_EMBEDDING_DIMENSION


class TestIndexRepo:
    """Test the index_repo function with mocked dependencies."""

    @pytest.mark.integration
    def test_index_repo_basic(self, mock_qdrant_client, mock_text_embedding):
        """Test basic repository indexing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            (Path(tmpdir) / "test.md").write_text(SAMPLE_MARKDOWN_TEXT)
            (Path(tmpdir) / "code.py").write_text(SAMPLE_PYTHON_CODE)
            (Path(tmpdir) / "ignore.txt").write_text("ignored content")

            with patch('app.embedder', return_value=mock_text_embedding), \
                    patch('app.QdrantClient', return_value=mock_qdrant_client):

                index_repo(
                    work_root=tmpdir,
                    qdrant_url="http://localhost:6333",
                    api_key="",
                    collection=TEST_COLLECTION_NAME,
                    model_name="test-model",
                    includes="*.md,*.py",
                    excludes="*.txt",
                    chunk_max_tokens=CHUNK_MAX_TOKENS_TEST,
                    chunk_min_chars=CHUNK_MIN_CHARS_TEST,
                    chunk_overlap=CHUNK_OVERLAP_TOKENS_TEST
                )

                # Verify collection was ensured
                mock_qdrant_client.get_collection.assert_called()

                # Verify embedding was called
                mock_text_embedding.embed.assert_called()

                # Verify upsert was called with points
                mock_qdrant_client.upsert.assert_called()

    @pytest.mark.integration
    def test_index_repo_empty_directory(self, mock_qdrant_client, mock_text_embedding):
        """Test indexing empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('app.embedder', return_value=mock_text_embedding), \
                    patch('app.QdrantClient', return_value=mock_qdrant_client):

                index_repo(
                    work_root=tmpdir,
                    qdrant_url="http://localhost:6333",
                    api_key="",
                    collection=TEST_COLLECTION_NAME,
                    model_name="test-model",
                    includes="*.md",
                    excludes="",
                    chunk_max_tokens=CHUNK_MAX_TOKENS_TEST,
                    chunk_min_chars=CHUNK_MIN_CHARS_TEST,
                    chunk_overlap=CHUNK_OVERLAP_TOKENS_TEST
                )

                # Should still ensure collection
                mock_qdrant_client.get_collection.assert_called()

                # Should not call embed or upsert for empty directory
                mock_text_embedding.embed.assert_not_called()
                mock_qdrant_client.upsert.assert_not_called()

    @pytest.mark.integration
    def test_index_repo_with_small_chunks(self, mock_qdrant_client, mock_text_embedding):
        """Test that small chunks are filtered out."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file with very short content
            (Path(tmpdir) / "short.md").write_text("x")  # Very short content

            with patch('app.embedder', return_value=mock_text_embedding), \
                    patch('app.QdrantClient', return_value=mock_qdrant_client):

                index_repo(
                    work_root=tmpdir,
                    qdrant_url="http://localhost:6333",
                    api_key="",
                    collection=TEST_COLLECTION_NAME,
                    model_name="test-model",
                    includes="*.md",
                    excludes="",
                    chunk_max_tokens=CHUNK_MAX_TOKENS_TEST,
                    chunk_min_chars=CHUNK_MIN_CHARS_TEST,  # Higher than content length
                    chunk_overlap=CHUNK_OVERLAP_TOKENS_TEST
                )

                # Should not process chunks that are too small
                mock_text_embedding.embed.assert_not_called()
                mock_qdrant_client.upsert.assert_not_called()

    @pytest.mark.integration
    def test_index_repo_batch_processing(self, mock_qdrant_client, mock_text_embedding):
        """Test that batching works correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple files to trigger batching
            for i in range(5):
                (Path(tmpdir) /
                 f"file_{i}.md").write_text(SAMPLE_MARKDOWN_TEXT)

            with patch('app.embedder', return_value=mock_text_embedding), \
                    patch('app.QdrantClient', return_value=mock_qdrant_client):

                index_repo(
                    work_root=tmpdir,
                    qdrant_url="http://localhost:6333",
                    api_key="",
                    collection=TEST_COLLECTION_NAME,
                    model_name="test-model",
                    includes="*.md",
                    excludes="",
                    chunk_max_tokens=CHUNK_MAX_TOKENS_TEST,
                    chunk_min_chars=CHUNK_MIN_CHARS_TEST,
                    chunk_overlap=CHUNK_OVERLAP_TOKENS_TEST
                )

                # Should have called upsert at least once
                assert mock_qdrant_client.upsert.call_count >= 1


class TestMain:
    """Test the main function."""

    @pytest.mark.integration
    @patch('app.index_repo')
    @patch('os.getenv')
    def test_main_default_args(self, mock_getenv, mock_index_repo):
        """Test main function with default arguments."""
        # Mock environment variables
        env_vars = {
            "QDRANT_URL": "http://localhost:6333",
            "QDRANT_API_KEY": "",
            "COLLECTION_NAME": TEST_COLLECTION_NAME,
            "EMBEDDING_MODEL": "test-model",
            "INDEX_INCLUDE": "*.md",
            "INDEX_EXCLUDE": "*.txt",
            "CHUNK_MAX_TOKENS": str(CHUNK_MAX_TOKENS_TEST),
            "CHUNK_MIN_CHARS": str(CHUNK_MIN_CHARS_TEST),
            "CHUNK_OVERLAP_TOKENS": str(CHUNK_OVERLAP_TOKENS_TEST),
        }
        mock_getenv.side_effect = lambda key, default="": env_vars.get(
            key, default)

        with patch('sys.argv', ['app.py']):
            main()

            mock_index_repo.assert_called_once()
            args = mock_index_repo.call_args[1]  # Get keyword arguments
            assert args['qdrant_url'] == "http://localhost:6333"
            assert args['collection'] == TEST_COLLECTION_NAME

    @pytest.mark.integration
    @patch('app.QdrantClient')
    @patch('os.getenv')
    def test_main_recreate_flag(self, mock_getenv, mock_qdrant_client):
        """Test main function with --recreate flag."""
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        env_vars = {
            "QDRANT_URL": "http://localhost:6333",
            "COLLECTION_NAME": TEST_COLLECTION_NAME,
        }
        mock_getenv.side_effect = lambda key, default="": env_vars.get(
            key, default)

        with patch('sys.argv', ['app.py', '--recreate']), \
                patch('app.index_repo'):

            main()

            # Should recreate collection with named vector config for MCP compatibility
            from qdrant_client.http.models import VectorParams, Distance
            expected_vectors_config = {TEST_MODEL_NAME: VectorParams(
                size=EXPECTED_EMBEDDING_DIMENSION, distance=Distance.COSINE)}
            mock_client.recreate_collection.assert_called_once_with(
                TEST_COLLECTION_NAME,
                vectors_config=expected_vectors_config
            )

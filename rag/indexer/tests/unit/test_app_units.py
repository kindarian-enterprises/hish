"""
Unit tests for app.py functions that need better coverage.

These tests focus on isolated unit testing of individual functions
without heavy mocking or integration concerns.
"""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest

from app import (
    ensure_model_suffix,
    get_model_suffix,
    get_optimal_model,
    guess_dim,
    is_code_collection,
    process_single_file,
)
from tests.conftest import (
    EXPECTED_EMBEDDING_DIMENSION,
    SAMPLE_MARKDOWN_TEXT,
    SAMPLE_PYTHON_CODE,
    TEST_COLLECTION_NAME,
    TEST_MODEL_NAME,
)


class TestGuessDocumentationCoverage:
    """Test guess_dim function thoroughly for all code paths."""

    @pytest.mark.unit
    def test_guess_dim_bge_variants(self):
        """Test all BGE model variants."""
        # BGE small variants
        assert guess_dim("BAAI/bge-small-en-v1.5") == 384
        assert guess_dim("bge-small-chinese") == 384
        assert guess_dim("BGE-SMALL-MULTILINGUAL") == 384

        # BGE base variants
        assert guess_dim("BAAI/bge-base-en-v1.5") == 768
        assert guess_dim("bge-base-chinese") == 768
        assert guess_dim("BGE-BASE-MULTILINGUAL") == 768

        # BGE large variants
        assert guess_dim("BAAI/bge-large-en-v1.5") == 1024
        assert guess_dim("bge-large-chinese") == 1024
        assert guess_dim("BGE-LARGE-MULTILINGUAL") == 1024

        # Generic BGE (should default to small)
        assert guess_dim("bge-custom") == 384
        assert guess_dim("BGE-EXPERIMENTAL") == 384

    @pytest.mark.unit
    def test_guess_dim_other_models(self):
        """Test dimension guessing for other model types."""
        # MiniLM models
        assert guess_dim("sentence-transformers/all-MiniLM-L6-v2") == 384
        assert guess_dim("minilm-base") == 384
        assert guess_dim("MINILM-LARGE") == 384

        # MPNet models
        assert (
            guess_dim("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
            == 768
        )
        assert guess_dim("PARAPHRASE-MULTILINGUAL-MPNET-BASE-V2") == 768

        # Unknown models (should default to MPNet dimensions)
        assert guess_dim("unknown-model") == 768
        assert guess_dim("custom/embedding-model") == 768
        assert guess_dim("") == 768

    @pytest.mark.unit
    def test_guess_dim_case_insensitive(self):
        """Test that guess_dim is case insensitive."""
        model_pairs = [
            ("bge-small", "BGE-SMALL"),
            ("bge-base", "BGE-BASE"),
            ("bge-large", "BGE-LARGE"),
            ("minilm", "MINILM"),
            ("mpnet", "MPNET"),
        ]

        for lower, upper in model_pairs:
            assert guess_dim(lower) == guess_dim(upper)


class TestCollectionHelpers:
    """Test collection helper functions thoroughly."""

    @pytest.mark.unit
    def test_is_code_collection_edge_cases(self):
        """Test is_code_collection with edge cases."""
        # Code collections
        code_collections = [
            "project_code",
            "adamantite_code",
            "platform-backend_code",
            "my-awesome-project_code",
            "test123_code",
        ]

        for collection in code_collections:
            assert is_code_collection(collection), f"Failed for {collection}"

        # Non-code collections
        non_code_collections = [
            "hish_framework",
            "cross_project_intelligence",
            "documentation",
            "project_docs",
            "code_documentation",  # Contains 'code' but doesn't end with '_code'
            "codecov_reports",  # Contains 'code' but doesn't end with '_code'
            "",  # Empty string
            "project",  # Simple name
            "collection_name",  # Generic name
        ]

        for collection in non_code_collections:
            assert not is_code_collection(collection), f"Failed for {collection}"

    @pytest.mark.unit
    def test_get_model_suffix_edge_cases(self):
        """Test get_model_suffix with edge cases."""
        # Test exact matches
        assert (
            get_model_suffix(
                "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
            )
            == "mpnet"
        )
        assert get_model_suffix("BAAI/bge-small-en-v1.5") == "bge"

        # Test partial matches (case insensitive)
        assert (
            get_model_suffix(
                "SENTENCE-TRANSFORMERS/PARAPHRASE-MULTILINGUAL-MPNET-BASE-V2"
            )
            == "mpnet"
        )
        assert get_model_suffix("baai/BGE-SMALL-en-v1.5") == "bge"

        # Test unknown models
        assert get_model_suffix("openai/text-embedding-ada-002") == "unknown"
        assert get_model_suffix("custom/model") == "unknown"
        assert get_model_suffix("") == "unknown"
        assert get_model_suffix("random-string") == "unknown"

    @pytest.mark.unit
    def test_ensure_model_suffix_complex_names(self):
        """Test ensure_model_suffix with complex collection names."""
        test_cases = [
            # (input_collection, model_name, expected_output)
            (
                "my-complex_collection-name",
                TEST_MODEL_NAME,
                "my-complex_collection-name_mpnet",
            ),
            (
                "collection_with_underscores",
                TEST_MODEL_NAME,
                "collection_with_underscores_mpnet",
            ),
            ("collection-with-dashes", TEST_MODEL_NAME, "collection-with-dashes_mpnet"),
            ("collection123", TEST_MODEL_NAME, "collection123_mpnet"),
            (
                "collection_bge",
                TEST_MODEL_NAME,
                "collection_mpnet",
            ),  # Removes _bge, adds _mpnet
            (
                "collection_code",
                TEST_MODEL_NAME,
                "collection_code_mpnet",
            ),  # Preserves _code, adds _mpnet
            ("already_mpnet", TEST_MODEL_NAME, "already_mpnet"),  # Already correct
        ]

        for input_name, model_name, expected in test_cases:
            result = ensure_model_suffix(input_name, model_name)
            assert (
                result == expected
            ), f"Failed for {input_name}: got {result}, expected {expected}"

    @pytest.mark.unit
    def test_get_optimal_model_coverage(self):
        """Test get_optimal_model function coverage."""
        # Test without override (should always return MPNet now)
        assert get_optimal_model("any_collection") == TEST_MODEL_NAME
        assert get_optimal_model("project_code") == TEST_MODEL_NAME
        assert get_optimal_model("hish_framework") == TEST_MODEL_NAME

        # Test with override
        custom_model = "custom/embedding-model"
        assert get_optimal_model("any_collection", custom_model) == custom_model
        assert get_optimal_model("project_code", custom_model) == custom_model
        assert get_optimal_model("hish_framework", custom_model) == custom_model

        # Test with empty override (empty string is falsy, so it should return default)
        assert get_optimal_model("any_collection", "") == TEST_MODEL_NAME
        assert get_optimal_model("any_collection", None) == TEST_MODEL_NAME


class TestProcessSingleFileUnit:
    """Unit tests for process_single_file function."""

    @pytest.fixture
    def temp_file_setup(self):
        """Create temporary files for testing."""
        temp_dir = tempfile.mkdtemp()

        files = {
            "test.py": SAMPLE_PYTHON_CODE,
            "test.md": SAMPLE_MARKDOWN_TEXT,
            "empty.txt": "",
            "large.txt": "x" * 10000,  # Large file
        }

        file_paths = {}
        for filename, content in files.items():
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            file_paths[filename] = file_path

        return temp_dir, file_paths

    @pytest.mark.unit
    def test_process_single_file_basic(self, temp_file_setup):
        """Test basic file processing."""
        temp_dir, file_paths = temp_file_setup

        mock_model = Mock()
        mock_model.embed.return_value = [[0.1] * EXPECTED_EMBEDDING_DIMENSION]

        with patch("app.read_text") as mock_read_text:
            mock_read_text.return_value = SAMPLE_PYTHON_CODE

            filename, points, file_size = process_single_file(
                rel="test.py",
                work_root=temp_dir,
                model=mock_model,
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                model_name=TEST_MODEL_NAME,
                max_file_size_mb=1,
                collection=TEST_COLLECTION_NAME,
            )

            assert filename == "test.py"
            assert len(points) > 0
            assert file_size > 0
            mock_model.embed.assert_called()

    @pytest.mark.unit
    def test_process_single_file_empty_file(self, temp_file_setup):
        """Test processing of empty files."""
        temp_dir, file_paths = temp_file_setup

        mock_model = Mock()

        with patch("app.read_text") as mock_read_text:
            mock_read_text.return_value = ""

            filename, points, file_size = process_single_file(
                rel="empty.txt",
                work_root=temp_dir,
                model=mock_model,
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                model_name=TEST_MODEL_NAME,
                max_file_size_mb=1,
                collection=TEST_COLLECTION_NAME,
            )

            assert filename == "empty.txt"
            assert len(points) == 0  # No points for empty file
            assert file_size >= 0

    @pytest.mark.unit
    def test_process_single_file_file_too_large(self, temp_file_setup):
        """Test handling of files that are too large."""
        temp_dir, file_paths = temp_file_setup

        mock_model = Mock()

        with (
            patch("app.read_text") as mock_read_text,
            patch("os.path.getsize") as mock_getsize,
        ):
            # Mock file size to be larger than limit
            mock_getsize.return_value = 2 * 1024 * 1024  # 2MB
            mock_read_text.return_value = "small content"

            filename, points, file_size = process_single_file(
                rel="large.txt",
                work_root=temp_dir,
                model=mock_model,
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                model_name=TEST_MODEL_NAME,
                max_file_size_mb=1,  # 1MB limit
                collection=TEST_COLLECTION_NAME,
            )

            assert filename == "large.txt"
            assert len(points) == 0  # No points for oversized file
            assert file_size == 0  # File size is set to 0 when skipped

    @pytest.mark.unit
    def test_process_single_file_read_error(self, temp_file_setup):
        """Test handling of file read errors."""
        temp_dir, file_paths = temp_file_setup

        mock_model = Mock()

        with patch("app.read_text") as mock_read_text:
            mock_read_text.side_effect = Exception("File read error")

            filename, points, file_size = process_single_file(
                rel="test.py",
                work_root=temp_dir,
                model=mock_model,
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                model_name=TEST_MODEL_NAME,
                max_file_size_mb=1,
                collection=TEST_COLLECTION_NAME,
            )

            assert filename == "test.py"
            assert len(points) == 0  # No points due to error
            assert file_size >= 0

    @pytest.mark.unit
    def test_process_single_file_embedding_error(self, temp_file_setup):
        """Test handling of embedding errors."""
        temp_dir, file_paths = temp_file_setup

        mock_model = Mock()
        mock_model.embed.side_effect = Exception("Embedding failed")

        with patch("app.read_text") as mock_read_text:
            mock_read_text.return_value = SAMPLE_PYTHON_CODE

            filename, points, file_size = process_single_file(
                rel="test.py",
                work_root=temp_dir,
                model=mock_model,
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                model_name=TEST_MODEL_NAME,
                max_file_size_mb=1,
                collection=TEST_COLLECTION_NAME,
            )

            assert filename == "test.py"
            assert len(points) == 0  # No points due to embedding error
            assert file_size == 0  # File size is set to 0 when embedding fails

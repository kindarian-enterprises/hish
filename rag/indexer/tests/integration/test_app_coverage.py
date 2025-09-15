"""
Additional tests to improve app.py coverage.

These tests focus on covering the missing code paths identified in coverage reports,
particularly around file processing, error handling, and command-line functionality.
"""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest

from app import (
    ensure_model_suffix,
    get_model_suffix,
    get_optimal_model,
    is_code_collection,
    main,
    process_files_in_chunks,
)
from tests.conftest import (
    EXPECTED_EMBEDDING_DIMENSION,
    SAMPLE_MARKDOWN_TEXT,
    SAMPLE_PYTHON_CODE,
    TEST_COLLECTION_NAME,
    TEST_MODEL_NAME,
)


class TestProcessFilesInChunks:
    """Test the process_files_in_chunks function for large repository handling."""

    @pytest.fixture
    def mock_setup(self):
        """Set up mocks for file processing tests."""
        mock_client = Mock()
        mock_model = Mock()
        mock_model.embed.return_value = [[0.1] * EXPECTED_EMBEDDING_DIMENSION]

        # Create temporary files
        temp_dir = tempfile.mkdtemp()
        files = []

        # Create test files
        test_files = {
            "test1.py": SAMPLE_PYTHON_CODE,
            "test2.md": SAMPLE_MARKDOWN_TEXT,
            "test3.py": "print('small file')",
        }

        for filename, content in test_files.items():
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, "w") as f:
                f.write(content)
            files.append(filename)

        return {
            "client": mock_client,
            "model": mock_model,
            "temp_dir": temp_dir,
            "files": files,
        }

    @pytest.mark.integration
    def test_process_files_in_chunks_basic(self, mock_setup):
        """Test basic file processing in chunks."""
        setup = mock_setup

        with patch("app.process_single_file") as mock_process_single:
            # Mock return: (filename, points, file_size)
            mock_process_single.return_value = (
                "test.py",
                [Mock(id=1, vector=[0.1] * EXPECTED_EMBEDDING_DIMENSION)],
                1024,
            )

            total_files, total_chunks = process_files_in_chunks(
                files_to_process=setup["files"],
                work_root=setup["temp_dir"],
                model=setup["model"],
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                optimal_model=TEST_MODEL_NAME,
                max_file_size_mb=1,
                collection=TEST_COLLECTION_NAME,
                client=setup["client"],
                batch_size=2,
                repo_chunk_size=2,
                memory_cleanup_interval=2,
                max_workers=1,
            )

            assert total_files == len(setup["files"])
            assert total_chunks >= 0
            assert mock_process_single.call_count == len(setup["files"])
            setup["client"].upsert.assert_called()

    @pytest.mark.integration
    def test_process_files_in_chunks_large_repo(self, mock_setup):
        """Test chunked processing for large repositories."""
        setup = mock_setup

        # Create many more files to trigger chunking
        large_file_list = setup["files"] * 10  # 30 files total

        with patch("app.process_single_file") as mock_process_single:
            mock_process_single.return_value = (
                "test.py",
                [Mock(id=1, vector=[0.1] * EXPECTED_EMBEDDING_DIMENSION)],
                2048,
            )

            total_files, total_chunks = process_files_in_chunks(
                files_to_process=large_file_list,
                work_root=setup["temp_dir"],
                model=setup["model"],
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                optimal_model=TEST_MODEL_NAME,
                max_file_size_mb=1,
                collection=TEST_COLLECTION_NAME,
                client=setup["client"],
                batch_size=5,
                repo_chunk_size=3,  # Small chunks to test chunking logic
                memory_cleanup_interval=5,
                max_workers=1,
            )

            assert total_files == len(large_file_list)
            assert mock_process_single.call_count == len(large_file_list)
            # Should have multiple upsert calls due to batching
            assert setup["client"].upsert.call_count >= 2

    @pytest.mark.integration
    def test_process_files_in_chunks_error_handling(self, mock_setup):
        """Test error handling in file processing."""
        setup = mock_setup

        with patch("app.process_single_file") as mock_process_single:
            # First file succeeds, second fails, third succeeds
            mock_process_single.side_effect = [
                ("test1.py", [Mock(id=1)], 1024),
                Exception("Processing failed"),
                ("test3.py", [Mock(id=3)], 512),
            ]

            # Should not raise exception, should continue processing
            total_files, total_chunks = process_files_in_chunks(
                files_to_process=setup["files"],
                work_root=setup["temp_dir"],
                model=setup["model"],
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                optimal_model=TEST_MODEL_NAME,
                max_file_size_mb=1,
                collection=TEST_COLLECTION_NAME,
                client=setup["client"],
                batch_size=10,
                repo_chunk_size=10,
                memory_cleanup_interval=10,
                max_workers=1,
            )

            # Should process successful files despite errors
            assert total_files >= 2
            assert mock_process_single.call_count == 3

    @pytest.mark.integration
    def test_process_files_in_chunks_upsert_error(self, mock_setup):
        """Test handling of Qdrant upsert errors."""
        setup = mock_setup
        setup["client"].upsert.side_effect = Exception("Qdrant connection failed")

        with patch("app.process_single_file") as mock_process_single:
            mock_process_single.return_value = (
                "test.py",
                [Mock(id=1, vector=[0.1] * EXPECTED_EMBEDDING_DIMENSION)],
                1024,
            )

            # Should not raise exception, should log error and continue
            total_files, total_chunks = process_files_in_chunks(
                files_to_process=setup["files"][:1],  # Just one file
                work_root=setup["temp_dir"],
                model=setup["model"],
                chunk_max_tokens=100,
                chunk_min_chars=50,
                chunk_overlap=20,
                optimal_model=TEST_MODEL_NAME,
                max_file_size_mb=1,
                collection=TEST_COLLECTION_NAME,
                client=setup["client"],
                batch_size=1,  # Force immediate upsert
                repo_chunk_size=10,
                memory_cleanup_interval=10,
                max_workers=1,
            )

            assert total_files == 1
            setup["client"].upsert.assert_called()


class TestModelHelperFunctions:
    """Test the model helper functions for coverage."""

    @pytest.mark.unit
    def test_get_model_suffix_all_models(self):
        """Test get_model_suffix with various model names."""
        assert (
            get_model_suffix(
                "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
            )
            == "mpnet"
        )
        assert get_model_suffix("BAAI/bge-small-en-v1.5") == "bge"
        assert get_model_suffix("unknown-model") == "unknown"
        assert get_model_suffix("") == "unknown"

    @pytest.mark.unit
    def test_ensure_model_suffix_variations(self):
        """Test ensure_model_suffix with various collection names."""
        # Test adding suffix
        assert (
            ensure_model_suffix("test_collection", TEST_MODEL_NAME)
            == "test_collection_mpnet"
        )

        # Test replacing existing suffix
        assert (
            ensure_model_suffix("test_collection_bge", TEST_MODEL_NAME)
            == "test_collection_mpnet"
        )
        assert (
            ensure_model_suffix("test_collection_code", TEST_MODEL_NAME)
            == "test_collection_code_mpnet"
        )

        # Test with already correct suffix
        assert (
            ensure_model_suffix("test_collection_mpnet", TEST_MODEL_NAME)
            == "test_collection_mpnet"
        )

    @pytest.mark.unit
    def test_is_code_collection_variations(self):
        """Test is_code_collection with various collection names."""
        # Code collections
        assert is_code_collection("project_code")
        assert is_code_collection("adamantite_code")
        assert is_code_collection("platform-backend_code")

        # Framework collections
        assert not is_code_collection("hish_framework")
        assert not is_code_collection("cross_project_intelligence")
        assert not is_code_collection("documentation")

    @pytest.mark.unit
    def test_get_optimal_model_with_override(self):
        """Test get_optimal_model with override parameter."""
        override_model = "custom/model"

        # Override should always be used
        assert get_optimal_model("any_collection", override_model) == override_model
        assert get_optimal_model("project_code", override_model) == override_model
        assert get_optimal_model("hish_framework", override_model) == override_model


class TestMainFunctionCoverage:
    """Test main function and command-line argument parsing."""

    @pytest.mark.integration
    @patch("app.index_repo")
    @patch("app.QdrantClient")
    def test_main_with_debug_flag(self, mock_qdrant_client, mock_index_repo):
        """Test main function with debug flag."""
        mock_index_repo.side_effect = Exception("Test error")

        with (
            patch("sys.argv", ["app.py", "--debug", "--workdir", "/tmp"]),
            patch("os.getenv") as mock_getenv,
            pytest.raises(SystemExit) as exc_info,
        ):
            mock_getenv.side_effect = lambda key, default="": {
                "QDRANT_URL": "http://localhost:6333",
                "COLLECTION_NAME": TEST_COLLECTION_NAME,
                "EMBEDDING_MODEL": TEST_MODEL_NAME,
                "INDEX_INCLUDE": "**/*.py",
                "INDEX_EXCLUDE": "**/.git/**",
            }.get(key, default)

            main()

        assert exc_info.value.code == 1

    @pytest.mark.integration
    @patch("app.index_repo")
    @patch("app.QdrantClient")
    def test_main_with_custom_args(self, mock_qdrant_client, mock_index_repo):
        """Test main function with custom command-line arguments."""
        with (
            patch(
                "sys.argv",
                [
                    "app.py",
                    "--workdir",
                    "/tmp",
                    "--workers",
                    "4",
                    "--batch-size",
                    "64",
                    "--debug",
                ],
            ),
            patch("os.getenv") as mock_getenv,
        ):
            mock_getenv.side_effect = lambda key, default="": {
                "QDRANT_URL": "http://localhost:6333",
                "COLLECTION_NAME": TEST_COLLECTION_NAME,
                "EMBEDDING_MODEL": TEST_MODEL_NAME,
                "INDEX_INCLUDE": "**/*.py",
                "INDEX_EXCLUDE": "**/.git/**",
                "CHUNK_MAX_TOKENS": "500",
                "CHUNK_MIN_CHARS": "100",
                "CHUNK_OVERLAP_TOKENS": "50",
                "MAX_WORKERS": "8",  # Should be overridden by command line
                "BATCH_SIZE": "128",  # Should be overridden by command line
            }.get(key, default)

            main()

            # Verify command line args override environment variables
            mock_index_repo.assert_called_once()
            call_args = mock_index_repo.call_args
            # Command line overrides env
            assert call_args[1]["max_workers"] == 4
            # Command line overrides env
            assert call_args[1]["batch_size"] == 64

    @pytest.mark.integration
    @patch("app.index_repo")
    @patch("app.QdrantClient")
    def test_main_environment_variable_parsing(
        self, mock_qdrant_client, mock_index_repo
    ):
        """Test main function environment variable parsing."""
        with (
            patch("sys.argv", ["app.py", "--workdir", "/tmp"]),
            patch("os.getenv") as mock_getenv,
        ):
            mock_getenv.side_effect = lambda key, default="": {
                "QDRANT_URL": "http://custom:6333",
                "QDRANT_API_KEY": "test-key",
                "COLLECTION_NAME": "custom_collection",
                "EMBEDDING_MODEL": "custom/model",
                "INDEX_INCLUDE": "**/*.js,**/*.ts",
                "INDEX_EXCLUDE": "**/.build/**",
                "CHUNK_MAX_TOKENS": "400",
                "CHUNK_MIN_CHARS": "80",
                "CHUNK_OVERLAP_TOKENS": "40",
                "MAX_WORKERS": "8",
                "BATCH_SIZE": "128",
                "MAX_FILE_SIZE_MB": "10",
                "REPO_CHUNK_SIZE": "200",
                "REPO_SIZE_THRESHOLD_MB": "100",
                "MEMORY_CLEANUP_INTERVAL": "100",
            }.get(key, default)

            main()

            # Verify all environment variables were used
            mock_index_repo.assert_called_once()
            call_args = mock_index_repo.call_args
            assert call_args[1]["qdrant_url"] == "http://custom:6333"
            assert call_args[1]["api_key"] == "test-key"
            # Collection name from environment (suffix added inside index_repo)
            assert call_args[1]["collection"] == "custom_collection"
            assert call_args[1]["model_name"] == "custom/model"
            assert call_args[1]["chunk_max_tokens"] == 400
            assert call_args[1]["chunk_min_chars"] == 80
            assert call_args[1]["chunk_overlap"] == 40
            assert call_args[1]["max_workers"] == 8
            # Environment variable should be used when no command line arg provided
            assert call_args[1]["batch_size"] == 128
            assert call_args[1]["max_file_size_mb"] == 10.0
            assert call_args[1]["repo_chunk_size"] == 200
            assert call_args[1]["repo_size_threshold_mb"] == 100.0
            assert call_args[1]["memory_cleanup_interval"] == 100


class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge cases for better coverage."""

    @pytest.mark.integration
    @patch("app.TextEmbedding")
    def test_embedder_with_model_loading_error(self, mock_text_embedding):
        """Test embedder function when model loading fails."""
        from app import embedder

        mock_text_embedding.side_effect = Exception("Model loading failed")

        with pytest.raises(Exception) as exc_info:
            embedder("invalid/model")

        assert "Model loading failed" in str(exc_info.value)

    @pytest.mark.integration
    def test_guess_dim_edge_cases(self):
        """Test guess_dim with edge cases."""
        from app import guess_dim

        # Test various model name patterns
        assert guess_dim("") == 768  # Default to MPNet dimensions
        # Default to MPNet dimensions
        assert guess_dim("some-random-model") == 768
        assert guess_dim("BAAI/BGE-SMALL-EN-V1.5") == 384  # Case insensitive
        assert guess_dim("paraphrase-multilingual-mpnet-base-v2") == 768
        assert (
            guess_dim("SentenceTransformers/paraphrase-multilingual-MPNet-BASE-v2")
            == 768
        )

    @pytest.mark.integration
    def test_ensure_collection_existing_collection(self):
        """Test ensure_collection when collection already exists."""
        from app import ensure_collection

        mock_client = Mock()

        # Test when get_collection succeeds (collection exists)
        mock_collection_info = Mock()
        mock_collection_info.vectors_count = 100
        mock_client.get_collection.return_value = mock_collection_info

        # Should NOT recreate collection if it already exists
        ensure_collection(
            mock_client,
            TEST_COLLECTION_NAME,
            EXPECTED_EMBEDDING_DIMENSION,
            TEST_MODEL_NAME,
        )

        mock_client.get_collection.assert_called_once_with(TEST_COLLECTION_NAME)
        mock_client.recreate_collection.assert_not_called()

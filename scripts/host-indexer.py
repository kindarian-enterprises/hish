#!/usr/bin/env python3
"""
Host-based RAG indexing for hish framework.
Direct import-based wrapper for the indexing functionality.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Add the rag/indexer directory to Python path for imports
hish_root = Path(__file__).parent.parent
sys.path.insert(0, str(hish_root / "rag" / "indexer"))

# Import the indexing function directly
try:
    from app import index_repo
except ImportError as e:
    print(f"Error: Unable to import indexing module. Make sure you have the required dependencies installed:")
    print(f"  pip install -r {hish_root}/rag/indexer/requirements.txt")
    print(f"Import error: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("host-indexer")


def load_env_file(env_file: Path) -> dict:
    """Load environment variables from .env file."""
    env_vars = {}

    if not env_file.exists():
        logger.warning(f"Environment file not found: {env_file}")
        return env_vars

    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Handle inline comments by splitting on # and taking first part
                    value = value.split('#')[0].strip()
                    env_vars[key.strip()] = value

    return env_vars


def index_directory(work_dir: Path,
                    env_file: Path,
                    collection_name: Optional[str] = None) -> bool:
    """Index a directory using direct function calls."""

    # Load environment variables from env file
    env_vars = load_env_file(env_file)

    # Override collection name if provided
    if collection_name:
        env_vars["COLLECTION_NAME"] = collection_name

    # Override Qdrant URL for host-based access
    env_vars["QDRANT_URL"] = "http://localhost:6333"

    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value

    logger.info(
        f"Indexing {work_dir} into collection '{env_vars.get('COLLECTION_NAME', 'unknown')}'")

    try:
        # Call the indexing function directly
        index_repo(
            work_root=str(work_dir),
            qdrant_url=env_vars.get("QDRANT_URL", "http://localhost:6333"),
            api_key=env_vars.get("QDRANT_API_KEY", ""),
            collection=env_vars.get("COLLECTION_NAME", "hish_framework"),
            model_name=env_vars.get(
                "EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"),
            includes=env_vars.get("INDEX_INCLUDE", ""),
            excludes=env_vars.get("INDEX_EXCLUDE", ""),
            chunk_max_tokens=int(env_vars.get("CHUNK_MAX_TOKENS", "350")),
            chunk_min_chars=int(env_vars.get("CHUNK_MIN_CHARS", "150")),
            chunk_overlap=int(env_vars.get("CHUNK_OVERLAP_TOKENS", "70")),
            max_workers=int(env_vars.get("MAX_WORKERS", "0")),
            batch_size=int(env_vars.get("BATCH_SIZE", "256")),
            max_file_size_mb=int(env_vars.get("MAX_FILE_SIZE_MB", "5")),
            repo_chunk_size=int(env_vars.get("REPO_CHUNK_SIZE", "100")),
            repo_size_threshold_mb=float(
                env_vars.get("REPO_SIZE_THRESHOLD_MB", "50.0")),
            memory_cleanup_interval=int(
                env_vars.get("MEMORY_CLEANUP_INTERVAL", "50"))
        )
        return True
    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        return False


def main():
    """Main entry point for host-based indexing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Host-based RAG indexing for hish framework")
    parser.add_argument("--work-dir", type=Path,
                        required=True, help="Directory to index")
    parser.add_argument("--env-file", type=Path, required=True,
                        help="Environment configuration file")
    parser.add_argument("--collection", type=str,
                        help="Override collection name")

    args = parser.parse_args()

    success = index_directory(
        work_dir=args.work_dir,
        env_file=args.env_file,
        collection_name=args.collection
    )

    if success:
        logger.info("✅ Indexing completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Indexing failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

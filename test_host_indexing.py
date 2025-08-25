#!/usr/bin/env python3
"""
Test script to run the indexer directly on the host for platform-backend.
This bypasses Docker and gives us direct visibility into what's happening.
"""

import os
import sys
from pathlib import Path

# Add the rag/indexer directory to the path
sys.path.insert(0, str(Path(__file__).parent / "rag" / "indexer"))

# Set environment variables
os.environ.update({
    "QDRANT_URL": "http://localhost:6333",
    "QDRANT_API_KEY": "",
    "COLLECTION_NAME": "platform-backend_code",
    "EMBEDDING_MODEL": "BAAI/bge-small-en-v1.5",
    "CHUNK_MAX_TOKENS": "512",
    "CHUNK_MIN_CHARS": "150",
    "CHUNK_OVERLAP_TOKENS": "70",
    "INDEX_INCLUDE": "**/*.py,**/*.yaml,**/*.yml,**/*.json,**/*.md,**/*.js,**/*.ts,**/*.tf,**/*.go,**/*.rs,**/*.scala,**/*.java,**/*.c,**/*.cpp,**/*.cc,**/*.cxx,**/*.h,**/*.hpp",
    "INDEX_EXCLUDE": "**/.git/**,**/.data/**,**/node_modules/**,**/.terraform/**,**/.venv/**,**/dist/**,**/build/**,**/__pycache__/**,**/venv/**,**/.pytest_cache/**,**/mocks-api/data/**,**/mock-data/**,**/test-data/**,**/sample-data/**,**/data/**,**/datasets/**,**/logs/**,**/tmp/**,**/temp/**,**/cache/**,**/.cache/**,**/target/**,**/out/**,**/.next/**,**/.nuxt/**,**/coverage/**,**/.coverage/**,**/htmlcov/**,**/.tox/**,**/.mypy_cache/**,**/.ruff_cache/**,**/migrations/**,**/fixtures/**,**/snapshots/**,**/*.log,**/*.logs,**/*.dump,**/*.sql,**/*.db,**/*.sqlite,**/*.sqlite3,**/*.parquet,**/*.arrow,**/*.feather,**/*.h5,**/*.hdf5,**/*.pkl,**/*.pickle,**/*.joblib,**/*.npy,**/*.npz,**/*.mat,**/*.csv,**/*.tsv,**/*.xlsx,**/*.xls,**/*.ods,**/*.pdf,**/*.doc,**/*.docx,**/*.ppt,**/*.pptx,**/*.zip,**/*.tar,**/*.tar.gz,**/*.tgz,**/*.tar.bz2,**/*.rar,**/*.7z,**/*.gz,**/*.bz2,**/*.xz,**/*.img,**/*.iso,**/*.dmg,**/*.exe,**/*.msi,**/*.deb,**/*.rpm,**/*.app,**/*.bin,**/*.so,**/*.dll,**/*.dylib,**/*.a,**/*.lib,**/*.o,**/*.obj,**/*.class,**/*.jar,**/*.war,**/*.ear,**/*.aar,**/*.apk,**/*.ipa,**/*.wasm,**/*.pyc,**/*.pyo,**/*.pyd,**/*.egg,**/*.egg-info/**,**/*.whl,**/*.gem,**/*.lock,**/yarn.lock,**/package-lock.json,**/poetry.lock,**/Pipfile.lock,**/Cargo.lock,**/composer.lock,**/Gemfile.lock,**/go.sum,**/mix.lock,**/*.min.js,**/*.min.css,**/*.bundle.js,**/*.bundle.css,**/vendor/**,**/vendors/**,**/third_party/**,**/3rdparty/**,**/external/**,**/lib/**,**/libs/**,**/.idea/**,**/.vscode/**,**/.vs/**,**/.eclipse/**,**/.settings/**,**/nbproject/**,**/*.swp,**/*.swo,**/*~,**/.DS_Store,**/Thumbs.db,**/desktop.ini,**/*.tmp,**/*.temp,**/*.bak,**/*.backup,**/*.orig,**/*.rej,**/*.patch",
    "MAX_WORKERS": "0",
    "BATCH_SIZE": "32",
    "MAX_FILE_SIZE_MB": "1",
    "REPO_CHUNK_SIZE": "10",
    "REPO_SIZE_THRESHOLD_MB": "1",
    "MEMORY_CLEANUP_INTERVAL": "5"
})


def main():
    """Run the indexer directly."""
    print("🚀 Starting platform-backend indexing directly on host...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🔗 Qdrant URL: {os.environ['QDRANT_URL']}")
    print(f"📚 Collection: {os.environ['COLLECTION_NAME']}")

    # Import and run the indexer
    try:
        from app import index_repo

        # Run indexing
        index_repo(
            work_root="../platform-backend",
            qdrant_url=os.environ["QDRANT_URL"],
            api_key=os.environ["QDRANT_API_KEY"],
            collection=os.environ["COLLECTION_NAME"],
            model_name=os.environ["EMBEDDING_MODEL"],
            includes=os.environ["INDEX_INCLUDE"],
            excludes=os.environ["INDEX_EXCLUDE"],
            chunk_max_tokens=int(os.environ["CHUNK_MAX_TOKENS"]),
            chunk_min_chars=int(os.environ["CHUNK_MIN_CHARS"]),
            chunk_overlap=int(os.environ["CHUNK_OVERLAP_TOKENS"]),
            max_workers=int(os.environ["MAX_WORKERS"]),
            batch_size=int(os.environ["BATCH_SIZE"]),
            max_file_size_mb=int(os.environ["MAX_FILE_SIZE_MB"]),
            repo_chunk_size=int(os.environ["REPO_CHUNK_SIZE"]),
            repo_size_threshold_mb=float(os.environ["REPO_SIZE_THRESHOLD_MB"]),
            memory_cleanup_interval=int(os.environ["MEMORY_CLEANUP_INTERVAL"])
        )

        print("✅ Indexing completed successfully!")

    except Exception as e:
        print(f"❌ Indexing failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

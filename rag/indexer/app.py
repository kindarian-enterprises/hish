import argparse
import gc
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

import numpy as np
import torch
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    HnswConfigDiff,
    OptimizersConfigDiff,
    PayloadSchemaType,
    PointStruct,
    VectorParams,
    WalConfigDiff,
)
from rich import print
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)

from chunkers import chunk_text, prefer_md_splits
from util import compile_globs, iter_files, read_text

# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("indexer")


def get_directory_size_mb(path: str) -> float:
    """Get the total size of a directory in MB."""
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, IOError):
                    continue
        return total_size / (1024 * 1024)  # Convert to MB
    except Exception as e:
        logger.warning(f"Could not calculate directory size for {path}: {e}")
        return 0.0


def should_use_chunking(work_root: str, repo_size_threshold_mb: float) -> bool:
    """Determine if repository chunking should be used based on size."""
    repo_size_mb = get_directory_size_mb(work_root)
    logger.info(f"Repository size: {repo_size_mb:.1f} MB")

    if repo_size_mb > repo_size_threshold_mb:
        logger.info(
            f"Repository size ({repo_size_mb:.1f} MB) exceeds threshold ({repo_size_threshold_mb} MB) - enabling chunking strategy"
        )
        return True
    else:
        logger.info(
            f"Repository size ({repo_size_mb:.1f} MB) is below threshold ({repo_size_threshold_mb} MB) - using standard processing"
        )
        return False


def process_files_in_chunks(
    files_to_process: List[str],
    work_root: str,
    model: TextEmbedding,
    chunk_max_tokens: int,
    chunk_min_chars: int,
    chunk_overlap: int,
    optimal_model: str,
    max_file_size_mb: float,
    collection: str,
    client: QdrantClient,
    batch_size: int,
    repo_chunk_size: int,
    memory_cleanup_interval: int,
    max_workers: int,
) -> Tuple[int, int]:
    """Process files in chunks with memory cleanup between chunks."""
    total_files = 0
    total_chunks = 0
    next_id = 1

    # Initialize detailed progress log file (use /tmp since work_root is read-only)
    log_file_path = "/tmp/indexing_progress.log"
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"=== INDEXING STARTED: {collection} ===\n")
        log_file.write(f"Total files to process: {len(files_to_process)}\n")
        log_file.write(f"Repository chunk size: {repo_chunk_size}\n")
        log_file.write(f"Max file size: {max_file_size_mb}MB\n")
        log_file.write("=" * 50 + "\n")
        log_file.flush()

    logger.info(f"Detailed progress will be logged to: {log_file_path}")

    # Split files into chunks
    file_chunks = [
        files_to_process[i : i + repo_chunk_size]
        for i in range(0, len(files_to_process), repo_chunk_size)
    ]

    logger.info(
        f"Processing {len(files_to_process)} files in {len(file_chunks)} chunks of {repo_chunk_size} files each"
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        main_task = progress.add_task(
            "Processing file chunks...", total=len(file_chunks)
        )

        for chunk_idx, file_chunk in enumerate(file_chunks):
            logger.info(
                f"Processing chunk {chunk_idx + 1}/{len(file_chunks)} ({len(file_chunk)} files)"
            )

            # Process this chunk of files
            batch = []
            chunk_task = progress.add_task(
                f"Chunk {chunk_idx + 1}", total=len(file_chunk)
            )

            # Reduce worker count for chunked processing to save memory
            chunk_workers = min(max_workers, 4)

            with ThreadPoolExecutor(max_workers=chunk_workers) as executor:
                future_to_file = {
                    executor.submit(
                        process_single_file,
                        rel,
                        work_root,
                        model,
                        chunk_max_tokens,
                        chunk_min_chars,
                        chunk_overlap,
                        optimal_model,
                        int(max_file_size_mb),
                        collection,
                    ): rel
                    for rel in file_chunk
                }

                for future in as_completed(future_to_file):
                    rel = future_to_file[future]

                    # Log the file being processed to a detailed log file
                    log_file_path = "/tmp/indexing_progress.log"
                    with open(log_file_path, "a", encoding="utf-8") as log_file:
                        log_file.write(f"PROCESSING: {rel}\n")
                        log_file.flush()

                    try:
                        file_path, points, chunk_count = future.result()

                        # Log successful completion
                        log_file_path = "/tmp/indexing_progress.log"
                        with open(log_file_path, "a", encoding="utf-8") as log_file:
                            log_file.write(
                                f"COMPLETED: {rel} -> {chunk_count} chunks\n"
                            )
                            log_file.flush()

                        if chunk_count > 0:
                            # Assign IDs to points
                            for point in points:
                                point.id = next_id
                                next_id += 1
                                total_chunks += 1

                            # Add to batch
                            batch.extend(points)

                            # Upsert in batches
                            if len(batch) >= batch_size:
                                logger.debug(
                                    f"Upserting batch of {len(batch)} vectors..."
                                )
                                try:
                                    client.upsert(
                                        collection_name=collection, points=batch
                                    )
                                    logger.debug("Batch upserted successfully")
                                except Exception as e:
                                    logger.error(f"Failed to upsert batch: {e}")
                                batch.clear()

                        total_files += 1
                        progress.advance(chunk_task)

                        # Periodic memory cleanup
                        if total_files % memory_cleanup_interval == 0:
                            gc.collect()
                            logger.debug(f"Memory cleanup after {total_files} files")

                    except Exception as e:
                        logger.error(f"Failed to process {rel}: {e}")

                        # Log the error to the detailed log file
                        log_file_path = "/tmp/indexing_progress.log"
                        with open(log_file_path, "a", encoding="utf-8") as log_file:
                            log_file.write(f"ERROR: {rel} -> {str(e)}\n")
                            log_file.flush()

                        progress.advance(chunk_task)
                        continue

            # Upsert remaining batch for this chunk
            if batch:
                logger.info(
                    f"Upserting final batch of {len(batch)} vectors for chunk {chunk_idx + 1}..."
                )
                try:
                    client.upsert(collection_name=collection, points=batch)
                    logger.info("Chunk batch upserted successfully")
                except Exception as e:
                    logger.error(f"Failed to upsert chunk batch: {e}")
                batch.clear()

            # Force garbage collection between chunks
            gc.collect()
            logger.info(
                f"Completed chunk {chunk_idx + 1}/{len(file_chunks)}, memory cleaned up"
            )
            progress.advance(main_task)
            progress.remove_task(chunk_task)

    return total_files, total_chunks


def normalize_vectors(vectors: List[List[float]]) -> List[List[float]]:
    """
    Normalize vectors to unit length for DOT distance.
    DOT distance with normalized vectors is equivalent to COSINE but ~30% faster.
    """
    arr = np.array(vectors)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    # Avoid division by zero
    norms = np.where(norms == 0, 1, norms)
    normalized = arr / norms
    return normalized.tolist()


def create_payload_indexes(client: QdrantClient, collection_name: str):
    """Create payload indexes for efficient pre-filtering."""
    logger.info(f"Creating payload indexes for collection '{collection_name}'...")

    try:
        # Index on repo field
        client.create_payload_index(
            collection_name=collection_name,
            field_name="repo",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        logger.info("Created index on 'repo' field")

        # Index on language field
        client.create_payload_index(
            collection_name=collection_name,
            field_name="language",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        logger.info("Created index on 'language' field")

        # Index on path_prefix field
        client.create_payload_index(
            collection_name=collection_name,
            field_name="path_prefix",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        logger.info("Created index on 'path_prefix' field")

    except Exception as e:
        logger.warning(f"Failed to create some payload indexes: {e}")


def ensure_collection(client: QdrantClient, name: str, dim: int, model_name: str):
    logger.info(f"Checking collection '{name}'...")

    # Use named vector for MCP compatibility
    logger.info(f"Using named vector '{model_name}' for MCP compatibility")

    try:
        collection_info = client.get_collection(name)
        logger.info(
            f"Collection '{name}' already exists with {collection_info.vectors_count} vectors"
        )
        # Try to create payload indexes if they don't exist
        try:
            create_payload_indexes(client, name)
        except Exception:
            pass  # Indexes may already exist
    except Exception:
        logger.info(
            f"Collection '{name}' not found, creating new collection with dimension {dim}"
        )
        # Create collection with optimized configuration
        # Using DOT distance (requires normalized vectors, ~30% faster than COSINE)
        # HNSW optimized for 768-dim MPNet embeddings
        vectors_config = {
            model_name: VectorParams(
                size=dim,
                distance=Distance.DOT,  # Changed from COSINE - requires normalized vectors
                hnsw_config=HnswConfigDiff(
                    m=40,  # Graph connectivity optimized for 768-dim
                    ef_construct=384,  # Build-time search effort
                    full_scan_threshold=10000,  # Use HNSW above this point count
                ),
                on_disk=True,  # Enable mmap for memory efficiency
            )
        }

        # Collection-level optimizations
        client.recreate_collection(
            collection_name=name,
            vectors_config=vectors_config,
            optimizers_config=OptimizersConfigDiff(
                indexing_threshold=10000,  # Start HNSW indexing after 10k points
            ),
            wal_config=WalConfigDiff(
                wal_capacity_mb=64,  # Write-ahead log size
            ),
        )

        logger.info(
            f"Collection '{name}' created with optimized config (DOT distance, HNSW m=40, ef_construct=384, on-disk storage)"
        )

        # Create payload indexes for pre-filtering
        create_payload_indexes(client, name)


def embedder(model_name: str):
    logger.info(f"Loading embedding model: {model_name}")

    # Check GPU availability and configure FastEmbed
    if torch.cuda.is_available():
        logger.info(
            f"🚀 GPU detected: {torch.cuda.get_device_name(0)} - Enabling CUDA acceleration"
        )
        model = TextEmbedding(model_name=model_name, cuda=True, lazy_load=False)
        logger.info(f"Embedding model '{model_name}' loaded successfully on GPU")
    else:
        logger.info("Using CPU (no GPU detected)")
        model = TextEmbedding(model_name=model_name)
        logger.info(f"Embedding model '{model_name}' loaded successfully on CPU")

    return model


def is_code_collection(collection_name: str) -> bool:
    """Determine if a collection should use code-specific embeddings."""
    framework_collections = {
        "hish_framework",
        "cross_project_intelligence",
        "framework_docs",
    }

    # Framework collections use BGE-small
    if collection_name in framework_collections:
        return False

    # Collections ending with _code are code repositories
    if collection_name.endswith("_code"):
        return True

    # Default to framework (BGE) for unknown collections
    return False


def get_model_suffix(model_name: str) -> str:
    """Get a short suffix for collection names based on model."""
    if "paraphrase-multilingual-mpnet-base-v2" in model_name.lower():
        return "mpnet"
    elif "bge-small" in model_name.lower():
        return "bge"
    else:
        return "unknown"


def get_optimal_model(collection_name: str, override_model: str | None = None) -> str:
    """Get the optimal embedding model for a collection type."""
    if override_model:
        return override_model

    # Use unified mpnet model for all collections (both code and framework)
    return "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


def ensure_model_suffix(collection_name: str, model_name: str) -> str:
    """Ensure collection name has the appropriate model suffix."""
    suffix = get_model_suffix(model_name)

    # Remove existing model suffixes if present, but preserve collection type indicators
    base_name = collection_name
    for old_suffix in ["_mpnet", "_bge"]:
        if base_name.endswith(old_suffix):
            base_name = base_name[: -len(old_suffix)]

    # Add the new model suffix
    if not base_name.endswith(f"_{suffix}"):
        return f"{base_name}_{suffix}"
    return base_name


def guess_dim(model_name: str) -> int:
    # BGE models: small=384, base=768, large=1024
    # MiniLM uses 384
    # MPNet models use 768
    if "bge-small" in model_name.lower():
        return 384
    elif "bge-base" in model_name.lower():
        return 768
    elif "bge-large" in model_name.lower():
        return 1024
    elif "bge" in model_name.lower():
        return 384  # Default BGE to small dimensions
    elif "minilm" in model_name.lower():
        return 384
    elif "paraphrase-multilingual-mpnet-base-v2" in model_name.lower():
        return 768
    else:
        # Default to 768 for unknown models (MPNet is now standard)
        return 768


def process_single_file(
    rel: str,
    work_root: str,
    model: TextEmbedding,
    chunk_max_tokens: int,
    chunk_min_chars: int,
    chunk_overlap: int,
    model_name: str,
    max_file_size_mb: int,
    collection: str,
) -> Tuple[str, List[PointStruct], int]:
    """
    Process a single file and return chunks with embeddings.
    Returns: (file_path, list_of_points, chunk_count)
    """
    path = os.path.join(work_root, rel)
    logger.debug(f"Processing file: {rel}")

    # Check file size - skip extremely large files
    try:
        file_size = os.path.getsize(path)
        if file_size > max_file_size_mb * 1024 * 1024:
            logger.warning(
                f"Skipping large file {rel} ({file_size / 1024 / 1024:.1f}MB) - exceeds {max_file_size_mb}MB limit"
            )
            return rel, [], 0
    except Exception as e:
        logger.warning(f"Could not check file size for {rel}: {e}")

    try:
        text = read_text(path)
    except Exception as e:
        logger.warning(f"Failed to read {rel}: {e}")
        return rel, [], 0

    # Prefer markdown-aware splitting, then chunk by tokens
    rough = (
        prefer_md_splits(text)
        if rel.lower().endswith((".md", ".mdx", ".txt"))
        else [text]
    )
    pieces: List[str] = []
    for r in rough:
        pieces.extend(chunk_text(r, max_tokens=chunk_max_tokens, overlap=chunk_overlap))

    # guard short chunks
    pieces = [p for p in pieces if len(p) >= chunk_min_chars]
    if not pieces:
        logger.debug(f"No chunks generated for {rel} (all too short)")
        return rel, [], 0

    logger.debug(f"Generated {len(pieces)} chunks for {rel}")

    # Compute embeddings (FastEmbed returns generator)
    try:
        embeddings = list(model.embed(pieces))
    except Exception as e:
        logger.error(f"Failed to generate embeddings for {rel}: {e}")
        return rel, [], 0

    # Normalize embeddings for DOT distance (equivalent to COSINE but faster)
    try:
        embeddings = normalize_vectors(embeddings)
    except Exception as e:
        logger.error(f"Failed to normalize embeddings for {rel}: {e}")
        return rel, [], 0

    # Extract language from file extension
    file_ext = os.path.splitext(rel)[1].lower().lstrip(".") or "no-ext"
    language_map = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "tsx": "typescript",
        "jsx": "javascript",
        "java": "java",
        "go": "go",
        "rs": "rust",
        "scala": "scala",
        "rb": "ruby",
        "php": "php",
        "c": "c",
        "cpp": "cpp",
        "cc": "cpp",
        "cxx": "cpp",
        "h": "c",
        "hpp": "cpp",
        "cs": "csharp",
        "sh": "shell",
        "bash": "shell",
        "sql": "sql",
        "yaml": "yaml",
        "yml": "yaml",
        "json": "json",
        "toml": "toml",
        "md": "markdown",
        "txt": "text",
    }
    language = language_map.get(file_ext, file_ext)

    # Extract path prefix (first 2-3 components for filtering)
    path_parts = rel.split("/")
    if len(path_parts) > 2:
        path_prefix = "/".join(path_parts[:2])
    elif len(path_parts) > 1:
        path_prefix = path_parts[0]
    else:
        path_prefix = ""

    # Create points for this file
    points = []
    for chunk, vec in zip(pieces, embeddings):
        file_title = os.path.basename(rel)

        # Create context header for better semantic search
        context_header = f"[repo: {collection}] [file: {rel}] [ext: {file_ext}] [title: {file_title}]\n---\n"
        enhanced_chunk = context_header + chunk

        # Enhanced payload with dual-write for compatibility and optimization metadata
        payload = {
            "path": rel,
            "repo": collection,
            "ext": file_ext,
            "title": file_title,
            "language": language,  # New: for pre-filtering
            "path_prefix": path_prefix,  # New: for pre-filtering
            "content": enhanced_chunk,  # LlamaIndex expects 'content' field
            "document": enhanced_chunk,  # Alternative field for other MCPs
            "raw_content": chunk,  # Original chunk without context header
        }

        # Use named vector field for MCP compatibility
        # Vectors are now normalized for DOT distance
        points.append(
            PointStruct(
                id=0,  # Will be set by caller
                vector={
                    model_name: list(vec)
                },  # Named vector field with normalized vector
                payload=payload,
            )
        )

    return rel, points, len(pieces)


def index_repo(
    work_root: str,
    qdrant_url: str,
    api_key: str,
    collection: str,
    model_name: str,
    includes: str,
    excludes: str,
    chunk_max_tokens: int,
    chunk_min_chars: int,
    chunk_overlap: int,
    max_workers: int = 0,
    batch_size: int = 256,
    max_file_size_mb: int = 5,
    repo_chunk_size: int = 100,
    repo_size_threshold_mb: float = 50.0,
    memory_cleanup_interval: int = 50,
):
    # Determine optimal model for this collection type
    optimal_model = get_optimal_model(collection, model_name)

    # Ensure collection name includes model suffix
    collection = ensure_model_suffix(collection, optimal_model)

    logger.info(f"Starting repository indexing from: {work_root}")
    logger.info(f"Target Qdrant: {qdrant_url}")
    logger.info(f"Collection: {collection}")
    logger.info(
        f"Collection type: {'Code Repository' if is_code_collection(collection) else 'Framework Documentation'}"
    )
    logger.info(f"Optimal model: {optimal_model}")
    logger.info(f"Include patterns: {includes}")
    logger.info(f"Exclude patterns: {excludes}")
    logger.info(f"Performance settings: {max_workers} workers, {batch_size} batch size")

    # Use named vector for MCP compatibility

    logger.info("Connecting to Qdrant...")
    client = QdrantClient(url=qdrant_url, api_key=api_key or None)
    logger.info("Qdrant connection established")

    dim = guess_dim(optimal_model)
    ensure_collection(client, collection, dim, optimal_model)

    model = embedder(optimal_model)

    logger.info("Compiling file patterns...")
    inc_spec, exc_spec = compile_globs(includes, excludes)

    logger.info("Scanning files...")
    files_to_process = list(iter_files(work_root, inc_spec, exc_spec))
    logger.info(f"Found {len(files_to_process)} files to process")

    # Debug: List all files found
    logger.info("Files to process:")
    for i, f in enumerate(files_to_process[:20]):  # Show first 20 files
        logger.info(f"  {i+1:2d}. {f}")
    if len(files_to_process) > 20:
        logger.info(f"  ... and {len(files_to_process) - 20} more files")

    if not files_to_process:
        logger.warning("No files found matching the patterns!")
        return

    # Determine optimal thread count based on file count and user preference
    if max_workers > 0:
        logger.info(f"Using user-specified {max_workers} worker threads")
    else:
        max_workers = min(8, max(2, len(files_to_process) // 10))  # 2-8 workers
        logger.info(
            f"Auto-detected {max_workers} worker threads for {len(files_to_process)} files"
        )

    # Determine if we should use chunking strategy based on repository size
    use_chunking = should_use_chunking(work_root, repo_size_threshold_mb)

    if use_chunking:
        # Use chunking strategy for large repositories
        total_files, total_chunks = process_files_in_chunks(
            files_to_process,
            work_root,
            model,
            chunk_max_tokens,
            chunk_min_chars,
            chunk_overlap,
            optimal_model,
            max_file_size_mb,
            collection,
            client,
            batch_size,
            repo_chunk_size,
            memory_cleanup_interval,
            max_workers,
        )
    else:
        # Use standard processing for smaller repositories
        total_files = 0
        total_chunks = 0
        standard_batch: List[PointStruct] = []
        next_id = 1

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("Processing files...", total=len(files_to_process))

            # Process files in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all files for processing
                future_to_file = {
                    executor.submit(
                        process_single_file,
                        rel,
                        work_root,
                        model,
                        chunk_max_tokens,
                        chunk_min_chars,
                        chunk_overlap,
                        optimal_model,
                        max_file_size_mb,
                        collection,
                    ): rel
                    for rel in files_to_process
                }

                # Process completed futures as they finish
                for future in as_completed(future_to_file):
                    rel = future_to_file[future]
                    try:
                        file_path, points, chunk_count = future.result()

                        if chunk_count > 0:
                            # Assign IDs to points
                            for point in points:
                                point.id = next_id
                                next_id += 1
                                total_chunks += 1

                            # Add to batch
                            standard_batch.extend(points)

                            # Upsert in reasonable batches
                            if len(standard_batch) >= batch_size:
                                logger.debug(
                                    f"Upserting batch of {len(standard_batch)} vectors..."
                                )
                                try:
                                    client.upsert(
                                        collection_name=collection,
                                        points=standard_batch,
                                    )
                                    logger.debug("Batch upserted successfully")
                                except Exception as e:
                                    logger.error(f"Failed to upsert batch: {e}")
                                standard_batch.clear()

                        total_files += 1
                        progress.advance(task)

                        # Periodic memory cleanup for standard processing too
                        if total_files % memory_cleanup_interval == 0:
                            gc.collect()

                    except Exception as e:
                        logger.error(f"Failed to process {rel}: {e}")
                        progress.advance(task)
                        continue

        # Final batch
        if standard_batch:
            logger.info(f"Upserting final batch of {len(standard_batch)} vectors...")
            try:
                client.upsert(collection_name=collection, points=standard_batch)
                logger.info("Final batch upserted successfully")
            except Exception as e:
                logger.error(f"Failed to upsert final batch: {e}")

    logger.info("Indexing complete!")
    print(
        f"[green]✓ Indexed[/green] files={total_files} chunks={total_chunks} into collection='{collection}'"
    )


def main():
    ap = argparse.ArgumentParser(
        description="Index repositories into Qdrant for Hish framework"
    )
    ap.add_argument("--workdir", default="/work", help="Mounted repo root")
    ap.add_argument(
        "--recreate", action="store_true", help="Drop & recreate collection first"
    )
    ap.add_argument("--debug", action="store_true", help="Enable debug logging")
    ap.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of worker threads (0=auto, default: from env or auto)",
    )
    ap.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="Batch size for Qdrant upserts (default: from env or 256)",
    )

    args = ap.parse_args()

    # Adjust logging level if debug is enabled
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    logger.info("=== Hish Framework Indexer ===")
    logger.info(f"Working directory: {args.workdir}")

    qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
    api_key = os.getenv("QDRANT_API_KEY", "")
    collection = os.getenv("COLLECTION_NAME", "hish_framework")
    model_name = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )

    inc = os.getenv("INDEX_INCLUDE", "")
    exc = os.getenv("INDEX_EXCLUDE", "")
    chunk_max = int(os.getenv("CHUNK_MAX_TOKENS", "300"))
    chunk_min = int(os.getenv("CHUNK_MIN_CHARS", "200"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP_TOKENS", "40"))
    max_workers = int(os.getenv("MAX_WORKERS", "0"))
    batch_size = int(os.getenv("BATCH_SIZE", "256"))
    max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "5"))

    # Repository chunking parameters
    repo_chunk_size = int(os.getenv("REPO_CHUNK_SIZE", "100"))
    repo_size_threshold_mb = float(os.getenv("REPO_SIZE_THRESHOLD_MB", "50.0"))
    memory_cleanup_interval = int(os.getenv("MEMORY_CLEANUP_INTERVAL", "50"))

    if args.recreate:
        logger.info("Recreate flag detected - will drop and recreate collection")
        # For safety, require explicit flag to recreate
        logger.info("Connecting to Qdrant for collection recreation...")
        client = QdrantClient(url=qdrant_url, api_key=api_key or None)

        # Determine optimal model for this collection type
        optimal_model = get_optimal_model(collection, model_name)
        dim = guess_dim(optimal_model)
        logger.info(
            f"Collection type: {'Code Repository' if is_code_collection(collection) else 'Framework Documentation'}"
        )
        logger.info(f"Using optimal model: {optimal_model}")
        logger.info(
            f"Recreating collection '{collection}' with dimension {dim} using named vector '{optimal_model}'"
        )
        vectors_config = {
            optimal_model: VectorParams(size=dim, distance=Distance.COSINE)
        }
        client.recreate_collection(collection, vectors_config=vectors_config)
        logger.info(f"Collection '{collection}' recreated successfully")

    try:
        index_repo(
            work_root=args.workdir,
            qdrant_url=qdrant_url,
            api_key=api_key,
            collection=collection,
            model_name=model_name,
            includes=inc,
            excludes=exc,
            chunk_max_tokens=chunk_max,
            chunk_min_chars=chunk_min,
            chunk_overlap=chunk_overlap,
            max_workers=args.workers if args.workers is not None else max_workers,
            batch_size=args.batch_size if args.batch_size is not None else batch_size,
            max_file_size_mb=max_file_size_mb,
            repo_chunk_size=repo_chunk_size,
            repo_size_threshold_mb=repo_size_threshold_mb,
            memory_cleanup_interval=memory_cleanup_interval,
        )
        logger.info("=== Indexing completed successfully! ===")
    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        if args.debug:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()

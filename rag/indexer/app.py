import os
import sys
import argparse
import json
import logging
from typing import Dict, Any, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding
from rich import print
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from chunkers import chunk_text, prefer_md_splits
from util import compile_globs, iter_files, read_text

# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("indexer")


def ensure_collection(client: QdrantClient, name: str, dim: int, model_name: str):
    logger.info(f"Checking collection '{name}'...")

    # Use named vector for MCP compatibility
    logger.info(f"Using named vector '{model_name}' for MCP compatibility")

    try:
        collection_info = client.get_collection(name)
        logger.info(
            f"Collection '{name}' already exists with {collection_info.vectors_count} vectors")
    except Exception:
        logger.info(
            f"Collection '{name}' not found, creating new collection with dimension {dim}")
        # Create collection with named vector for MCP compatibility
        vectors_config = {model_name: VectorParams(
            size=dim, distance=Distance.COSINE)}
        client.recreate_collection(
            collection_name=name,
            vectors_config=vectors_config
        )
        logger.info(
            f"Collection '{name}' created successfully with named vector '{model_name}'")


def embedder(model_name: str):
    logger.info(f"Loading embedding model: {model_name}")
    # FastEmbed API
    model = TextEmbedding(model_name=model_name)
    logger.info(f"Embedding model '{model_name}' loaded successfully")
    return model


def guess_dim(model_name: str) -> int:
    # BGE models: small=384, base=768, large=1024
    # MiniLM uses 384
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
    else:
        # Default to 384 for other models
        return 384


def process_single_file(rel: str, work_root: str, model: TextEmbedding,
                        chunk_max_tokens: int, chunk_min_chars: int,
                        chunk_overlap: int, model_name: str, max_file_size_mb: int, collection: str) -> Tuple[str, List[PointStruct], int]:
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
                f"Skipping large file {rel} ({file_size / 1024 / 1024:.1f}MB) - exceeds {max_file_size_mb}MB limit")
            return rel, [], 0
    except Exception as e:
        logger.warning(f"Could not check file size for {rel}: {e}")

    try:
        text = read_text(path)
    except Exception as e:
        logger.warning(f"Failed to read {rel}: {e}")
        return rel, [], 0

    # Prefer markdown-aware splitting, then chunk by tokens
    rough = prefer_md_splits(text) if rel.lower().endswith(
        (".md", ".mdx", ".txt")) else [text]
    pieces: List[str] = []
    for r in rough:
        pieces.extend(chunk_text(
            r, max_tokens=chunk_max_tokens, overlap=chunk_overlap))

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

    # Create points for this file
    points = []
    for chunk, vec in zip(pieces, embeddings):
        # Extract file extension and title
        file_ext = os.path.splitext(rel)[1].lower().lstrip('.') or 'no-ext'
        file_title = os.path.basename(rel)

        # Create context header for better semantic search
        context_header = f"[repo: {collection}] [file: {rel}] [ext: {file_ext}] [title: {file_title}]\n---\n"
        enhanced_chunk = context_header + chunk

        # Enhanced payload with dual-write for compatibility
        payload = {
            "path": rel,
            "repo": collection,
            "ext": file_ext,
            "title": file_title,
            "content": enhanced_chunk,  # LlamaIndex expects 'content' field
            "document": enhanced_chunk,  # Alternative field for other MCPs
            "raw_content": chunk  # Original chunk without context header
        }

        # Use named vector field for MCP compatibility
        points.append(PointStruct(
            id=0,  # Will be set by caller
            vector={model_name: list(vec)},  # Named vector field
            payload=payload))

    return rel, points, len(pieces)


def index_repo(work_root: str, qdrant_url: str, api_key: str, collection: str,
               model_name: str, includes: str, excludes: str,
               chunk_max_tokens: int, chunk_min_chars: int, chunk_overlap: int,
               max_workers: int = 0, batch_size: int = 256, max_file_size_mb: int = 5):

    logger.info(f"Starting repository indexing from: {work_root}")
    logger.info(f"Target Qdrant: {qdrant_url}")
    logger.info(f"Collection: {collection}")
    logger.info(f"Include patterns: {includes}")
    logger.info(f"Exclude patterns: {excludes}")
    logger.info(
        f"Performance settings: {max_workers} workers, {batch_size} batch size")

    # Use named vector for MCP compatibility

    logger.info("Connecting to Qdrant...")
    client = QdrantClient(url=qdrant_url, api_key=api_key or None)
    logger.info("Qdrant connection established")

    dim = guess_dim(model_name)
    ensure_collection(client, collection, dim, model_name)

    model = embedder(model_name)

    logger.info("Compiling file patterns...")
    inc_spec, exc_spec = compile_globs(includes, excludes)

    total_files = 0
    total_chunks = 0
    batch: List[PointStruct] = []
    next_id = 1

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
        max_workers = min(
            8, max(2, len(files_to_process) // 10))  # 2-8 workers
        logger.info(
            f"Auto-detected {max_workers} worker threads for {len(files_to_process)} files")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:

        task = progress.add_task(
            "Processing files...", total=len(files_to_process))

        # Process files in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(
                    process_single_file,
                    rel, work_root, model,
                    chunk_max_tokens, chunk_min_chars, chunk_overlap, model_name, max_file_size_mb, collection
                ): rel for rel in files_to_process
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
                        batch.extend(points)

                        # Upsert in reasonable batches
                        if len(batch) >= batch_size:
                            logger.debug(
                                f"Upserting batch of {len(batch)} vectors...")
                            try:
                                client.upsert(
                                    collection_name=collection, points=batch)
                                logger.debug("Batch upserted successfully")
                            except Exception as e:
                                logger.error(f"Failed to upsert batch: {e}")
                            batch.clear()

                    total_files += 1
                    progress.advance(task)

                except Exception as e:
                    logger.error(f"Failed to process {rel}: {e}")
                    progress.advance(task)
                    continue

    # Final batch
    if batch:
        logger.info(f"Upserting final batch of {len(batch)} vectors...")
        try:
            client.upsert(collection_name=collection, points=batch)
            logger.info("Final batch upserted successfully")
        except Exception as e:
            logger.error(f"Failed to upsert final batch: {e}")

    logger.info(f"Indexing complete!")
    print(
        f"[green]✓ Indexed[/green] files={total_files} chunks={total_chunks} into collection='{collection}'")


def main():
    ap = argparse.ArgumentParser(
        description="Index repositories into Qdrant for Hish framework")
    ap.add_argument("--workdir", default="/work", help="Mounted repo root")
    ap.add_argument("--recreate", action="store_true",
                    help="Drop & recreate collection first")
    ap.add_argument("--debug", action="store_true",
                    help="Enable debug logging")
    ap.add_argument("--workers", type=int, default=0,
                    help="Number of worker threads (0=auto, default: auto)")
    ap.add_argument("--batch-size", type=int, default=256,
                    help="Batch size for Qdrant upserts (default: 256)")

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
        "EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

    inc = os.getenv("INDEX_INCLUDE", "")
    exc = os.getenv("INDEX_EXCLUDE", "")
    chunk_max = int(os.getenv("CHUNK_MAX_TOKENS", "300"))
    chunk_min = int(os.getenv("CHUNK_MIN_CHARS", "200"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP_TOKENS", "40"))
    max_workers = int(os.getenv("MAX_WORKERS", "0"))
    batch_size = int(os.getenv("BATCH_SIZE", "256"))
    max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "5"))

    if args.recreate:
        logger.info(
            "Recreate flag detected - will drop and recreate collection")
        # For safety, require explicit flag to recreate
        logger.info("Connecting to Qdrant for collection recreation...")
        client = QdrantClient(url=qdrant_url, api_key=api_key or None)
        dim = guess_dim(model_name)
        logger.info(
            f"Recreating collection '{collection}' with dimension {dim} using named vector '{model_name}'")
        vectors_config = {model_name: VectorParams(
            size=dim, distance=Distance.COSINE)}
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
            max_workers=args.workers or max_workers,
            batch_size=args.batch_size or batch_size,
            max_file_size_mb=max_file_size_mb
        )
        logger.info("=== Indexing completed successfully! ===")
    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        if args.debug:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()

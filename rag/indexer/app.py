import os, sys, argparse, json, logging
from typing import Dict, Any, List
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
    
    # Convert model name to vector name (matching MCP server convention)
    # sentence-transformers/all-MiniLM-L6-v2 -> fast-all-minilm-l6-v2
    vector_name = model_name.replace("sentence-transformers/", "fast-").replace("all-MiniLM-L6-v2", "all-minilm-l6-v2").lower()
    logger.info(f"Using vector name: '{vector_name}'")
    
    try:
        collection_info = client.get_collection(name)
        logger.info(f"Collection '{name}' already exists with {collection_info.vectors_count} vectors")
    except Exception:
        logger.info(f"Collection '{name}' not found, creating new collection with dimension {dim}")
        # Create collection with named vector configuration
        vectors_config = {vector_name: VectorParams(size=dim, distance=Distance.COSINE)}
        client.recreate_collection(
            collection_name=name,
            vectors_config=vectors_config
        )
        logger.info(f"Collection '{name}' created successfully with vector '{vector_name}'")

def embedder(model_name: str):
    logger.info(f"Loading embedding model: {model_name}")
    # fastembed API
    model = TextEmbedding(model_name=model_name)
    logger.info(f"Embedding model '{model_name}' loaded successfully")
    return model

def guess_dim(model_name: str) -> int:
    # common dims; adjust if you use custom models
    return 384

def index_repo(work_root: str, qdrant_url: str, api_key: str, collection: str,
               model_name: str, includes: str, excludes: str,
               chunk_max_tokens: int, chunk_min_chars: int, chunk_overlap: int):

    logger.info(f"Starting repository indexing from: {work_root}")
    logger.info(f"Target Qdrant: {qdrant_url}")
    logger.info(f"Collection: {collection}")
    logger.info(f"Include patterns: {includes}")
    logger.info(f"Exclude patterns: {excludes}")
    
    # Convert model name to vector name (matching MCP server convention)
    vector_name = model_name.replace("sentence-transformers/", "fast-").replace("all-MiniLM-L6-v2", "all-minilm-l6-v2").lower()
    
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

    if not files_to_process:
        logger.warning("No files found matching the patterns!")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        task = progress.add_task("Processing files...", total=len(files_to_process))
        
        for rel in files_to_process:
            path = os.path.join(work_root, rel)
            logger.debug(f"Processing file: {rel}")
            
            try:
                text = read_text(path)
            except Exception as e:
                logger.warning(f"Failed to read {rel}: {e}")
                progress.advance(task)
                continue

            # Prefer markdown-aware splitting, then chunk by tokens
            rough = prefer_md_splits(text) if rel.lower().endswith((".md", ".mdx", ".txt")) else [text]
            pieces: List[str] = []
            for r in rough:
                pieces.extend(chunk_text(r, max_tokens=chunk_max_tokens, overlap=chunk_overlap))

            # guard short chunks
            pieces = [p for p in pieces if len(p) >= chunk_min_chars]
            if not pieces:
                logger.debug(f"No chunks generated for {rel} (all too short)")
                progress.advance(task)
                continue

            logger.debug(f"Generated {len(pieces)} chunks for {rel}")

            # Compute embeddings (fastembed returns an iterator)
            try:
                embeddings = list(model.embed(pieces))
            except Exception as e:
                logger.error(f"Failed to generate embeddings for {rel}: {e}")
                progress.advance(task)
                continue
                
            for chunk, vec in zip(pieces, embeddings):
                payload = {
                    "path": rel,
                    "repo": "kindarian-framework", 
                    "document": chunk  # MCP server expects 'document' field
                }
                # Use named vector for MCP server compatibility
                vectors = {vector_name: list(vec)}
                batch.append(PointStruct(id=next_id, vector=vectors, payload=payload))
                next_id += 1
                total_chunks += 1

            # Upsert in reasonable batches
            if len(batch) >= 256:
                logger.debug(f"Upserting batch of {len(batch)} vectors...")
                try:
                    client.upsert(collection_name=collection, points=batch)
                    logger.debug("Batch upserted successfully")
                except Exception as e:
                    logger.error(f"Failed to upsert batch: {e}")
                batch.clear()

            total_files += 1
            progress.advance(task)

    # Final batch
    if batch:
        logger.info(f"Upserting final batch of {len(batch)} vectors...")
        try:
            client.upsert(collection_name=collection, points=batch)
            logger.info("Final batch upserted successfully")
        except Exception as e:
            logger.error(f"Failed to upsert final batch: {e}")

    logger.info(f"Indexing complete!")
    print(f"[green]✓ Indexed[/green] files={total_files} chunks={total_chunks} into collection='{collection}'")

def main():
    ap = argparse.ArgumentParser(description="Index repositories into Qdrant for Kindarian framework")
    ap.add_argument("--workdir", default="/work", help="Mounted repo root")
    ap.add_argument("--recreate", action="store_true", help="Drop & recreate collection first")
    ap.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = ap.parse_args()

    # Adjust logging level if debug is enabled
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    logger.info("=== Kindarian Framework Indexer ===")
    logger.info(f"Working directory: {args.workdir}")

    qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
    api_key = os.getenv("QDRANT_API_KEY", "")
    collection = os.getenv("COLLECTION_NAME", "kindarian_framework")
    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    inc = os.getenv("INDEX_INCLUDE", "")
    exc = os.getenv("INDEX_EXCLUDE", "")
    chunk_max = int(os.getenv("CHUNK_MAX_TOKENS", "300"))
    chunk_min = int(os.getenv("CHUNK_MIN_CHARS", "200"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP_TOKENS", "40"))

    if args.recreate:
        logger.info("Recreate flag detected - will drop and recreate collection")
        # For safety, require explicit flag to recreate
        logger.info("Connecting to Qdrant for collection recreation...")
        client = QdrantClient(url=qdrant_url, api_key=api_key or None)
        dim = 384
        # Convert model name to vector name for consistency
        vector_name = model_name.replace("sentence-transformers/", "fast-").replace("all-MiniLM-L6-v2", "all-minilm-l6-v2").lower()
        logger.info(f"Recreating collection '{collection}' with dimension {dim} and vector name '{vector_name}'")
        vectors_config = {vector_name: VectorParams(size=dim, distance=Distance.COSINE)}
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
            chunk_overlap=chunk_overlap
        )
        logger.info("=== Indexing completed successfully! ===")
    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        if args.debug:
            logger.exception("Full traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Cross-Project Intelligence Collection Setup
Manages the dedicated collection for cross-project observations, patterns, and relationships.

Uses Phase 1 optimizations:
- DOT distance with normalized vectors
- HNSW tuning (m=40, ef_construct=384)
- On-disk storage + WAL
- Payload indexes for filtering
"""

from sentence_transformers import SentenceTransformer
from qdrant_client.http.models import (
    Distance,
    HnswConfigDiff,
    OptimizersConfigDiff,
    PayloadSchemaType,
    VectorParams,
    WalConfigDiff,
)
from qdrant_client import QdrantClient
import os
import sys
from pathlib import Path

# Add the rag/indexer directory to the path to import utilities
script_dir = Path(__file__).parent
rag_indexer_dir = script_dir.parent / "rag" / "indexer"
sys.path.insert(0, str(rag_indexer_dir))


def setup_intelligence_collection():
    """Create and configure the cross-project intelligence collection."""

    # Load environment variables
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY", "")
    collection_name = os.getenv(
        "INTELLIGENCE_COLLECTION_NAME", "cross_project_intelligence_mpnet")
    model_name = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

    print(
        f"🧠 Setting up Cross-Project Intelligence Collection: {collection_name}")
    print(f"📡 Qdrant URL: {qdrant_url}")
    print(f"🤖 Embedding Model: {model_name}")

    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=qdrant_url, api_key=api_key if api_key else None)

        # Get embedding dimension from model
        model = SentenceTransformer(model_name)
        embedding_dim = model.get_sentence_embedding_dimension()
        print(f"📐 Embedding Dimension: {embedding_dim}")

        # Create collection with Phase 1 optimizations
        # DOT distance (requires normalized vectors, ~30% faster than COSINE)
        # HNSW optimized for 768-dim MPNet embeddings
        vectors_config = {
            model_name: VectorParams(
                size=embedding_dim,
                distance=Distance.DOT,  # Changed from COSINE
                hnsw_config=HnswConfigDiff(
                    m=40,                # Graph connectivity for 768-dim
                    ef_construct=384,    # Build-time search effort
                    full_scan_threshold=10000,
                ),
                on_disk=True,  # Enable mmap for memory efficiency
            )
        }

        # Check if collection exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if collection_name in collection_names:
            print(f"⚠️  Collection '{collection_name}' already exists")
            recreate = input(
                "Do you want to recreate it? (y/N): ").lower().strip()
            if recreate == 'y':
                client.recreate_collection(
                    collection_name=collection_name,
                    vectors_config=vectors_config,
                    optimizers_config=OptimizersConfigDiff(
                        indexing_threshold=10000,
                    ),
                    wal_config=WalConfigDiff(
                        wal_capacity_mb=64,
                    ),
                )
                print(f"🔄 Recreated collection '{collection_name}' with Phase 1 optimizations")
            else:
                print(f"✅ Using existing collection '{collection_name}'")
                print(f"⚠️  Note: Existing collection may not have Phase 1 optimizations")
        else:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config,
                optimizers_config=OptimizersConfigDiff(
                    indexing_threshold=10000,
                ),
                wal_config=WalConfigDiff(
                    wal_capacity_mb=64,
                ),
            )
            print(f"✨ Created new collection '{collection_name}' with Phase 1 optimizations")

        # Create payload indexes for efficient pre-filtering
        print(f"📑 Creating payload indexes...")
        try:
            client.create_payload_index(
                collection_name=collection_name,
                field_name="repo",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            print(f"  ✓ Created index on 'repo' field")

            client.create_payload_index(
                collection_name=collection_name,
                field_name="language",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            print(f"  ✓ Created index on 'language' field")

            client.create_payload_index(
                collection_name=collection_name,
                field_name="pattern_type",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            print(f"  ✓ Created index on 'pattern_type' field")
        except Exception as e:
            print(f"  ⚠️  Some indexes may already exist: {e}")

        # Verify collection and show optimizations
        collection_info = client.get_collection(collection_name)
        print(f"\n📊 Collection Status: {collection_info.status}")
        print(f"📈 Vector Count: {collection_info.points_count}")

        # Show optimization details
        config = collection_info.config
        vec_config = config.params.vectors[model_name]
        print(f"\n🚀 Phase 1 Optimizations:")
        print(f"  • Distance: {vec_config.distance.value} (DOT = ~30% faster)")
        print(f"  • HNSW m: {vec_config.hnsw_config.m}")
        print(f"  • HNSW ef_construct: {vec_config.hnsw_config.ef_construct}")
        print(f"  • On-disk storage: {vec_config.on_disk}")
        print(f"  • Indexing threshold: {config.optimizer_config.indexing_threshold}")

        print(f"\n✅ Cross-Project Intelligence Collection setup complete!")
        print(f"\n🎯 Usage:")
        print(f"   - Framework docs: Use collection 'hish_framework_mpnet'")
        print(f"   - Cross-project intelligence: Use collection '{collection_name}'")
        print(f"   - ⚠️  Important: Vectors MUST be normalized before storage (DOT distance)")
        print(f"\n📋 Collection Purpose:")
        print(f"   - Pattern observations across projects")
        print(f"   - Relationship mappings between contexts")
        print(f"   - Effectiveness metrics and validation status")
        print(f"   - Knowledge flows and transfer opportunities")

    except Exception as e:
        print(f"❌ Error setting up intelligence collection: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_intelligence_collection()

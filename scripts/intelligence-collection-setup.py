#!/usr/bin/env python3
"""
Cross-Project Intelligence Collection Setup
Manages the dedicated collection for cross-project observations, patterns, and relationships.
"""

from sentence_transformers import SentenceTransformer
from qdrant_client.http.models import VectorParams, Distance
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

        # Create collection with named vectors for MCP compatibility
        vectors_config = {
            model_name: VectorParams(
                size=embedding_dim,
                distance=Distance.COSINE
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
                    collection_name, vectors_config=vectors_config)
                print(f"🔄 Recreated collection '{collection_name}'")
            else:
                print(f"✅ Using existing collection '{collection_name}'")
        else:
            client.create_collection(
                collection_name, vectors_config=vectors_config)
            print(f"✨ Created new collection '{collection_name}'")

        # Verify collection
        collection_info = client.get_collection(collection_name)
        print(f"📊 Collection Status: {collection_info.status}")
        print(f"📈 Vector Count: {collection_info.points_count}")

        print(f"\n✅ Cross-Project Intelligence Collection setup complete!")
        print(f"\n🎯 Usage:")
        print(
            f"   - Framework docs: Use collection '{os.getenv('COLLECTION_NAME', 'hish_framework')}'")
        print(
            f"   - Cross-project intelligence: Use collection '{collection_name}'")
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

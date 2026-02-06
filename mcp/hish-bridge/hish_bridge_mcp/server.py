"""
Hish MCP Bridge Server for Claude Code

Exposes Hish's Qdrant collections to Claude Code via MCP protocol.
Uses the same FastEmbed model and normalization as Hish's indexer for query compatibility.

Collections:
- hish_framework_mpnet: Framework docs, agent workflows, templates (READ-ONLY)
- cross_project_intelligence_mpnet: Cross-project patterns, learnings (READ/WRITE)
- {project}_docs_mpnet: Project-specific documentation (READ-ONLY)

Usage:
    python -m hish_bridge_mcp.server

Environment:
    QDRANT_URL: Qdrant server URL (default: http://localhost:6333)
    QDRANT_API_KEY: Optional API key for Qdrant Cloud
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime
from typing import Literal

import numpy as np
from fastembed import TextEmbedding
from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

# =============================================================================
# Configuration - MUST match Hish's indexer exactly
# =============================================================================

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VECTOR_NAME = EMBEDDING_MODEL  # Hish uses full model name as named vector key
VECTOR_DIM = 768

FRAMEWORK_COLLECTION = "hish_framework_mpnet"
INTELLIGENCE_COLLECTION = "cross_project_intelligence_mpnet"

PatternType = Literal["architecture", "decision", "learning", "anti-pattern", "bugfix"]

# =============================================================================
# Server Setup
# =============================================================================

mcp = FastMCP("hish-knowledge")

# =============================================================================
# Lazy-loaded Resources
# =============================================================================

_embedder: TextEmbedding | None = None
_qdrant: QdrantClient | None = None


def _normalize_vector(vector: list[float]) -> list[float]:
    """Normalize vector to unit length for DOT distance (matches Hish indexer)."""
    arr = np.array(vector, dtype=np.float64)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return vector
    return (arr / norm).tolist()


def get_embedder() -> TextEmbedding:
    """Lazy-load the embedding model to avoid startup delay."""
    global _embedder
    if _embedder is None:
        _embedder = TextEmbedding(model_name=EMBEDDING_MODEL)
    return _embedder


def get_qdrant() -> QdrantClient:
    """Lazy-load the Qdrant client."""
    global _qdrant
    if _qdrant is None:
        url = os.getenv("QDRANT_URL", "http://localhost:6333")
        api_key = os.getenv("QDRANT_API_KEY")
        _qdrant = QdrantClient(
            url=url,
            api_key=api_key if api_key else None,
            timeout=60,
        )
    return _qdrant


def embed_query(text: str) -> list[float]:
    """
    Embed query text using FastEmbed + normalize for DOT distance.

    Matches Hish indexer: same model, same normalization.
    """
    embedder = get_embedder()
    # FastEmbed.embed returns generator of ndarray
    vectors = list(embedder.embed([text]))
    if not vectors:
        return [0.0] * VECTOR_DIM
    vec = vectors[0]
    if hasattr(vec, "tolist"):
        vec = vec.tolist()
    else:
        vec = list(vec)
    return _normalize_vector(vec)


# =============================================================================
# MCP Tools
# =============================================================================


@mcp.tool()
def hish_find(
    query: str,
    collections: list[str] | None = None,
    limit: int = 5,
) -> dict:
    """
    Search Hish knowledge collections using semantic similarity.

    Args:
        query: Natural language search query describing what you're looking for
        collections: Which collections to search:
            - "framework": Framework docs, agent workflows, templates (hish_framework_mpnet)
            - "intelligence": Cross-project patterns, validated learnings (cross_project_intelligence_mpnet)
            - Or full name e.g. "myproject_docs_mpnet"
        limit: Maximum results per collection (default: 5)

    Returns:
        Search results with content, scores, and metadata from matching documents.

    Examples:
        - hish_find("JWT authentication patterns")
        - hish_find("error handling best practices", ["framework"])
        - hish_find("database migration strategy", ["intelligence"], 10)
    """
    if collections is None:
        collections = ["framework", "intelligence"]

    qdrant = get_qdrant()
    vector = embed_query(query)

    results: list[dict] = []
    collection_map = {
        "framework": FRAMEWORK_COLLECTION,
        "intelligence": INTELLIGENCE_COLLECTION,
    }

    for coll_key in collections:
        coll_name = collection_map.get(coll_key)
        if not coll_name:
            if coll_key.endswith("_docs_mpnet"):
                coll_name = coll_key
            else:
                continue

        try:
            response = qdrant.query_points(
                collection_name=coll_name,
                query=vector,
                using=VECTOR_NAME,
                limit=limit,
                with_payload=True,
            )

            for hit in response.points:
                payload = hit.payload or {}
                results.append({
                    "collection": coll_key,
                    "score": round(float(hit.score), 4),
                    "content": payload.get("content") or payload.get("document") or payload.get("raw_content", ""),
                    "type": payload.get("type", "unknown"),
                    "file_path": payload.get("path"),
                    "project": payload.get("project"),
                    "repo": payload.get("repo"),
                    "tags": payload.get("tags", []),
                })

        except UnexpectedResponse as e:
            results.append({"collection": coll_key, "error": f"Query failed: {str(e)}"})
        except Exception as e:
            results.append({"collection": coll_key, "error": str(e)})

    results.sort(key=lambda x: x.get("score", 0.0), reverse=True)

    return {
        "query": query,
        "embedding_model": EMBEDDING_MODEL,
        "total_results": len([r for r in results if "error" not in r]),
        "results": results,
    }


@mcp.tool()
def hish_find_framework(query: str, limit: int = 5) -> dict:
    """
    Search framework documentation, agent workflows, and templates.

    Use for: coding standards, agent behavioral patterns, workflow templates.

    Examples:
        - hish_find_framework("session workflow")
        - hish_find_framework("quality obsessed maintainable code")
    """
    return hish_find(query, collections=["framework"], limit=limit)


@mcp.tool()
def hish_find_intelligence(query: str, limit: int = 5) -> dict:
    """
    Search cross-project learnings, validated patterns, and architectural decisions.

    Use for: proven patterns, architectural decisions, solutions to common problems.

    Examples:
        - hish_find_intelligence("JWT refresh token")
        - hish_find_intelligence("database migration strategy")
    """
    return hish_find(query, collections=["intelligence"], limit=limit)


@mcp.tool()
def hish_find_project(query: str, project: str, limit: int = 5) -> dict:
    """
    Search project-specific documentation.

    Args:
        query: Natural language search query
        project: Project name (collection will be {project}_docs_mpnet)
        limit: Maximum number of results

    Examples:
        - hish_find_project("API endpoints", "vara")
        - hish_find_project("deployment process", "mayr")
    """
    collection_name = f"{project}_docs_mpnet"
    return hish_find(query, collections=[collection_name], limit=limit)


@mcp.tool()
def hish_store(
    content: str,
    pattern_type: str = "learning",
    project: str = "unknown",
    tags: list[str] | None = None,
    evidence: str = "",
) -> dict:
    """
    Store a validated pattern to cross-project intelligence.

    IMPORTANT: Only store after user approval.

    Framework collections are READ-ONLY. Only cross_project_intelligence accepts writes.

    Args:
        content: Clear, actionable pattern description
        pattern_type: architecture | decision | learning | anti-pattern | bugfix
        project: Source project name
        tags: Searchable tags for discovery
        evidence: How was this pattern validated?

    Example:
        hish_store(
            content="Pattern: Redis-backed JWT blacklist for token revocation...",
            pattern_type="architecture",
            project="vara-orchestrator",
            tags=["jwt", "redis", "security"],
            evidence="100% test coverage, handles 10k revocations/sec"
        )
    """
    valid_types = ["architecture", "decision", "learning", "anti-pattern", "bugfix"]
    if pattern_type not in valid_types:
        return {
            "status": "error",
            "message": f"Invalid pattern_type. Must be one of: {valid_types}",
        }

    if tags is None:
        tags = []

    qdrant = get_qdrant()
    vector = embed_query(content)
    point_id = str(uuid.uuid4())

    try:
        qdrant.upsert(
            collection_name=INTELLIGENCE_COLLECTION,
            points=[
                {
                    "id": point_id,
                    "vector": {VECTOR_NAME: vector},
                    "payload": {
                        "content": content,
                        "type": pattern_type,
                        "project": project,
                        "tags": tags,
                        "evidence": evidence,
                        "created_at": datetime.utcnow().isoformat(),
                        "source": "claude-code-mcp",
                    },
                }
            ],
        )

        return {
            "status": "stored",
            "id": point_id,
            "collection": INTELLIGENCE_COLLECTION,
            "message": "Pattern stored. Discoverable from both Cursor and Claude Code.",
        }

    except Exception as e:
        return {"status": "error", "message": f"Storage failed: {str(e)}"}


@mcp.tool()
def hish_collections() -> dict:
    """
    List available Hish knowledge collections and their status.

    Returns collection names, purposes, point counts, and write permissions.
    """
    qdrant = get_qdrant()
    collections_info: list[dict] = []

    known_collections = [
        (FRAMEWORK_COLLECTION, "Framework docs, agent workflows, templates", False),
        (INTELLIGENCE_COLLECTION, "Cross-project patterns, learnings, taxonomies", True),
    ]

    for name, purpose, writable in known_collections:
        try:
            info = qdrant.get_collection(name)
            collections_info.append({
                "name": name,
                "purpose": purpose,
                "writable": writable,
                "points_count": info.points_count,
                "status": "available",
            })
        except UnexpectedResponse:
            collections_info.append({
                "name": name,
                "purpose": purpose,
                "writable": writable,
                "status": "not_found",
            })
        except Exception as e:
            collections_info.append({
                "name": name,
                "purpose": purpose,
                "writable": writable,
                "status": "error",
                "error": str(e),
            })

    # Discover project-specific collections
    try:
        all_collections = qdrant.get_collections()
        for coll in all_collections.collections:
            if coll.name in (FRAMEWORK_COLLECTION, INTELLIGENCE_COLLECTION):
                continue
            if coll.name.endswith("_docs_mpnet"):
                project_name = coll.name.replace("_docs_mpnet", "")
                try:
                    info = qdrant.get_collection(coll.name)
                    collections_info.append({
                        "name": coll.name,
                        "purpose": f"Project documentation for {project_name}",
                        "writable": False,
                        "points_count": info.points_count,
                        "status": "available",
                    })
                except Exception:
                    pass
    except Exception:
        pass

    return {
        "embedding_model": EMBEDDING_MODEL,
        "vector_dimensions": VECTOR_DIM,
        "collections": collections_info,
    }


# =============================================================================
# Entry Point
# =============================================================================


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()

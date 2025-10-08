# HISH Local Qdrant Optimization & Cursor Integration

**Date Started:** 2025-10-06
**Status:** ✅ Phase 1 COMPLETE - Core Optimizations Implemented
**Objective:** Optimize local Qdrant code vectorization for performance and enforce Qdrant-first retrieval in Cursor agents.

---

## 🎯 Goals

1. **Optimize Qdrant vectorization pipeline** for low-latency, high-recall code search
2. **Enforce Qdrant-first retrieval** - Agents prefer local Qdrant MCP over Cursor's built-in semantic search
3. **Performance targets**: p95 latency minimal, Recall@10 ≥ 0.9
4. **Keep using MPNet** (768-dim) with optimized configuration

---

## 📋 Current State Analysis

### **✅ Already Implemented:**
- Model: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (768-dim)
- Storage: Qdrant with named vectors for MCP compatibility
- MCP integration: Existing `qdrant-unified` MCP server
- Distance metric: **COSINE** (current)
- Collection management: Auto-detection of code vs framework collections
- Batch processing: Configurable batch sizes

### **❌ Missing Optimizations:**
- [ ] **Normalization**: Embeddings not normalized on write
- [ ] **Distance metric**: Using COSINE instead of DOT (less efficient)
- [ ] **HNSW params**: Default params, not optimized (need m=40, ef_construct=384)
- [ ] **Search ef**: Using default, need ef=96
- [ ] **Quantization**: Not enabled (scalar int8 or PQ M=48)
- [ ] **On-disk storage**: Not configured (mmap, WAL)
- [ ] **Code-aware chunking**: Generic chunking (200-400 tokens, 30-50 overlap needed)
- [ ] **Payload indexes**: No indexes on repo/lang/path_prefix
- [ ] **GPU acceleration**: No .half() optimization for CUDA
- [ ] **Pre-filtering**: No repo/lang/path filtering before ANN
- [ ] **Cursor integration**: No hook to prefer Qdrant over @codebase

---

## 🗺️ Implementation Plan (4 Phases)

### **Phase 1: Core Qdrant Optimizations** ✅ COMPLETE
**Goal:** Optimize vector storage and search performance

**Changes Implemented:**
1. ✅ **Normalize embeddings on write** (app.py:251-261)
   - Added `normalize_vectors()` function
   - Normalizes after embedding generation
   - Ensures unit vectors for DOT = COSINE but faster

2. ✅ **Switch to DOT distance** (app.py:323)
   - Changed `Distance.COSINE` → `Distance.DOT`
   - Works correctly with normalized vectors
   - ~20-30% faster than COSINE

3. ✅ **Configure HNSW parameters** (app.py:324-328)
   - Added `HnswConfigDiff(m=40, ef_construct=384)`
   - Better graph connectivity for 768-dim vectors
   - Default search `ef=96` (tune 64-128 based on latency)

4. ✅ **Enable on-disk storage** (app.py:329, 334-342)
   - Added `on_disk=True` for vectors
   - Added WAL settings for durability
   - Reduces memory pressure

5. ✅ **Add payload indexes** (app.py:264-294, 310, 350)
   - Created `create_payload_indexes()` function
   - Indexes on `repo`, `language`, `path_prefix`
   - Enables efficient pre-filtering

6. ✅ **Add metadata extraction** (app.py:504-576)
   - Extract `language` from file extension (30+ languages)
   - Extract `path_prefix` from file path
   - Add to payload for filtering

**Files Modified:**
- ✅ `rag/indexer/app.py` - Core optimizations (~150 lines changed)
- ✅ `rag/indexer/requirements.txt` - Added numpy>=1.21.0
- ✅ `requirements-dev.txt` - Include indexer requirements
- ✅ `Makefile` - Enhanced dev-setup target
- ✅ `docs/development/dev-environment-setup.md` - New setup guide
- ✅ `scripts/test-qdrant-optimizations.py` - Validation tests

**Test & Validate:**
```bash
# Setup dev environment (one-time)
mkvirtualenv hish-dev --python=python3.12
workon hish-dev
make dev-setup

# Run validation tests
python3 scripts/test-qdrant-optimizations.py

# Test on real collection (recreates collection with optimizations)
make index-framework
```

---

### **Phase 2: Code-Aware Chunking**
**Goal:** Improve chunking for code content

**Changes:**
1. **Adjust chunk sizes** (chunkers.py)
   - Code: 200-400 tokens (currently 512)
   - Overlap: 30-50 tokens (currently 50)
   - Language-aware boundaries

2. **Add code structure awareness** (chunkers.py)
   - Respect function/class boundaries
   - Preserve import statements with chunks
   - Keep comments with code

3. **Metadata enrichment** (app.py:process_single_file)
   - Add `repo` field to payload
   - Add `language` field (from file extension)
   - Add `path_prefix` field (first 2-3 path components)
   - Add `file_type` (code vs docs)

**Files to modify:**
- `rag/indexer/chunkers.py` (chunk sizes, boundaries)
- `rag/indexer/app.py` (metadata extraction)
- `config/env.mpnet.code` (chunk config updates)

**Estimated changes:** 2 files, ~150 lines modified

---

### **Phase 3: Quantization & GPU Acceleration**
**Goal:** Reduce memory and improve encoding speed

**Changes:**
1. **Scalar quantization (int8)** (app.py:ensure_collection)
   - Add `ScalarQuantization` config
   - Start with int8 (simple, fast)
   - Only if collection expected >1M vectors
   - Keep PQ off by default (use only if memory pressure)

2. **GPU acceleration** (app.py:embedder)
   - Detect CUDA availability
   - Use `.half()` for FP16 on GPU
   - Adjust batch sizes: CPU 64-128, GPU 256-1024

3. **Batch encoding optimization** (app.py:process_single_file)
   - Dynamic batch sizing based on device
   - Memory-aware batching
   - Progress reporting

**Files to modify:**
- `rag/indexer/app.py` (embedder, ensure_collection, batching)
- `config/env.mpnet.code` (batch size configs)

**Estimated changes:** 1 file, ~80 lines modified

---

### **Phase 4: Cursor Agent Integration**
**Goal:** Enforce Qdrant-first retrieval in Cursor

**Changes:**
1. **Create Cursor hook infrastructure**
   - Create `.cursor/hooks/` directory
   - Add `pre_prompt` hook script
   - Hook calls MCP `qdrant-find` before Cursor search

2. **Update agent personas**
   - Add rule: "Use `local_qdrant` results as primary code context"
   - Fallback to built-in search only if Qdrant returns nothing
   - Explicit preference for local indexed code

3. **MCP search integration**
   - Hook calls existing `qdrant-unified` MCP server
   - Injects results as `extra_context` named `local_qdrant`
   - Pre-filters by repo/lang/path before ANN search
   - Uses `ef=96` (configurable)

4. **Update prompts**
   - `prompts/dev_agent/dev_agent_init_prompt.md`
   - `templates/dev_agent_persona.md`
   - `prompts/qa/qa_agent_init_prompt.md`
   - `prompts/red_team/red_team_agent_init_prompt.md`

**Files to create:**
- `.cursor/hooks/pre_prompt` (Python script)
- `.cursor/hooks/hish_local_search.py` (MCP client wrapper)
- `.cursor/hooks/README.md` (documentation)

**Files to modify:**
- `prompts/dev_agent/dev_agent_init_prompt.md`
- `templates/dev_agent_persona.md`
- `prompts/qa/qa_agent_init_prompt.md`
- `prompts/red_team/red_team_agent_init_prompt.md`
- `scripts/run-mcp-unified.sh` (ensure hook can call it)

**Estimated changes:** 3 new files, 5 files modified, ~300 lines total

---

## 📝 Detailed Implementation Specs

### **Normalization Implementation:**

```python
def normalize_vectors(vectors: List[List[float]]) -> List[List[float]]:
    """Normalize vectors to unit length for DOT distance."""
    import numpy as np
    arr = np.array(vectors)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return (arr / norms).tolist()
```

### **HNSW Configuration:**

```python
from qdrant_client.http.models import (
    Distance, VectorParams, HnswConfigDiff,
    OptimizersConfigDiff, WalConfigDiff
)

vectors_config = {
    model_name: VectorParams(
        size=dim,
        distance=Distance.DOT,  # Changed from COSINE
        hnsw_config=HnswConfigDiff(
            m=40,               # Graph connectivity (768-dim optimal)
            ef_construct=384,   # Build-time search
            full_scan_threshold=10000,  # Use HNSW above this
        ),
        on_disk=True,  # Enable mmap
    )
}

# Collection-level config
client.recreate_collection(
    collection_name=name,
    vectors_config=vectors_config,
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=10000,  # Start indexing after 10k points
    ),
    wal_config=WalConfigDiff(
        wal_capacity_mb=64,  # WAL size
    ),
)
```

### **Scalar Quantization (conditional):**

```python
from qdrant_client.http.models import ScalarQuantization, ScalarType

# Only if expecting >1M vectors
if expected_size > 1_000_000:
    vectors_config[model_name].quantization_config = ScalarQuantization(
        type=ScalarType.INT8,
        quantile=0.99,  # Outlier handling
        always_ram=False,  # Allow disk
    )
```

### **Payload Indexing:**

```python
# After collection creation
client.create_payload_index(
    collection_name=name,
    field_name="repo",
    field_schema="keyword",
)
client.create_payload_index(
    collection_name=name,
    field_name="language",
    field_schema="keyword",
)
client.create_payload_index(
    collection_name=name,
    field_name="path_prefix",
    field_schema="keyword",
)
```

### **Cursor Pre-Prompt Hook:**

```python
#!/usr/bin/env python3
"""
HISH Cursor Pre-Prompt Hook
Injects local Qdrant results before Cursor's built-in semantic search
"""
import sys
import json
from pathlib import Path

# Import our MCP client wrapper
sys.path.insert(0, str(Path(__file__).parent))
from hish_local_search import search_local_qdrant

def main():
    event = json.load(sys.stdin)
    query = event.get("prompt", "")
    meta = event.get("metadata", {}) or {}

    # Extract filters from metadata
    filters = {
        k: meta.get(k)
        for k in ("repo", "language", "path_prefix")
        if meta.get(k) is not None
    }

    # Search local Qdrant via MCP
    hits = search_local_qdrant(
        query=query,
        collection="all_code",  # or auto-detect from context
        top_k=40,
        ef=96,  # Search effort
        filters=filters,
    )

    if hits:
        # Inject as extra context
        event.setdefault("extra_context", [])
        event["extra_context"].insert(0, {
            "name": "local_qdrant",
            "content": "\n\n".join(
                f"[{h.get('path')}:{h.get('span','')}]\n{h['text']}"
                for h in hits[:20]
            ),
            "priority": "high",  # Prefer over built-in
        })

        # Add system instruction
        preamble = (
            "CRITICAL: Prefer `local_qdrant` context from our local code index. "
            "Only use Cursor's built-in snippets if `local_qdrant` returned nothing. "
            "Local Qdrant results are more accurate and up-to-date."
        )
        event["system_prompt_preamble"] = preamble

    json.dump(event, sys.stdout)

if __name__ == "__main__":
    main()
```

### **MCP Client Wrapper:**

```python
"""
hish_local_search.py
Wrapper for calling HISH MCP Qdrant search
"""
import subprocess
import json
from typing import List, Dict, Any, Optional

def search_local_qdrant(
    query: str,
    collection: str = "all_code",
    top_k: int = 40,
    ef: int = 96,
    filters: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Search local Qdrant via MCP server.

    Args:
        query: Search query text
        collection: Collection name (auto-detect if "all_code")
        top_k: Number of results
        ef: HNSW search effort (64-128)
        filters: Payload filters (repo, language, path_prefix)

    Returns:
        List of matches with path, span, text, score
    """
    # Build MCP request
    mcp_request = {
        "method": "qdrant-find",
        "params": {
            "query": query,
            "collection_name": collection,
            "limit": top_k,
            "score_threshold": 0.7,  # Minimum relevance
        }
    }

    # Add filters if provided
    if filters:
        mcp_request["params"]["filter"] = {
            "must": [
                {"key": k, "match": {"value": v}}
                for k, v in filters.items()
            ]
        }

    # Call MCP server (adapt to your actual invocation)
    # This assumes the MCP server is callable via script
    try:
        result = subprocess.run(
            ["bash", "-c", "source ./scripts/run-mcp-unified.sh && mcp_search"],
            input=json.dumps(mcp_request),
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            return parse_mcp_results(data)
    except Exception as e:
        print(f"MCP search failed: {e}", file=sys.stderr)

    return []

def parse_mcp_results(data: Dict) -> List[Dict[str, Any]]:
    """Parse MCP response into standardized format."""
    hits = []
    for item in data.get("results", []):
        hits.append({
            "path": item.get("metadata", {}).get("path", "unknown"),
            "span": item.get("metadata", {}).get("span", ""),
            "text": item.get("content", ""),
            "score": item.get("score", 0.0),
            "repo": item.get("metadata", {}).get("repo"),
            "language": item.get("metadata", {}).get("language"),
        })
    return hits
```

---

## 📊 Performance Targets

### **Latency:**
- **p50**: <100ms for queries with <50k vectors
- **p95**: <500ms for queries with <500k vectors
- **p99**: <1s for queries with <5M vectors

### **Recall:**
- **Recall@10**: ≥ 0.9 vs brute-force baseline
- **Recall@20**: ≥ 0.95 vs brute-force baseline

### **Memory:**
- **Without quantization**: ~4GB per 1M 768-dim vectors
- **With int8**: ~2GB per 1M vectors
- **With PQ M=48**: ~1GB per 1M vectors (use only if needed)

### **Throughput:**
- **CPU encoding**: 64-128 docs/batch → ~100-200 docs/sec
- **GPU encoding**: 256-1024 docs/batch → ~1000-2000 docs/sec

---

## ✅ Acceptance Criteria

**Phase 1 (Core Optimizations):**
- [x] Embeddings normalized on write
- [x] Qdrant uses DOT distance with normalized vectors
- [x] HNSW configured: m=40, ef_construct=384, ef=96
- [x] On-disk mmap and WAL enabled
- [x] Payload indexes on repo/lang/path_prefix
- [x] Metadata extraction (language, path_prefix)
- [x] Dev environment setup documented
- [x] Validation tests created

**Phase 2 (Code-Aware Chunking):**
- [ ] Scalar int8 quantization ready (off by default)
- [ ] Code-aware chunking: 200-400 tokens, 30-50 overlap
- [ ] Language-specific chunking boundaries

**Phase 3 (GPU & Quantization):**
- [ ] GPU .half() optimization when CUDA available
- [ ] Dynamic batch sizing (CPU/GPU)
- [ ] Scalar int8 quantization (conditional)

**Phase 4 (Cursor Integration):**
- [ ] Pre-filtering by repo/lang/path before ANN
- [ ] Cursor hook prefers local Qdrant over built-in search
- [ ] Agent personas updated with Qdrant-first rule
- [ ] Performance validated: p95 latency meets target, Recall@10 ≥ 0.9

---

## 🔄 Validation Plan

### **Phase 1 Validation:**
```bash
# Test normalized DOT vs COSINE
python3 -c "from rag.indexer.app import test_normalization"

# Benchmark search latency
python3 scripts/benchmark-search.py --ef 96 --queries 100

# Verify HNSW params
curl http://localhost:6333/collections/{name} | jq '.result.config.hnsw_config'
```

### **Phase 2 Validation:**
```bash
# Test chunking on sample files
python3 scripts/test-chunking.py --input tests/fixtures/sample_code/

# Verify metadata extraction
python3 scripts/verify-metadata.py --collection test_code_mpnet
```

### **Phase 3 Validation:**
```bash
# Test GPU encoding
python3 scripts/test-gpu-encoding.py

# Benchmark quantization
python3 scripts/benchmark-quantization.py --type int8
```

### **Phase 4 Validation:**
```bash
# Test Cursor hook
.cursor/hooks/pre_prompt < tests/fixtures/sample_event.json

# End-to-end test with agent
# Use agent, verify it references local_qdrant context
```

### **Recall Testing:**
```python
# Generate 50-100 query sample
# Compare results: local Qdrant vs brute-force
# Measure Recall@10, Recall@20
# Ensure ≥ 0.9 recall threshold
```

---

## 🚨 Rollback Plan

### **Preparation:**
- [ ] Tag current state: `git tag pre-qdrant-optimization`
- [ ] Backup existing collections: `make backup`
- [ ] Document current HNSW settings

### **Rollback:**
```bash
# Revert code changes
git reset --hard pre-qdrant-optimization

# Restore collections from backup
# OR recreate with old settings
```

---

## 💬 Notes

- **MPNet model unchanged** - keeping 768-dim
- **MCP compatibility preserved** - named vectors maintained
- **Backward compatible** - old collections continue working
- **Cursor hook optional** - can be disabled if issues arise
- **Quantization conservative** - start with int8, PQ only if needed

---

**Last Updated:** 2025-10-06 (Initial planning)

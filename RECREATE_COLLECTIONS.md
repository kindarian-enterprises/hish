# Recreate Collections with Phase 1 Optimizations

## Why Recreate?

Old collections use:
- COSINE distance
- Non-normalized vectors
- Default HNSW params
- No payload indexes

New collections use:
- DOT distance (~30% faster)
- Normalized vectors
- Optimized HNSW (m=40, ef_construct=384)
- Payload indexes on repo/language/path_prefix
- On-disk storage + WAL

**They're incompatible**, so we need to delete and recreate.

---

## Step 1: Check Existing Collections

```bash
curl -s http://localhost:6333/collections | jq -r '.result.collections[].name'
```

## Step 2: Delete Old Collections

```bash
# Delete framework collection
curl -X DELETE http://localhost:6333/collections/hish_framework_mpnet

# Delete any code collections (adjust names as needed)
curl -X DELETE http://localhost:6333/collections/YOUR_PROJECT_code_mpnet

# Delete intelligence collection if it exists
curl -X DELETE http://localhost:6333/collections/cross_project_intelligence_mpnet
```

## Step 3: Verify Deletion

```bash
curl -s http://localhost:6333/collections | jq -r '.result.collections[]'
```

Should show empty or remaining collections.

## Step 4: Recreate with Optimizations

```bash
cd /home/nshimokochi/Documents/projects/hish

# Recreate framework collection (with optimizations)
make index-framework

# Recreate intelligence collection
make setup-intelligence

# Recreate code collections (if you have projects configured)
make index-code
```

## Step 5: Verify New Configuration

```bash
# Check framework collection config
curl -s http://localhost:6333/collections/hish_framework_mpnet | jq '.result.config'
```

Should show:
```json
{
  "params": {
    "vectors": {
      "sentence-transformers/paraphrase-multilingual-mpnet-base-v2": {
        "size": 768,
        "distance": "Dot",        // ← Was "Cosine"
        "hnsw_config": {
          "m": 40,                 // ← Was 16 (default)
          "ef_construct": 384,     // ← Was 100 (default)
          "full_scan_threshold": 10000
        },
        "on_disk": true            // ← New
      }
    }
  },
  "optimizer_config": {
    "indexing_threshold": 10000    // ← New
  },
  "wal_config": {
    "wal_capacity_mb": 64          // ← New
  }
}
```

Check payload indexes:
```bash
curl -s http://localhost:6333/collections/hish_framework_mpnet | jq '.result.payload_schema'
```

Should show indexes on: `repo`, `language`, `path_prefix`

---

## Quick Delete All + Recreate

```bash
cd /home/nshimokochi/Documents/projects/hish

# Delete all collections
for collection in $(curl -s http://localhost:6333/collections | jq -r '.result.collections[].name'); do
  echo "Deleting $collection..."
  curl -X DELETE http://localhost:6333/collections/$collection
done

# Recreate with optimizations
make setup-intelligence
make index-framework
make index-code  # If you have projects configured
```

---

## Troubleshooting

**Qdrant not running:**
```bash
docker compose -f deploy/compose.rag.yml up -d
```

**Check Qdrant status:**
```bash
curl http://localhost:6333/health
```

**View logs:**
```bash
docker compose -f deploy/compose.rag.yml logs -f qdrant
```

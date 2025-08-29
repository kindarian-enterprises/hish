#!/bin/bash

# Optimize Qdrant collections for better search quality
# Sets ef_search parameter to improve recall

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Configuration
QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"
EF_SEARCH="${EF_SEARCH:-128}"  # Use 256 for beefy boxes

print_info "Optimizing Qdrant collections for better search quality"
print_info "Qdrant URL: $QDRANT_URL"
print_info "ef_search: $EF_SEARCH"

# Check if Qdrant is accessible
if ! curl -s "$QDRANT_URL/collections" > /dev/null; then
    print_error "Cannot connect to Qdrant at $QDRANT_URL"
    print_info "Make sure Qdrant is running and accessible"
    exit 1
fi

# Get list of collections
print_info "Fetching collections..."
collections=$(curl -s "$QDRANT_URL/collections" | jq -r '.result.collections[].name' 2>/dev/null || echo "")

if [ -z "$collections" ]; then
    print_warning "No collections found or error fetching collections"
    exit 0
fi

print_info "Found collections: $collections"

# Optimize each collection
for collection in $collections; do
    print_info "Optimizing collection: $collection"
    
    # Get current collection info
    current_config=$(curl -s "$QDRANT_URL/collections/$collection" | jq '.result.config.params.vectors' 2>/dev/null || echo "")
    
    if [ -z "$current_config" ]; then
        print_warning "Could not get current config for $collection, skipping..."
        continue
    fi
    
    # Update ef_search parameter
    update_payload=$(cat <<EOF
{
    "optimizers_config": {
        "ef_search": $EF_SEARCH
    }
}
EOF
)
    
    print_info "Setting ef_search=$EF_SEARCH for $collection..."
    
    if curl -s -X PATCH "$QDRANT_URL/collections/$collection" \
        -H "Content-Type: application/json" \
        -d "$update_payload" > /dev/null; then
        print_success "Successfully optimized $collection"
    else
        print_error "Failed to optimize $collection"
    fi
done

print_success "Collection optimization complete!"
print_info "All collections now use ef_search=$EF_SEARCH for better search quality"
print_info ""
print_info "Note: This setting improves recall but may increase search latency"
print_info "Adjust EF_SEARCH environment variable if you need different values:"
print_info "  - 64: Fast searches, lower recall"
print_info "  - 128: Balanced (default)"
print_info "  - 256: Higher recall, slower searches (for beefy boxes)"

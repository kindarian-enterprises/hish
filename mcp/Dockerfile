FROM python:3.11-slim

# Install mcp-server-qdrant and dependencies
RUN pip install --no-cache-dir mcp-server-qdrant

# Pre-warm the embedding model to avoid download delay on startup
RUN python -c "from fastembed import TextEmbedding; print('Pre-warming embedding model...'); model = TextEmbedding(model_name='sentence-transformers/all-MiniLM-L6-v2'); list(model.embed(['test'])); print('Model ready!')"

# Set default command
CMD ["mcp-server-qdrant"]

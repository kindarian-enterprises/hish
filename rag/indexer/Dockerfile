FROM python:3.12-slim AS base

WORKDIR /app

# System deps for tokenizers/curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git ca-certificates && rm -rf /var/lib/apt/lists/*

# Production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py chunkers.py util.py ./

# Test stage with additional dependencies
FROM base AS test

# Install test dependencies
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# Copy test files
COPY tests/ ./tests/
COPY pytest.ini .

# Default test command
CMD ["pytest", "-v", "--tb=short"]

# Production stage (default)
FROM base AS production

# Default command shows help
CMD ["python", "app.py", "--help"]
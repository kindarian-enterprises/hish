# Hish Cursor Context Framework - Makefile
# Multi-project development agent framework with shared knowledge

.PHONY: help health test new-context list-contexts index-repo reindex-contexts clean logs index collections setup-cursor quick-start backup mcp build-mcp optimize-collections index-framework setup-intelligence lint lint-fix format type-check mypy-errors pre-commit-install dev-setup

# Default target
help: ## Show this help message
	@echo "🧠 Hish Cursor Context Framework"
	@echo "====================================="
	@echo "Multi-project development agent framework with shared knowledge"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Framework Management

health: ## Check service health
	@echo "🏥 Health Check:"
	@echo -n "Qdrant: "
	@curl -s http://localhost:6333/health > /dev/null && echo "✅ Healthy" || echo "❌ Unhealthy"
	@echo -n "Collections: "
	@curl -s http://localhost:6333/collections | jq -r '.result.collections[] | .name' 2>/dev/null | wc -l | xargs -I {} echo "{} collections available"

logs: ## Show framework logs
	@echo "📜 Framework Logs:"
	docker compose -f deploy/compose.rag.yml --env-file config/env.framework logs -f

# Project Management
new-context: ## Create a new project context (interactive)
	@echo "📝 Creating new project context..."
	./scripts/new-project-context.sh

list-contexts: ## List all project contexts
	@echo "📁 Project Contexts:"
	@echo "Local contexts (gitignored):"
	@find local -maxdepth 1 -type d -not -path local 2>/dev/null | sort | while read dir; do \
		echo "  🎯 $$(basename $$dir) - $$dir"; \
	done
	@echo ""
	@echo "Shared contexts (tracked):"
	@find contexts -maxdepth 1 -type d -not -path contexts 2>/dev/null | sort | while read dir; do \
		echo "  📚 $$(basename $$dir) - $$dir"; \
	done
	@echo ""
	@echo "💡 Agents discover context automatically - no configuration needed"



# Knowledge Management
index: ## Index framework docs and all project code repositories (host-based) - Uses unified MPNet embeddings
	@echo "🚀 Host-based indexing with unified MPNet embeddings..."
	@echo "📚 Indexing framework documentation with MPNet (preserving existing data)..."
	@python3 scripts/host-indexer.py --work-dir "$(PWD)" --env-file config/env.mpnet --collection hish_framework_mpnet
	@echo "🔍 Discovering and indexing project code repositories with MPNet..."
	@if [ -d "local" ]; then \
		for context_dir in local/*/; do \
			if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
				repo_path=$$(cat "$$context_dir/repo_path.txt" | tr -d '\n'); \
				context_name=$$(basename "$$context_dir"); \
				if [ -d "$$repo_path" ]; then \
					echo "📁 Host-indexing $$context_name code with MPNet: $$repo_path"; \
					echo "⚠️  WARNING: Code collection will be DROPPED and RECREATED with MPNet embeddings!"; \
					python3 scripts/host-indexer.py --work-dir "$$repo_path" --env-file config/env.mpnet.code --collection "$${context_name}_code_mpnet" --recreate; \
				else \
					echo "⚠️  Repo path not found for $$context_name: $$repo_path"; \
				fi; \
			fi; \
		done; \
	else \
		echo "ℹ️  No local contexts found. Create one with make new-context"; \
	fi
	@echo "✅ Indexing complete! Framework and code repositories now use unified MPNet embeddings."

index-code: ## Index all project code repositories with MPNet embeddings (DESTRUCTIVE: replaces existing code collections)
	@echo "🔍 Indexing all project code repositories with MPNet embeddings..."
	@if [ -d "local" ]; then \
		for context_dir in local/*/; do \
			if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
				repo_path=$$(cat "$$context_dir/repo_path.txt" | tr -d '\n'); \
				context_name=$$(basename "$$context_dir"); \
				if [ -d "$$repo_path" ]; then \
					echo "📁 MPNet indexing $$context_name: $$repo_path"; \
					echo "⚠️  WARNING: Code collection will be DROPPED and RECREATED with MPNet!"; \
					python3 scripts/host-indexer.py --work-dir "$$repo_path" --env-file config/env.mpnet.code --collection "$${context_name}_code_mpnet" --recreate; \
				else \
					echo "⚠️  Repo path not found for $$context_name: $$repo_path"; \
				fi; \
			fi; \
		done; \
	else \
		echo "ℹ️  No local contexts found. Create one with make new-context"; \
	fi
	@echo "✅ Code repository indexing complete! All code now uses MPNet embeddings."

index-framework: ## Index framework docs only with MPNet embeddings - ONLY vectorized documentation, NOT learnings - PRESERVES existing data
	@echo "📚 Indexing framework documentation with MPNet embeddings..."
	@echo "ℹ️  Framework collection will be updated, preserving existing data..."
	@python3 scripts/host-indexer.py --work-dir "$(PWD)" --env-file $(or $(ENV_FILE),config/env.mpnet) --collection hish_framework_mpnet
	@echo "✅ Framework documentation indexing complete!"

setup-intelligence: ## Setup cross-project intelligence collection with MPNet embeddings - For patterns applicable to framework or 2+ projects
	@echo "🧠 Setting up cross-project intelligence collection with MPNet..."
	@EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2 INTELLIGENCE_COLLECTION_NAME=cross_project_intelligence_mpnet python3 scripts/intelligence-collection-setup.py
	@echo "✅ Intelligence collection setup complete!"

reindex-contexts: ## Reindex specific contexts (Usage: make reindex-contexts CONTEXTS="context1 context2 context3") - DESTRUCTIVE: replaces code data only
	@if [ -z "$(CONTEXTS)" ]; then \
		echo "❌ Usage: make reindex-contexts CONTEXTS=\"context1 context2 context3\""; \
		echo "📁 Available project contexts:"; \
		if [ -d "local" ]; then \
			found_contexts=false; \
			for context_dir in local/*/; do \
				if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
					echo "  - $$(basename "$$context_dir")"; \
					found_contexts=true; \
				fi; \
			done; \
			if [ "$$found_contexts" = false ]; then \
				echo "  (no project contexts found)"; \
			fi; \
		else \
			echo "  (no contexts found)"; \
		fi; \
		exit 1; \
	fi
	@echo "🔄 Reindexing specified contexts: $(CONTEXTS)"
	@echo "⚠️  WARNING: Code collections will be DROPPED and RECREATED, losing existing code data!"
	@for context_name in $(CONTEXTS); do \
		context_dir="local/$$context_name"; \
		if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
			repo_path=$$(cat "$$context_dir/repo_path.txt" | tr -d '\n'); \
			if [ -d "$$repo_path" ]; then \
				echo "📁 Reindexing $$context_name: $$repo_path"; \
				make index-repo REPO_PATH="$$repo_path" COLLECTION_NAME="$${context_name}_code_mpnet"; \
			else \
				echo "⚠️  Repo path not found for $$context_name: $$repo_path"; \
			fi; \
		else \
			echo "❌ Context '$$context_name' not found or missing repo_path.txt"; \
		fi; \
	done
	@echo "✅ Reindexing complete for: $(CONTEXTS)"

index-repo: ## Index a specific repository with unified MPNet embeddings - Auto-detects collection type
	@if [ -z "$(REPO_PATH)" ] || [ -z "$(COLLECTION_NAME)" ]; then \
		echo "❌ Usage: make index-repo REPO_PATH=/path/to/repo COLLECTION_NAME=collection_name"; \
		exit 1; \
	fi
	@echo "📚 Host-based indexing of repository: $(REPO_PATH)"
	@echo "📁 Collection: $(COLLECTION_NAME)"
	@if [ "$(REPO_PATH)" = "." ] || echo "$(COLLECTION_NAME)" | grep -E "(hish_framework|cross_project_intelligence|framework_docs)" > /dev/null; then \
		echo "🔍 Framework collection detected - using MPNet embeddings..."; \
		echo "ℹ️  Framework collection will be updated, preserving existing data..."; \
		python3 scripts/host-indexer.py --work-dir "$(REPO_PATH)" --env-file config/env.mpnet --collection "$(COLLECTION_NAME)"; \
	else \
		echo "🔍 Code collection detected - using MPNet embeddings..."; \
		echo "⚠️  WARNING: Code collection will be DROPPED and RECREATED with MPNet!"; \
		python3 scripts/host-indexer.py --work-dir "$(REPO_PATH)" --env-file config/env.mpnet.code --collection "$(COLLECTION_NAME)" --recreate; \
	fi

collections: ## List all knowledge collections
	@echo "🗂️  Knowledge Collections:"
	@curl -s http://localhost:6333/collections | jq -r '.result.collections[].name' 2>/dev/null | while read collection; do \
		points=$$(curl -s http://localhost:6333/collections/$$collection | jq -r '.result.points_count' 2>/dev/null || echo "unknown"); \
		echo "  📚 $$collection - $$points chunks"; \
	done || echo "❌ Could not connect to Qdrant"

optimize-collections: ## Optimize collections for better search quality (sets ef_search=128)
	@echo "🚀 Optimizing collections for better search quality..."
	@./scripts/optimize-collections.sh



# Development
dev-setup: ## Install development dependencies and pre-commit hooks
	@echo "🔧 Setting up development environment..."
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "✅ Development environment ready!"

test: ## Run framework tests (host-based)
	@echo "🧪 Running framework tests..."
	@echo "📋 Using host-based testing environment..."
	cd rag/indexer && python -m pytest tests/ -v

# Code Quality
lint: ## Run all linting checks (ruff, black, isort, mypy)
	@echo "🔍 Running code quality checks..."
	@echo "📁 Checking rag/indexer/..."
	cd rag/indexer && ruff check . --output-format=concise
	cd rag/indexer && black --check --diff .
	cd rag/indexer && isort --check-only --diff .
	cd rag/indexer && mypy . --ignore-missing-imports || echo "⚠️ Type checking found issues (non-blocking)"
	@echo "✅ Linting complete!"

lint-fix: ## Fix auto-fixable linting issues
	@echo "🔧 Fixing linting issues..."
	cd rag/indexer && ruff check . --fix
	cd rag/indexer && black .
	cd rag/indexer && isort .
	@echo "✅ Auto-fixes applied!"

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	cd rag/indexer && black .
	cd rag/indexer && isort .
	@echo "✅ Code formatted!"

type-check: ## Run type checking with mypy
	@echo "🔍 Running type checks..."
	cd rag/indexer && mypy . --ignore-missing-imports
	@echo "✅ Type checking complete!"

mypy-errors: ## Show mypy errors in detail
	@echo "🔍 Detailed mypy error analysis..."
	cd rag/indexer && mypy app.py --ignore-missing-imports --show-error-codes || true

pre-commit-install: ## Install pre-commit hooks
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install
	@echo "✅ Pre-commit hooks installed!"

clean: ## Clean up containers and volumes
	@echo "🧹 Cleaning up framework..."
	docker compose -f deploy/compose.rag.yml --env-file config/env.framework down -v
	docker system prune -f

# Maintenance

backup: ## Backup knowledge database
	@echo "💾 Backing up knowledge database..."
	@BACKUP_FILE="hish-knowledge-backup-$$(date +%Y%m%d-%H%M%S).tar.gz"
	@tar -czf "$$BACKUP_FILE" rag/qdrant_data/ 2>/dev/null || tar -czf "$$BACKUP_FILE" .data/qdrant/ 2>/dev/null || echo "❌ No data directory found"
	@echo "✅ Backup created: $$BACKUP_FILE"

quick-start: ## Quick setup guide - show configuration steps
	@echo "🚀 Hish Cursor Context - Quick Start"
	@echo "========================================"
	@echo ""
	@echo "📋 Setup Steps:"
	@echo "  1. Configure Cursor MCP integration: make setup-cursor"
	@echo "  2. Set up Python virtual environment: see docs/setup/virtual-environment-guide.md"
	@echo "  3. Create your first project context: make new-context"
	@echo "  4. Setup intelligence collection: make setup-intelligence"
	@echo "  5. Index everything: make index"
	@echo "  6. In Cursor: @prompts/dev_agent/dev_agent_init_prompt.md"
	@echo "     QA Agent: @prompts/qa/qa_agent_init_prompt.md"
	@echo "     Red Team: @prompts/red_team/red_team_agent_init_prompt.md"
	@echo ""
	@echo "🔧 Development Setup:"
	@echo "  • make dev-setup       - Install dev dependencies + pre-commit hooks"
	@echo "  • make lint            - Run all code quality checks"
	@echo "  • make lint-fix        - Auto-fix linting issues"
	@echo "  • make format          - Format code (black + isort)"
	@echo ""
	@echo "🧠 Knowledge Architecture:"
	@echo "  • hish_framework - Static docs, guides, project contexts"
	@echo "  • cross_project_intelligence - Dynamic observations, patterns"
	@echo ""
	@echo "🚀 Indexing Options:"
	@echo "  • make index           - Full indexing (unified MPNet embeddings)"
	@echo "  • make index-code      - Code repositories only (MPNet embeddings)"
	@echo "  • make index-framework - Framework docs only (MPNet embeddings)"
	@echo "  • make index-repo      - Specific repository (unified MPNet)"
	@echo ""
	@echo "🔧 MCP Server Options:"
	@echo "  • make build-mcp       - Build MCP server image with pre-warmed model"
	@echo "  • make setup-cursor    - Build MCP image + show Cursor configuration"
	@echo ""
	@echo "💡 Cursor will auto-start services when you restart after MCP config"
	@echo "📚 All commands: make help"

setup-cursor: ## Setup Cursor MCP integration with pre-built server image
	@echo "🔌 Cursor MCP Integration Setup - Unified MPNet Embeddings"
	@echo "=========================================================="
	@echo ""
	@echo "🔧 Building MCP server image with pre-downloaded model..."
	@docker compose -f deploy/compose.rag.yml build mcp-qdrant-unified
	@echo ""
	@echo "✅ MCP server image built with pre-warmed MPNet model!"
	@echo ""
	@echo "Add this to your Cursor settings.json:"
	@echo ""
	@echo '{'
	@echo '  "mcpServers": {'
	@echo '    "qdrant-unified": {'
	@echo '      "type": "stdio",'
	@echo '      "command": "$(PWD)/scripts/run-mcp-unified.sh",'
	@echo '      "workingDirectory": "$(PWD)",'
	@echo '      "env": {'
	@echo '        "NO_COLOR": "1"'
	@echo '      }'
	@echo '    }'
	@echo '  }'
	@echo '}'
	@echo ""
	@echo "🔍 Unified Search Tools:"
	@echo "  • All Collections: Use qdrant-find with any collection (MPNet embeddings)"
	@echo "  • Better granular text understanding for both docs and code"
	@echo ""
	@echo "📖 Detailed guide: docs/setup/getting-started.md"
	@echo "🧪 Test framework: qdrant-find \"test query\" hish_framework_mpnet"
	@echo "🧪 Test code repos: qdrant-find \"function implementation\" project_code_mpnet"



build-mcp: ## Build MCP server image with pre-warmed MPNet model
	@echo "🔧 Building MCP server image with pre-downloaded MPNet model..."
	@docker compose -f deploy/compose.rag.yml build mcp-qdrant-unified
	@echo "✅ MCP server image built! Model will be ready instantly on startup."

mcp: ## Start MCP server for development
	@echo "🔌 Starting MCP server (stdio mode)..."
	docker compose -f ./deploy/compose.rag.yml run --rm -i mcp-qdrant-unified

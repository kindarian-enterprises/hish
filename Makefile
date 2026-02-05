# Hish Cursor Context Framework - Makefile
# Multi-project development agent framework with shared knowledge

# Ruff output: concise (default) or github (for CI annotations)
LINT_FORMAT ?= concise

.PHONY: help health test new-context list-contexts index-repo reindex-contexts clean logs index collections setup-cursor setup-framework setup-hooks setup-commands quick-start backup mcp build-mcp optimize-collections index-framework setup-intelligence lint lint-rag lint-sbmi lint-fix format format-rag format-sbmi type-check mypy-errors pre-commit-install dev-setup check test-sbmi test-sbmi-coverage test-sbmi-unit test-sbmi-integration sbmi-compile sbmi-compile-ci sbmi-verify sbmi-compact sbmi-compact-force sbmi-stats sbmi-analyze install-deps-sbmi install-deps-sbmi-lint context-init-portable context-link-remote context-link-local context-push context-pull context-status

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
	@./scripts/new-project-context.sh

list-contexts: ## List all project contexts
	@echo "📁 Project Contexts:"
	@if [ -L "local" ]; then \
		echo "🔗 Portable context enabled: local -> $$(readlink local)"; \
		echo ""; \
	fi
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
index: ## Index framework docs and all project documentation (host-based) - Markdown/docs only, NO code
	@echo "📚 Indexing Documentation"
	@echo "========================="
	@echo ""
	@echo "Framework docs..."
	@python3 scripts/host-indexer.py --work-dir "$(PWD)" --env-file config/env.mpnet --collection hish_framework_mpnet --recreate
	@echo ""
	@echo "Project docs..."
	@if [ -d "local" ]; then \
		for context_dir in local/*/; do \
			if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
				repo_path=$$(cat "$$context_dir/repo_path.txt" | tr -d '\n'); \
				context_name=$$(basename "$$context_dir"); \
				if [ -d "$$repo_path" ]; then \
					echo "  $$context_name: $$repo_path"; \
					python3 scripts/host-indexer.py --work-dir "$$repo_path" --env-file config/env.mpnet --collection "$${context_name}_docs_mpnet" --recreate; \
				else \
					echo "  ⚠️  Not found: $$context_name"; \
				fi; \
			fi; \
		done; \
	else \
		echo "  No projects. Run: make new-context"; \
	fi
	@echo ""
	@echo "✅ Done"

index-framework: ## Index framework docs only with MPNet embeddings - ONLY vectorized documentation, NOT learnings - RECREATES collection
	@echo "📚 Indexing framework documentation with MPNet embeddings..."
	@echo "⚠️  Framework collection will be RECREATED (replaces all data)..."
	@python3 scripts/host-indexer.py --work-dir "$(PWD)" --env-file $(or $(ENV_FILE),config/env.mpnet) --collection hish_framework_mpnet --recreate
	@echo "✅ Framework documentation indexing complete!"

setup-intelligence: ## Setup cross-project intelligence collection with MPNet embeddings - For patterns applicable to framework or 2+ projects
	@echo "🧠 Setting up cross-project intelligence collection with MPNet..."
	@EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2 INTELLIGENCE_COLLECTION_NAME=cross_project_intelligence_mpnet python3 scripts/intelligence-collection-setup.py
	@echo "✅ Intelligence collection setup complete!"

reindex-contexts: ## Reindex specific project documentation contexts (Usage: make reindex-contexts CONTEXTS="context1 context2 context3")
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
	@echo "🔄 Reindexing documentation for specified contexts: $(CONTEXTS)"
	@echo "📝 Indexing markdown/docs only - Cursor handles code natively"
	@for context_name in $(CONTEXTS); do \
		context_dir="local/$$context_name"; \
		if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
			repo_path=$$(cat "$$context_dir/repo_path.txt" | tr -d '\n'); \
			if [ -d "$$repo_path" ]; then \
				echo "📁 Reindexing $$context_name: $$repo_path"; \
				make index-repo REPO_PATH="$$repo_path" COLLECTION_NAME="$${context_name}_docs_mpnet"; \
			else \
				echo "⚠️  Repo path not found for $$context_name: $$repo_path"; \
			fi; \
		else \
			echo "❌ Context '$$context_name' not found or missing repo_path.txt"; \
		fi; \
	done
	@echo "✅ Reindexing complete for: $(CONTEXTS)"

index-repo: ## Index a specific repository documentation with MPNet embeddings (markdown/docs only)
	@if [ -z "$(REPO_PATH)" ] || [ -z "$(COLLECTION_NAME)" ]; then \
		echo "❌ Usage: make index-repo REPO_PATH=/path/to/repo COLLECTION_NAME=collection_name"; \
		exit 1; \
	fi
	@echo "📚 Host-based documentation indexing: $(REPO_PATH)"
	@echo "📁 Collection: $(COLLECTION_NAME)"
	@echo "🎯 Indexing markdown/docs only - Cursor handles code natively"
	@python3 scripts/host-indexer.py --work-dir "$(REPO_PATH)" --env-file config/env.mpnet --collection "$(COLLECTION_NAME)" --recreate
	@echo "✅ Documentation indexed successfully!"

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
dev-setup: ## Install development dependencies and pre-commit hooks (requires hish-dev venv)
	@echo "🔧 Setting up Hish development environment..."
	@echo ""
	@# Check if in virtual environment
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "❌ ERROR: No virtual environment activated!"; \
		echo ""; \
		echo "Please activate the hish-dev virtualenv:"; \
		echo "  workon hish-dev"; \
		echo ""; \
		echo "Or create it first:"; \
		echo "  mkvirtualenv hish-dev --python=python3.12"; \
		echo "  workon hish-dev"; \
		echo "  make dev-setup"; \
		echo ""; \
		exit 1; \
	fi
	@# Check if it's the hish-dev venv (optional check)
	@if echo "$$VIRTUAL_ENV" | grep -q "hish-dev"; then \
		echo "✅ Using hish-dev virtualenv: $$VIRTUAL_ENV"; \
	else \
		echo "⚠️  WARNING: Expected 'hish-dev' venv, but using: $$VIRTUAL_ENV"; \
		echo "   (continuing anyway...)"; \
	fi
	@echo ""
	@echo "📦 Installing development dependencies..."
	pip install --upgrade pip
	pip install -r requirements-dev.txt
	@echo ""
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install
	@echo ""
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "📋 Available commands:"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Check code quality"
	@echo "  make lint-fix    - Auto-fix linting issues"
	@echo "  make format      - Format code"
	@echo "  make index       - Index framework + code"
	@echo ""

test: ## Run framework tests (host-based)
	@echo "🧪 Running framework tests..."
	@echo "📋 Using host-based testing environment..."
	cd rag/indexer && python -m pytest tests/ -v

# SBMI Testing
test-sbmi: ## Run all SBMI compiler tests
	@echo "🧪 Running SBMI compiler tests..."
	cd sbmi && python3 -m pytest tests/ -v

test-sbmi-coverage: ## Run SBMI tests with coverage (CI)
	@echo "🧪 Running SBMI compiler tests with coverage..."
	cd sbmi && python3 -m pytest tests/ -v --cov=sbmi --cov-report=xml --cov-report=term-missing

test-sbmi-unit: ## Run SBMI unit tests only
	@echo "🧪 Running SBMI unit tests..."
	cd sbmi && python3 -m pytest tests/ -v -m unit

test-sbmi-integration: ## Run SBMI integration tests
	@echo "🧪 Running SBMI integration tests..."
	cd sbmi && python3 -m pytest tests/ -v -m integration

sbmi-compile: ## Compile workflow indexes to .compact format (full)
	@echo "📦 Compiling workflow indexes..."
	python3 scripts/compile-indexes.py

sbmi-compile-ci: ## Prepare local/workflow-indexes and compile (CI; no local/ required)
	@echo "📦 Preparing workflow-indexes and compiling (CI)..."
	mkdir -p local/workflow-indexes
	cp templates/workflow-indexes/*.md local/workflow-indexes/
	$(MAKE) sbmi-compile

sbmi-verify: ## Verify compiled .compact files exist and preserve essential content
	@echo "🔍 Verifying compiled files..."
	@if ! ls local/workflow-indexes/*.L*.compact 1>/dev/null 2>&1; then \
		echo "No .compact files found; running sbmi-compile-ci first..."; \
		$(MAKE) sbmi-compile-ci; \
	fi
	@for stem in framework-command-index framework-file-index framework-repository-index session-workflow-enforcement; do \
		found=0; \
		for f in local/workflow-indexes/$$stem.L*.compact; do \
			[ -f "$$f" ] && found=1 && break; \
		done; \
		[ $$found -eq 1 ] || { echo "Missing $$stem .compact"; exit 1; }; \
	done
	@cmd_idx=$$(ls local/workflow-indexes/framework-command-index.L*.compact 2>/dev/null | head -1); \
	[ -n "$$cmd_idx" ] || { echo "Missing framework-command-index .compact"; exit 1; }; \
	grep -q "make index" "$$cmd_idx" && grep -q "Makefile" "$$cmd_idx" && grep -q "dev_agent" "$$cmd_idx" && grep -q "make quick-start" "$$cmd_idx" || { echo "Essential content missing in $$cmd_idx"; exit 1; }
	@echo "✅ Compiled files verified - essential commands preserved"

sbmi-compact: ## Incrementally compact changed framework docs (session-end)
	@echo "⚡ Compacting changed framework documentation..."
	python3 scripts/compact-framework.py

sbmi-compact-force: ## Force full recompilation of all framework docs
	@echo "🔄 Force recompiling all framework documentation..."
	python3 scripts/compact-framework.py --force

sbmi-stats: ## Show SBMI compilation cache statistics
	@echo "📊 SBMI Cache Statistics:"
	python3 scripts/compact-framework.py --stats

sbmi-analyze: ## Analyze phrase frequency for compression optimization
	@echo "📊 Analyzing framework documentation phrase frequency..."
	python3 scripts/analyze-phrase-frequency.py

sbmi-validate: ## Validate SBMI expansion graph balance
	@echo "🔍 Validating SBMI expansion graph..."
	python3 scripts/validate-expansion-graph.py

sbmi-validate-verbose: ## Validate SBMI graph with verbose output
	@echo "🔍 Validating SBMI expansion graph (verbose)..."
	python3 scripts/validate-expansion-graph.py --verbose --check-balance

# Code Quality
lint: lint-rag lint-sbmi ## Run all linting checks (rag + sbmi)

lint-rag: ## Lint rag/indexer (ruff, black, isort, mypy)
	@echo "🔍 Linting rag/indexer/..."
	cd rag/indexer && ruff check . --output-format=concise
	cd rag/indexer && black --check --diff .
	cd rag/indexer && isort --check-only --diff .
	cd rag/indexer && mypy . --ignore-missing-imports || echo "⚠️ Type checking found issues (non-blocking)"
	@echo "✅ rag/indexer lint complete!"

lint-sbmi: ## Lint sbmi/ (ruff, black, isort, mypy). Set LINT_FORMAT=github for CI.
	@echo "🔍 Linting sbmi/..."
	cd sbmi && ruff check . --output-format=$(LINT_FORMAT)
	cd sbmi && black --check --diff .
	cd sbmi && isort --check-only --diff .
	cd sbmi && mypy compiler/ --ignore-missing-imports || true
	@echo "✅ sbmi lint complete!"

lint-fix: ## Fix auto-fixable linting issues (rag + sbmi)
	@echo "🔧 Fixing linting issues..."
	cd rag/indexer && ruff check . --fix && black . && isort .
	cd sbmi && ruff check . --fix && black . && isort .
	@echo "✅ Auto-fixes applied!"

format: format-rag format-sbmi ## Format all code (rag + sbmi)

format-rag: ## Format rag/indexer
	@echo "🎨 Formatting rag/indexer/..."
	cd rag/indexer && black . && isort .
	@echo "✅ rag/indexer formatted!"

format-sbmi: ## Format sbmi/
	@echo "🎨 Formatting sbmi/..."
	cd sbmi && black . && isort .
	@echo "✅ sbmi formatted!"

check: lint test test-sbmi ## Run all checks (lint + tests)

type-check: ## Run type checking with mypy (rag only)
	@echo "🔍 Running type checks..."
	cd rag/indexer && mypy . --ignore-missing-imports
	@echo "✅ Type checking complete!"

# CI / one-off installs (no venv required; use in CI or with system python)
install-deps-sbmi: ## Install SBMI runtime + test deps (for CI)
	python3 -m pip install --upgrade pip
	pip install -r sbmi/requirements.txt
	pip install -r sbmi/requirements-test.txt

install-deps-sbmi-lint: ## Install SBMI + lint tools (for CI lint job)
	python3 -m pip install --upgrade pip
	pip install -r sbmi/requirements-lint.txt
	pip install -r sbmi/requirements.txt

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
	@echo "  3. Compile framework indexes: make sbmi-compact-force"
	@echo "  4. Create your first project context: make new-context"
	@echo "  5. Setup intelligence collection: make setup-intelligence"
	@echo "  6. Index documentation: make index"
	@echo "  7. In Cursor:"
	@echo "     Dev Agent: @prompts/dev_agent/dev_agent_init_prompt.md"
	@echo "     Red Team: @prompts/red_team/red_team_agent_init_prompt.md"
	@echo ""
	@echo "🔧 Development Setup:"
	@echo "  • make dev-setup       - Install dev dependencies + pre-commit hooks"
	@echo "  • make lint            - Run all code quality checks"
	@echo "  • make lint-fix        - Auto-fix linting issues"
	@echo "  • make format          - Format code (black + isort)"
	@echo ""
	@echo "🧠 Knowledge Architecture:"
	@echo "  • hish_framework_mpnet - Framework docs, agent directives (READ-ONLY)"
	@echo "  • cross_project_intelligence - Agent-curated patterns (WRITABLE with approval)"
	@echo "  • {project}_docs_mpnet - Project documentation (markdown/AGENTS.md synopses)"
	@echo ""
	@echo "🚀 Indexing Options (Documentation Only - Cursor handles code):"
	@echo "  • make index           - Full doc indexing (framework + all project docs)"
	@echo "  • make index-framework - Framework docs only (fast)"
	@echo "  • make index-repo      - Specific repository docs"
	@echo "  • make reindex-contexts - Specific project docs"
	@echo ""
	@echo "🔧 MCP Server Options:"
	@echo "  • make build-mcp       - Build MCP server image with pre-warmed model"
	@echo "  • make setup-cursor    - Build MCP image + show Cursor configuration"
	@echo ""
	@echo "💡 Cursor will auto-start services when you restart after MCP config"
	@echo "📚 All commands: make help"

setup-hooks: ## Install Cursor hooks (collection guidance + framework protection)
	@echo "🪝 Installing Cursor Hooks"
	@echo "=========================="
	@./scripts/setup-hooks.sh

setup-commands: ## Install Cursor custom commands (agent init + session management)
	@echo "⚡ Installing Cursor Commands"
	@echo "============================="
	@./scripts/setup-commands.sh

setup-framework: ## Setup framework for agent use (compile .compact files)
	@echo "📦 Setting up framework for agent use..."
	@echo "Compiling framework documentation to .compact files..."
	@$(MAKE) sbmi-compact-force
	@echo ""
	@echo "✅ Framework setup complete!"
	@echo "   - All .md files compiled to .compact"
	@echo "   - Agents will read .compact files (token-optimized)"
	@echo "   - RAG will index .md files (full semantic search)"
	@echo ""

setup-cursor: setup-framework ## Setup Cursor MCP integration with pre-built server image + hooks + commands
	@echo "🔌 Cursor MCP Integration Setup - Unified MPNet Embeddings"
	@echo "=========================================================="
	@echo ""
	@echo "Building MCP server..."
	@docker compose -f deploy/compose.rag.yml build mcp-qdrant-unified
	@echo ""
	@./scripts/setup-hooks.sh
	@echo ""
	@./scripts/setup-commands.sh
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Add to Cursor settings.json:"
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
	@echo "Restart Cursor, then:"
	@echo "  • Type /dev to start"
	@echo "  • Use qdrant-find for docs"
	@echo "  • Use codebase_search for code"



build-mcp: ## Build MCP server image with pre-warmed MPNet model
	@echo "🔧 Building MCP server image with pre-downloaded MPNet model..."
	@docker compose -f deploy/compose.rag.yml build mcp-qdrant-unified
	@echo "✅ MCP server image built! Model will be ready instantly on startup."

mcp: ## Start MCP server for development
	@echo "🔌 Starting MCP server (stdio mode)..."
	docker compose -f ./deploy/compose.rag.yml run --rm -i mcp-qdrant-unified

# Portable Context Management
context-init-portable: ## Initialize portable context repository (OPTIONAL - for multi-environment sync)
	@echo "🔗 Initializing portable context..."
	@echo "⚠️  This is OPTIONAL. Only use if you work across multiple machines."
	@./scripts/context-init-portable.sh

context-link-remote: ## Link existing remote portable context (Usage: make context-link-remote REPO=<git-url>)
	@if [ -z "$(REPO)" ]; then \
		echo "❌ Usage: make context-link-remote REPO=<git-url>"; \
		echo "Example: make context-link-remote REPO=git@github.com:user/hish-context.git"; \
		exit 1; \
	fi
	@./scripts/context-link-remote.sh "$(REPO)"

context-link-local: ## Link existing local portable context (Usage: make context-link-local CONTEXT_PATH=<path>)
	@if [ -z "$(CONTEXT_PATH)" ]; then \
		echo "❌ Usage: make context-link-local CONTEXT_PATH=<path>"; \
		echo "Example: make context-link-local CONTEXT_PATH=~/Dropbox/hish-context"; \
		exit 1; \
	fi
	@./scripts/context-link-local.sh "$(CONTEXT_PATH)"

context-push: ## Commit and push context changes to portable repository
	@if [ ! -L "local" ]; then \
		echo "❌ Portable context not configured. Run 'make context-init-portable' first."; \
		exit 1; \
	fi
	@./scripts/context-sync.sh push

context-pull: ## Pull context changes from portable repository
	@if [ ! -L "local" ]; then \
		echo "❌ Portable context not configured. Run 'make context-init-portable' first."; \
		exit 1; \
	fi
	@./scripts/context-sync.sh pull

context-status: ## Show portable context git status
	@if [ ! -L "local" ]; then \
		echo "❌ Portable context not configured."; \
		echo ""; \
		echo "To set up portable context:"; \
		echo "  make context-init-portable    # Initialize new portable context"; \
		echo "  make context-link-remote      # Link existing remote context"; \
		echo "  make context-link-local       # Link existing local context"; \
		exit 1; \
	fi
	@./scripts/context-sync.sh status

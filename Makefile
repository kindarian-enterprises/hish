# Hish Cursor Context Framework - Makefile
# Multi-project development agent framework with shared knowledge

.PHONY: help up down status health test new-context index-repo reindex-contexts clean logs index collections search setup-cursor quick-start update backup info mcp optimize-collections

# Default target
help: ## Show this help message
	@echo "🧠 Hish Cursor Context Framework"
	@echo "====================================="
	@echo "Multi-project development agent framework with shared knowledge"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Framework Management
up: ## Start the RAG knowledge system
	@echo "🚀 Starting Hish Cursor Context framework..."
	docker compose -f compose.rag.yml --env-file env.framework up -d
	@echo "⏳ Waiting for services to be ready..."
	@sleep 10
	@make health

down: ## Stop the RAG knowledge system
	@echo "🛑 Stopping framework services..."
	docker compose -f compose.rag.yml --env-file env.framework down

status: ## Show service status
	@echo "📊 Framework Service Status:"
	docker compose -f compose.rag.yml --env-file env.framework ps

health: ## Check service health
	@echo "🏥 Health Check:"
	@echo -n "Qdrant: "
	@curl -s http://localhost:6333/health > /dev/null && echo "✅ Healthy" || echo "❌ Unhealthy"
	@echo -n "Collections: "
	@curl -s http://localhost:6333/collections | jq -r '.result.collections[] | .name' 2>/dev/null | wc -l | xargs -I {} echo "{} collections available"

logs: ## Show framework logs
	@echo "📜 Framework Logs:"
	docker compose -f compose.rag.yml --env-file env.framework logs -f

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
index: ## Index framework docs and all project code repositories (container-based)
	@echo "📚 Indexing framework documentation and local contexts..."
	@echo "🔍 Using env.framework for framework documentation (focuses on local/, docs/, contexts/)..."
	@echo "🐳 Container path mapping: $(PWD) → /work"
	docker compose -f compose.rag.yml --env-file env.framework run --rm -e COLLECTION_NAME="framework_docs" indexer python3 app.py --workdir "/work"
	@echo "🔍 Discovering project code repositories..."
	@if [ -d "local" ]; then \
		for context_dir in local/*/; do \
			if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
				repo_path=$$(cat "$$context_dir/repo_path.txt" | tr -d '\n'); \
				context_name=$$(basename "$$context_dir"); \
				if [ -d "$$repo_path" ]; then \
					echo "📁 Indexing $$context_name code: $$repo_path"; \
					make index-repo REPO_PATH="$$repo_path" COLLECTION_NAME="$${context_name}_code"; \
				else \
					echo "⚠️  Repo path not found for $$context_name: $$repo_path"; \
				fi; \
			fi; \
		done; \
	else \
		echo "ℹ️  No local contexts found. Create one with make new-context"; \
	fi
	@echo "✅ Indexing complete! Framework and all project code is now searchable."

index-host: ## Index framework docs and all project code repositories (host-based, faster)
	@echo "🚀 Host-based indexing for improved performance..."
	@echo "📚 Indexing framework documentation..."
	@python3 scripts/host-indexer.py --work-dir "$(PWD)" --env-file env.framework --collection framework_docs
	@echo "🔍 Discovering and indexing project code repositories..."
	@if [ -d "local" ]; then \
		for context_dir in local/*/; do \
			if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
				repo_path=$$(cat "$$context_dir/repo_path.txt" | tr -d '\n'); \
				context_name=$$(basename "$$context_dir"); \
				if [ -d "$$repo_path" ]; then \
					echo "📁 Host-indexing $$context_name code: $$repo_path"; \
					python3 scripts/host-indexer.py --work-dir "$$repo_path" --env-file env.code --collection "$${context_name}_code"; \
				else \
					echo "⚠️  Repo path not found for $$context_name: $$repo_path"; \
				fi; \
			fi; \
		done; \
	else \
		echo "ℹ️  No local contexts found. Create one with make new-context"; \
	fi
	@echo "✅ Host-based indexing complete! Framework and all project code is now searchable."

index-framework: ## Index framework docs only (fast reindexing for framework changes)
	@echo "📚 Indexing framework documentation only..."
	@echo "🚀 Using host-based indexing for optimal performance..."
	@python3 scripts/host-indexer.py --work-dir "$(PWD)" --env-file env.framework --collection framework_docs
	@echo "✅ Framework documentation indexing complete!"

reindex-contexts: ## Reindex specific contexts (Usage: make reindex-contexts CONTEXTS="context1 context2 context3")
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
	@for context_name in $(CONTEXTS); do \
		context_dir="local/$$context_name"; \
		if [ -d "$$context_dir" ] && [ -f "$$context_dir/repo_path.txt" ]; then \
			repo_path=$$(cat "$$context_dir/repo_path.txt" | tr -d '\n'); \
			if [ -d "$$repo_path" ]; then \
				echo "📁 Reindexing $$context_name: $$repo_path"; \
				make index-repo REPO_PATH="$$repo_path" COLLECTION_NAME="$${context_name}_code"; \
			else \
				echo "⚠️  Repo path not found for $$context_name: $$repo_path"; \
			fi; \
		else \
			echo "❌ Context '$$context_name' not found or missing repo_path.txt"; \
		fi; \
	done
	@echo "✅ Reindexing complete for: $(CONTEXTS)"

index-repo: ## Index a code repository into the knowledge base
	@if [ -z "$(REPO_PATH)" ] || [ -z "$(COLLECTION_NAME)" ]; then \
		echo "❌ Usage: make index-repo REPO_PATH=/path/to/repo COLLECTION_NAME=collection_name"; \
		exit 1; \
	fi
	@echo "📚 Indexing repository: $(REPO_PATH)"
	@echo "📁 Collection: $(COLLECTION_NAME)"
	@if [ "$(REPO_PATH)" = "." ]; then \
		echo "🔍 Using env.framework for framework documentation (focuses on local/ and docs/)..."; \
		echo "🐳 Container path mapping: $(PWD) → /work"; \
		docker compose -f compose.rag.yml --env-file env.framework run --rm -e COLLECTION_NAME="$(COLLECTION_NAME)" indexer python3 app.py --workdir "/work"; \
	else \
		echo "🔍 Using env.code for external code repository..."; \
		echo "🐳 Container path mapping: $(REPO_PATH) → /work/$$(basename $(REPO_PATH))"; \
		docker compose -f compose.rag.yml --env-file env.code run --rm -e COLLECTION_NAME="$(COLLECTION_NAME)" indexer-code python3 app.py --workdir "/work/$$(basename $(REPO_PATH))"; \
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

search: ## Search knowledge base (requires QUERY)
	@if [ -z "$(QUERY)" ]; then \
		echo "❌ Usage: make search QUERY=\"your search terms\""; \
		exit 1; \
	fi
	@echo "🔍 Searching for: $(QUERY)"
	@echo "Results will appear here when MCP tools are available..."

# Development
test: ## Run framework tests
	@echo "🧪 Running framework tests..."
	@echo "📋 Using env.framework for test configuration..."
	docker compose -f compose.rag.yml --env-file env.framework run --rm indexer-test pytest -v

clean: ## Clean up containers and volumes
	@echo "🧹 Cleaning up framework..."
	docker compose -f compose.rag.yml --env-file env.framework down -v
	docker system prune -f

# Maintenance
update: ## Update framework (git pull + rebuild)
	@echo "🔄 Updating framework..."
	git pull
	docker compose -f compose.rag.yml --env-file env.framework build --no-cache

backup: ## Backup knowledge database
	@echo "💾 Backing up knowledge database..."
	@BACKUP_FILE="hish-knowledge-backup-$$(date +%Y%m%d-%H%M%S).tar.gz"
	@tar -czf "$$BACKUP_FILE" rag/qdrant_data/ 2>/dev/null || tar -czf "$$BACKUP_FILE" .data/qdrant/ 2>/dev/null || echo "❌ No data directory found"
	@echo "✅ Backup created: $$BACKUP_FILE"

# Quick Actions
quick-start: ## Quick setup guide - show configuration steps
	@echo "🚀 Hish Cursor Context - Quick Start"
	@echo "========================================"
	@echo ""
	@echo "📋 Setup Steps:"
	@echo "  1. Configure Cursor MCP integration: make setup-cursor"
	@echo "  2. Create your first project context: make new-context"
	@echo "  3. Index everything: make index-host (faster) or make index (container-based)"
	@echo "  4. In Cursor: @dev_agent_init_prompt.md"
	@echo ""
	@echo "🚀 Performance Options:"
	@echo "  • make index-host      - Host-based indexing (faster, recommended)"
	@echo "  • make index           - Container-based indexing (original method)"
	@echo "  • make index-framework - Framework docs only (quick updates)"
	@echo ""
	@echo "💡 Cursor will auto-start Qdrant when you restart after MCP config"
	@echo "📚 All commands: make help"

setup-cursor: ## Show Cursor MCP configuration instructions
	@echo "🔌 Cursor MCP Integration Setup"
	@echo "=============================="
	@echo ""
	@echo "Add this to your Cursor settings.json:"
	@echo ""
	@echo '{'
	@echo '  "mcpServers": {'
	@echo '    "qdrant": {'
	@echo '      "type": "stdio",'
	@echo '      "command": "$(PWD)/scripts/run-mcp-llamaindex.sh",'
	@echo '      "workingDirectory": "$(PWD)",'
	@echo '      "env": {'
	@echo '        "NO_COLOR": "1"'
	@echo '      }'
	@echo '    }'
	@echo '  }'
	@echo '}'
	@echo ""
	@echo "📖 Detailed guide: docs/setup/cursor-mcp-integration.md"
	@echo "🧪 Test with: qdrant-find \"test query\" in Cursor chat"

# Information
info: ## Show framework information
	@echo "🧠 Hish Cursor Context Framework"
	@echo "======================================"
	@echo "Version: Multi-Project Intelligence Edition"
	@echo "Purpose: Cross-project knowledge sharing for development agents"
	@echo ""
	@echo "🏗️  Architecture:"
	@echo "  • Context Management: hish/ (this repo)"
	@echo "  • Code Repositories: External (indexed by RAG)"
	@echo "  • Knowledge Base: Qdrant vector database"
	@echo "  • Agent Interface: Cursor + MCP protocol"
	@echo ""
	@echo "📊 Current Status:"
	@make health
	@echo ""
	@echo "📁 Project Contexts:"
	@make list-contexts

mcp: ## Start MCP server for development  
	@echo "🔌 Starting MCP server (stdio mode)..."
	docker compose -f compose.rag.yml --env-file env.mcp run --rm -i mcp-qdrant-llamaindex


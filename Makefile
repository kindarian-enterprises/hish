# Kindarian Cursor Context Framework - Makefile
# Multi-project development agent framework with shared knowledge

.PHONY: help up down status health test new-context index-repo clean logs index collections search setup-cursor quick-start update backup info mcp

# Default target
help: ## Show this help message
	@echo "🧠 Kindarian Cursor Context Framework"
	@echo "====================================="
	@echo "Multi-project development agent framework with shared knowledge"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Framework Management
up: ## Start the RAG knowledge system
	@echo "🚀 Starting Kindarian Cursor Context framework..."
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
index: ## Index framework docs and all project code repositories
	@echo "📚 Indexing framework documentation and local contexts..."
	make index-repo REPO_PATH=. COLLECTION_NAME=framework_docs
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

index-repo: ## Index a code repository into the knowledge base
	@if [ -z "$(REPO_PATH)" ] || [ -z "$(COLLECTION_NAME)" ]; then \
		echo "❌ Usage: make index-repo REPO_PATH=/path/to/repo COLLECTION_NAME=collection_name"; \
		exit 1; \
	fi
	@echo "📚 Indexing repository: $(REPO_PATH)"
	@echo "📁 Collection: $(COLLECTION_NAME)"
	@echo "🔍 Using env.framework for indexing configuration..."
	docker compose -f compose.rag.yml --env-file env.framework run --rm indexer python3 app.py index "$(REPO_PATH)" --collection "$(COLLECTION_NAME)"

collections: ## List all knowledge collections
	@echo "🗂️  Knowledge Collections:"
	@curl -s http://localhost:6333/collections | jq -r '.result.collections[] | "  📚 \(.name) - \(.points_count) chunks"' 2>/dev/null || echo "❌ Could not connect to Qdrant"

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
	@BACKUP_FILE="kindarian-knowledge-backup-$$(date +%Y%m%d-%H%M%S).tar.gz"
	@tar -czf "$$BACKUP_FILE" rag/qdrant_data/ 2>/dev/null || tar -czf "$$BACKUP_FILE" .data/qdrant/ 2>/dev/null || echo "❌ No data directory found"
	@echo "✅ Backup created: $$BACKUP_FILE"

# Quick Actions
quick-start: up ## Quick start: launch framework and show next steps
	@echo ""
	@echo "🎉 Framework is ready! Next steps:"
	@echo "  1. Configure Cursor MCP integration: make setup-cursor"
	@echo "  2. Create your first project context: make new-context"
	@echo "  3. Index your code repositories: make index"
	@echo "  4. In Cursor: @dev_agent_init_prompt.md"
	@echo ""
	@echo "📚 Available commands: make help"

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
	@echo '      "command": "$(PWD)/scripts/run-mcp-stdio.sh",'
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
	@echo "🧠 Kindarian Cursor Context Framework"
	@echo "======================================"
	@echo "Version: Multi-Project Intelligence Edition"
	@echo "Purpose: Cross-project knowledge sharing for development agents"
	@echo ""
	@echo "🏗️  Architecture:"
	@echo "  • Context Management: kindarian-cursor-context/ (this repo)"
	@echo "  • Code Repositories: External (indexed by RAG)"
	@echo "  • Knowledge Base: Qdrant vector database"
	@echo "  • Agent Interface: Cursor + MCP protocol"
	@echo ""
	@echo "📊 Current Status:"
	@make health
	@echo ""
	@echo "📁 Project Contexts:"
	@make list-contexts

# Development helpers
mcp: ## Start MCP server for development
	@echo "🔌 Starting MCP server (stdio mode)..."
	docker compose -f compose.rag.yml --env-file env.framework run --rm -i mcp-qdrant-stdio
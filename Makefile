# Kindarian Cursor Context - Development Makefile
# Provides common commands for RAG knowledge system and project setup

.PHONY: help setup up down clean index test health status logs

# Default target
help: ## Show this help message
	@echo "Kindarian Cursor Context - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================================================
# RAG SYSTEM MANAGEMENT
# ============================================================================

setup: ## Set up RAG infrastructure and dependencies
	@echo "Setting up RAG infrastructure..."
	@if [ ! -f "compose.rag.yml" ]; then echo "Error: compose.rag.yml not found. Copy RAG infrastructure first."; exit 1; fi
	@docker-compose -f compose.rag.yml pull
	@echo "RAG infrastructure ready"

up: ## Start RAG services (Qdrant vector database)
	@echo "Starting RAG services..."
	@docker-compose -f compose.rag.yml up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	@$(MAKE) health

down: ## Stop RAG services
	@echo "Stopping RAG services..."
	@docker-compose -f compose.rag.yml down

restart: ## Restart RAG services
	@$(MAKE) down
	@$(MAKE) up

clean: ## Stop services and remove volumes (WARNING: deletes all data)
	@echo "WARNING: This will delete all indexed data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@docker-compose -f compose.rag.yml down -v
	@docker system prune -f

# ============================================================================
# KNOWLEDGE INDEXING
# ============================================================================

index: ## Index current project codebase
	@echo "Indexing current project..."
	@if [ ! -d "rag/indexer" ]; then echo "Error: RAG indexer not found. Copy RAG infrastructure first."; exit 1; fi
	@cd rag/indexer && python app.py index . --collection project_code --extensions .py .md .txt .js .ts .yml .yaml

index-docs: ## Index documentation only
	@echo "Indexing documentation..."
	@cd rag/indexer && python app.py index ./docs --collection project_docs --extensions .md .txt

index-external: ## Index external directory (usage: make index-external DIR=/path/to/dir)
	@if [ -z "$(DIR)" ]; then echo "Usage: make index-external DIR=/path/to/directory"; exit 1; fi
	@echo "Indexing external directory: $(DIR)"
	@cd rag/indexer && python app.py index $(DIR) --collection external_code

reindex: ## Clear and rebuild all indices
	@echo "Rebuilding all indices..."
	@cd rag/indexer && python app.py clear-collection project_code
	@cd rag/indexer && python app.py clear-collection project_docs
	@$(MAKE) index
	@$(MAKE) index-docs

# ============================================================================
# SYSTEM MONITORING
# ============================================================================

health: ## Check health of RAG services
	@echo "Checking RAG service health..."
	@curl -s http://localhost:6333/health || echo "Qdrant not responding"
	@curl -s http://localhost:6333/collections || echo "Collections endpoint not available"

status: ## Show status of all services
	@echo "RAG Service Status:"
	@echo "==================="
	@docker-compose -f compose.rag.yml ps

logs: ## Show logs from RAG services
	@docker-compose -f compose.rag.yml logs -f

logs-qdrant: ## Show Qdrant logs only
	@docker-compose -f compose.rag.yml logs -f qdrant

# ============================================================================
# DEVELOPMENT UTILITIES
# ============================================================================

shell-qdrant: ## Open shell in Qdrant container
	@docker-compose -f compose.rag.yml exec qdrant /bin/bash

backup: ## Backup Qdrant data
	@echo "Creating backup..."
	@mkdir -p backups
	@docker-compose -f compose.rag.yml exec qdrant tar czf /tmp/qdrant-backup-$$(date +%Y%m%d-%H%M%S).tar.gz /qdrant/storage
	@docker cp $$(docker-compose -f compose.rag.yml ps -q qdrant):/tmp/qdrant-backup-*.tar.gz ./backups/
	@echo "Backup created in ./backups/"

restore: ## Restore from backup (usage: make restore BACKUP=filename.tar.gz)
	@if [ -z "$(BACKUP)" ]; then echo "Usage: make restore BACKUP=filename.tar.gz"; exit 1; fi
	@echo "Restoring from backup: $(BACKUP)"
	@$(MAKE) down
	@docker volume rm kindarian-cursor-context_qdrant_storage || true
	@$(MAKE) up
	@sleep 5
	@docker cp ./backups/$(BACKUP) $$(docker-compose -f compose.rag.yml ps -q qdrant):/tmp/restore.tar.gz
	@docker-compose -f compose.rag.yml exec qdrant tar xzf /tmp/restore.tar.gz -C /
	@$(MAKE) restart

# ============================================================================
# PROJECT SETUP
# ============================================================================

init-project: ## Initialize a new project with templates (usage: make init-project NAME=myproject)
	@if [ -z "$(NAME)" ]; then echo "Usage: make init-project NAME=myproject"; exit 1; fi
	@echo "Initializing new project: $(NAME)"
	@./scripts/setup-new-project.sh

copy-templates: ## Copy templates to current directory
	@echo "Copying templates to current directory..."
	@cp templates/persona/dev_agent_persona_template.md ./dev_agent_persona.md
	@cp templates/context/dev_agent_context_template.md ./dev_agent_context.md
	@cp templates/prompts/dev_agent_init_prompt_template.md ./dev_agent_init_prompt.md
	@cp templates/prompts/dev_agent_session_end_prompt_template.md ./dev_agent_session_end_prompt.md
	@echo "Templates copied. Customize them for your project."

copy-rag: ## Copy RAG infrastructure to current directory
	@echo "Copying RAG infrastructure..."
	@cp -r rag ./
	@cp -r mcp ./
	@cp compose.rag.yml ./
	@echo "RAG infrastructure copied. Run 'make setup' to initialize."

# ============================================================================
# TESTING & VALIDATION
# ============================================================================

test-connection: ## Test connection to RAG services
	@echo "Testing RAG service connections..."
	@curl -f http://localhost:6333/health && echo "✓ Qdrant health check passed" || echo "✗ Qdrant health check failed"
	@curl -f http://localhost:6333/collections && echo "✓ Qdrant collections endpoint accessible" || echo "✗ Qdrant collections endpoint failed"

test-index: ## Test indexing with sample data
	@echo "Testing indexing with sample data..."
	@cd rag/indexer && echo "This is a test document for indexing" > test.txt
	@cd rag/indexer && python app.py index . --collection test_collection --extensions .txt
	@cd rag/indexer && rm test.txt
	@echo "Test indexing completed"

test-search: ## Test search functionality
	@echo "Testing search functionality..."
	@cd rag/indexer && python -c "from app import search_documents; print(search_documents('test', 'test_collection', limit=1))"

# ============================================================================
# MAINTENANCE
# ============================================================================

update: ## Update RAG infrastructure
	@echo "Updating RAG infrastructure..."
	@docker-compose -f compose.rag.yml pull
	@$(MAKE) restart

optimize: ## Optimize Qdrant database
	@echo "Optimizing Qdrant database..."
	@curl -X POST http://localhost:6333/collections/project_code/index
	@curl -X POST http://localhost:6333/collections/project_docs/index

stats: ## Show database statistics
	@echo "Qdrant Database Statistics:"
	@echo "=========================="
	@curl -s http://localhost:6333/collections | jq '.result.collections[] | {name: .name, points_count: .points_count, vectors_count: .vectors_count}'

# ============================================================================
# DOCUMENTATION
# ============================================================================

docs: ## Open documentation in browser
	@echo "Opening documentation..."
	@if command -v xdg-open >/dev/null 2>&1; then xdg-open docs/; elif command -v open >/dev/null 2>&1; then open docs/; else echo "Please open docs/ directory manually"; fi

readme: ## Show README
	@cat README.md

# ============================================================================
# ENVIRONMENT HELPERS
# ============================================================================

env-check: ## Check if required environment variables are set
	@echo "Checking environment configuration..."
	@echo "QDRANT_HOST: $${QDRANT_HOST:-localhost}"
	@echo "QDRANT_PORT: $${QDRANT_PORT:-6333}"
	@echo "EMBEDDING_MODEL: $${EMBEDDING_MODEL:-all-MiniLM-L6-v2}"

env-example: ## Copy environment example files
	@if [ -f "templates/config/.env.example" ]; then cp templates/config/.env.example .env.example; echo "Environment example copied to .env.example"; fi
	@if [ -f "templates/config/.env.rag" ]; then cp templates/config/.env.rag .env.rag.example; echo "RAG environment example copied to .env.rag.example"; fi

# ============================================================================
# QUICK COMMANDS
# ============================================================================

quick-start: ## Quick start: setup + start services + index current directory
	@$(MAKE) setup
	@$(MAKE) up
	@sleep 15
	@$(MAKE) index
	@echo ""
	@echo "🎉 Quick start complete!"
	@echo "Your project is now indexed and ready for RAG queries."
	@echo ""
	@echo "Try these commands:"
	@echo "  make test-search    # Test search functionality"
	@echo "  make health         # Check service health"
	@echo "  make stats          # View database statistics"

dev: ## Development mode: start services and show logs
	@$(MAKE) up
	@$(MAKE) logs

stop: ## Alias for 'down'
	@$(MAKE) down

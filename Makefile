# PAL-adin Makefile
.PHONY: help install dev build test lint format clean docker-up docker-down docker-build

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)PAL-adin Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "$(BLUE)Installing backend dependencies...$(NC)"
	cd backend && pip install -r requirements.txt
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	cd frontend && npm install
	@echo "$(GREEN)✓ All dependencies installed$(NC)"

dev: ## Start development servers
	@echo "$(BLUE)Starting development environment...$(NC)"
	docker-compose up -d postgres keydb qdrant minio ollama
	@echo "$(GREEN)✓ Services started$(NC)"
	@echo "$(BLUE)Backend: http://localhost:8000$(NC)"
	@echo "$(BLUE)Frontend: http://localhost:3000$(NC)"

build: ## Build all containers
	@echo "$(BLUE)Building Docker containers...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Build complete$(NC)"

test: ## Run all tests
	@echo "$(BLUE)Running backend tests...$(NC)"
	cd backend && pytest
	@echo "$(BLUE)Running frontend tests...$(NC)"
	cd frontend && npm test
	@echo "$(GREEN)✓ All tests passed$(NC)"

test-coverage: ## Run tests with coverage
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	cd backend && pytest --cov=app --cov-report=html
	cd frontend && npm run test:coverage
	@echo "$(GREEN)✓ Coverage reports generated$(NC)"

lint: ## Lint all code
	@echo "$(BLUE)Linting backend...$(NC)"
	cd backend && black --check . && isort --check . && flake8
	@echo "$(BLUE)Linting frontend...$(NC)"
	cd frontend && npm run lint
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format all code
	@echo "$(BLUE)Formatting backend...$(NC)"
	cd backend && black . && isort .
	@echo "$(BLUE)Formatting frontend...$(NC)"
	cd frontend && npm run format
	@echo "$(GREEN)✓ Formatting complete$(NC)"

clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name ".svelte-kit" -exec rm -rf {} +
	@echo "$(GREEN)✓ Cleaned$(NC)"

docker-up: ## Start all Docker services
	@echo "$(BLUE)Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started$(NC)"

docker-down: ## Stop all Docker services
	@echo "$(BLUE)Stopping Docker services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

docker-build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build --no-cache
	@echo "$(GREEN)✓ Images built$(NC)"

docker-logs: ## Show Docker logs
	docker-compose logs -f

db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	cd backend && alembic upgrade head
	@echo "$(GREEN)✓ Migrations complete$(NC)"

db-reset: ## Reset database (WARNING: deletes all data)
	@echo "$(RED)⚠ WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d postgres; \
		sleep 5; \
		cd backend && alembic upgrade head; \
		echo "$(GREEN)✓ Database reset$(NC)"; \
	fi

setup: ## Initial setup for development
	@echo "$(BLUE)Setting up PAL-adin development environment...$(NC)"
	cp .env.example .env
	@echo "$(GREEN)✓ Created .env file - please update with your settings$(NC)"
	$(MAKE) install
	$(MAKE) docker-up
	sleep 10
	$(MAKE) db-migrate
	@echo "$(GREEN)✓ Setup complete!$(NC)"

monitor: ## Open monitoring dashboards
	@echo "$(BLUE)Opening monitoring dashboards...$(NC)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3001 (admin/admin)"
	@echo "MinIO Console: http://localhost:9001"

check-health: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(NC)"
	@curl -f http://localhost:8000/health && echo "$(GREEN)✓ Backend healthy$(NC)" || echo "$(RED)✗ Backend unhealthy$(NC)"
	@curl -f http://localhost:3000/health && echo "$(GREEN)✓ Frontend healthy$(NC)" || echo "$(RED)✗ Frontend unhealthy$(NC)"
	@docker-compose ps

.DEFAULT_GOAL := help

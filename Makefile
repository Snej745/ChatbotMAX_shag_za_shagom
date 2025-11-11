.PHONY: help build up down restart logs shell clean test

# Цвета для вывода
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m # No Color

help: ## Показать помощь
	@echo "$(GREEN)MAX Dependency Counseling Bot - Docker Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

build: ## Собрать Docker образ
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker-compose build

up: ## Запустить бота
	@echo "$(GREEN)Starting bot...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Bot started! Check logs with 'make logs'$(NC)"

down: ## Остановить бота
	@echo "$(YELLOW)Stopping bot...$(NC)"
	docker-compose down

restart: ## Перезапустить бота
	@echo "$(YELLOW)Restarting bot...$(NC)"
	docker-compose restart

logs: ## Показать логи (Ctrl+C для выхода)
	docker-compose logs -f maxbot

logs-tail: ## Показать последние 100 строк логов
	docker-compose logs --tail=100 maxbot

status: ## Показать статус контейнера
	@echo "$(GREEN)Container status:$(NC)"
	docker-compose ps
	@echo ""
	@echo "$(GREEN)Resource usage:$(NC)"
	docker stats max-dependency-bot --no-stream

shell: ## Зайти в контейнер
	docker-compose exec maxbot /bin/bash

rebuild: ## Пересобрать образ без кэша
	@echo "$(YELLOW)Rebuilding without cache...$(NC)"
	docker-compose build --no-cache
	docker-compose up -d

clean: ## Удалить контейнер и образ
	@echo "$(RED)Cleaning up...$(NC)"
	docker-compose down -v
	docker rmi maxbot:latest || true

clean-all: ## Полная очистка Docker
	@echo "$(RED)WARNING: This will remove all unused Docker resources!$(NC)"
	@read -p "Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker system prune -a --volumes; \
	fi

deploy: build up ## Собрать и запустить (полное развертывание)
	@echo "$(GREEN)Deployment complete!$(NC)"

update: ## Обновить код и перезапустить
	@echo "$(GREEN)Updating...$(NC)"
	git pull
	docker-compose build
	docker-compose up -d
	@echo "$(GREEN)Update complete!$(NC)"

check-env: ## Проверить .env файл
	@if [ -f .env ]; then \
		echo "$(GREEN).env file found$(NC)"; \
		echo "$(YELLOW)BOT_TOKEN:$(NC) $$(grep BOT_TOKEN .env | cut -d'=' -f2 | head -c 20)..."; \
	else \
		echo "$(RED).env file not found!$(NC)"; \
		exit 1; \
	fi

test: ## Проверить образ
	@echo "$(GREEN)Testing Docker image...$(NC)"
	docker run --rm maxbot:latest python -c "import bot; print('✅ Import test passed')"

health: ## Проверить healthcheck
	@docker inspect --format='{{json .State.Health}}' max-dependency-bot | python -m json.tool

info: ## Показать информацию об образе
	@echo "$(GREEN)Image information:$(NC)"
	docker images maxbot:latest
	@echo ""
	@echo "$(GREEN)Container information:$(NC)"
	docker inspect max-dependency-bot | grep -E '"Status"|"Running"|"Pid"'

# Алиасы для Windows пользователей
start: up
stop: down

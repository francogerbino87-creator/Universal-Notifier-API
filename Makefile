# Makefile para Universal Notifier API

# Variables
DOCKER_COMPOSE = docker-compose
PYTHON = python
PIP = pip

.PHONY: help build up down logs restart test clean

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@echo "  make build     - Construir imágenes Docker"
	@echo "  make up        - Iniciar servicios"
	@echo "  make down      - Detener servicios"
	@echo "  make logs      - Ver logs de la API"
	@echo "  make restart   - Reiniciar servicios"
	@echo "  make clean     - Limpiar contenedores y volúmenes"
	@echo "  make debug     - Iniciar con MongoDB Express"

build: ## Construir imágenes Docker
	$(DOCKER_COMPOSE) build

up: ## Iniciar servicios
	$(DOCKER_COMPOSE) up -d

down: ## Detener servicios
	$(DOCKER_COMPOSE) down

logs: ## Ver logs de la API
	$(DOCKER_COMPOSE) logs -f api

restart: ## Reiniciar servicios
	$(DOCKER_COMPOSE) restart

clean: ## Limpiar contenedores y volúmenes
	$(DOCKER_COMPOSE) down -v
	@echo "Limpieza completada"

debug: ## Iniciar con MongoDB Express (UI)
	$(DOCKER_COMPOSE) --profile debug up -d

status: ## Ver estado de los servicios
	$(DOCKER_COMPOSE) ps

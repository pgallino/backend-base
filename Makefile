# Makefile reorganizado y minimalista
# Objetivo: dejar comandos claros y pocos atajos para desarrollo y deploy.

# Variables
PYTHON_FILES = src

default: help

.PHONY: help dev-up dev-down dev-build dev-shell api cli dev-cli dev-api format format-check lint test test-unit test-acceptance migrate prod-build prod-run prod-stop ci

# Ayuda: lista los comandos recomendados
help:
	@echo "Comandos principales:"
	@echo "  Flujo recomendado:"
	@echo "    1) Levanta el entorno fuera del contenedor:"
	@echo "       docker compose -f docker-compose.dev.yml up -d --build"
	@echo "    2) Entra al contenedor o ejecuta make dentro del contenedor:"
	@echo "       docker compose -f docker-compose.dev.yml exec dev sh"
	@echo "       make api  # o make cli, make migrate, etc."
	@echo "  make api           # Inicia la API (uvicorn) — pensado para ejecutarse dentro del contenedor dev (backend service)"
	@echo "  make cli CLI_ARGS=\"...\"  # Ejecuta la CLI — pensado para ejecutarse dentro del contenedor dev"
	@echo "  make migrate       # Ejecuta migraciones — pensado para ejecutarse dentro del contenedor dev"
	@echo "  make format        # Formatea el código (black/isort)"
	@echo "  make test          # Ejecuta tests (unit + acceptance)"
	@echo "  make prod-build    # Construye imagen de producción"
	@echo "  make prod-run      # Ejecuta imagen de producción (usa .env)"
	@echo "  make ci            # Ejecuta checks y tests (útil en CI)"
	@echo "\n(Nota: hay targets host-level como dev-up/dev-down que pueden usarse opcionalmente.)"

# -----------------------------
# Development: build / compose helpers
# -----------------------------

# Build development image (Dockerfile.dev)
dev-build:
	docker build -t backend-base:dev -f Dockerfile.dev .

# Bring up a development compose environment (services sleep; use exec to run)
dev-up: dev-build
	@echo "-> Levantando entorno de desarrollo"
	docker compose -f docker-compose.dev.yml up -d --build

dev-down:
	@echo "-> Bajando entorno de desarrollo"
	docker compose -f docker-compose.dev.yml down

# Open shell in dev container (requires dev-up)
dev-shell:
	@echo "-> Abre una shell en el contenedor de desarrollo desde el host:"
	@echo "   docker compose -f docker-compose.dev.yml exec dev sh"
	@echo "   (Este target no asume responsabilidad de levantar el container)"

# Start the API inside the dev container (runs uvicorn inside the running container)
api:
	@echo "-> Iniciando API (uvicorn). Ejecuta esto dentro del contenedor dev."
	uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# Run CLI inside dev container. Usage: make cli CLI_ARGS="tools list"
	@echo "-> Ejecutando CLI (Typer). Ejecuta esto dentro del contenedor dev."
	python -m src.cli_app $(CLI_ARGS)

# Compatibility: keep older dev-cli/dev-api targets (alias)
dev-cli: cli

dev-api: api

# -----------------------------
# Formatting / linting / tests
# -----------------------------

format:
	@echo "-> Formateando código con black e isort..."
	isort $(PYTHON_FILES)
	black $(PYTHON_FILES)

format-check:
	@echo "-> Verificando formato..."
	isort --check-only $(PYTHON_FILES)
	black --check $(PYTHON_FILES)

lint:
	@echo "-> Chequeo de tipos (mypy)..."
	mypy $(PYTHON_FILES)

# Tests
test: test-unit test-acceptance
	@echo "-> Tests completos ejecutados"

test-unit:
	@echo "-> Ejecutando tests unitarios..."
	pytest --cov=src/domain --cov=src/adapters/db/repositories --cov-report=term-missing --cov-report=xml:coverage-unit.xml --cov-fail-under=75 tests/domain tests/adapters/db

test-acceptance:
	@echo "-> Ejecutando tests de aceptación (BDD)..."
	pytest tests/acceptance

# -----------------------------
# Migrations
# -----------------------------

# Run alembic commands locally (host) or use the container via dev-up
alembic-init:
	PYTHONPATH=$(shell pwd) alembic init alembic

alembic-migrate:
	PYTHONPATH=$(shell pwd) alembic revision --autogenerate -m "Nueva migracion"

# Upgrade DB schema (host)
alembic-upgrade:
	PYTHONPATH=$(shell pwd) alembic upgrade head

# Shortcut: run migrations inside dev container (recommended for dev)
migrate:
	@echo "-> Ejecutando migraciones (dentro del contenedor dev)"
	PYTHONPATH=$(shell pwd) alembic upgrade head

# -----------------------------
# Production image helpers
# -----------------------------

prod-build:
	docker build -t backend-base:prod -f Dockerfile.prod .

prod-run: prod-build
	@echo "-> Ejecutando imagen de producción (backend-base:prod)"
	docker run --rm -d --name backend-prod -p 8000:8000 --env-file .env backend-base:prod

prod-stop:
	-docker stop backend-prod || true

# -----------------------------
# CI convenience
# -----------------------------

ci: format-check lint test
	@echo "✅ CI OK"



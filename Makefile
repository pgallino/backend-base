# Variable que apunta a nuestra carpeta de código fuente
PYTHON_FILES = src

# Coverage targets for acceptance tests (default focuses on the routes/controllers
# and on repository implementations). You can override when calling make, e.g.
# `make test-acceptance ACCEPTANCE_COV_DIRS="src"`
ACCEPTANCE_COV_DIRS ?= src/adapters/api/routes src/adapters/db/repositories

# Build pytest --cov flags from the list of dirs in ACCEPTANCE_COV_DIRS
COVER_FLAGS := $(foreach d,$(ACCEPTANCE_COV_DIRS),--cov=$(d))

.PHONY: up down shell run format format-check check test test-unit test-acceptance ci

# --- Comandos para el Host (tu máquina) ---

# Levanta el servicio de Docker en segundo plano
up:
	docker compose up -d --build

# Detiene y elimina el servicio
down:
	docker compose down

# El comando principal para empezar a trabajar: levanta y entra a la shell
shell: up
	@echo "-> Ingresando a la shell del contenedor..."
	@echo "   (Una vez dentro, usa 'make run' o 'make format, etc')"
	@echo "----------------------------------------------------------------------"
	docker compose exec backend sh



# --- Migraciones Alembic ---

PYTHONPATH_VAR=PYTHONPATH=$(shell python -c "import os; print(os.getcwd())")

alembic-init:
	$(PYTHONPATH_VAR) alembic init alembic

alembic-migrate:
	$(PYTHONPATH_VAR) alembic revision --autogenerate -m "Nueva migracion"

alembic-upgrade:
	$(PYTHONPATH_VAR) alembic upgrade head

alembic-downgrade:
	$(PYTHONPATH_VAR) alembic downgrade -1

# --- Comandos para el Contenedor (dentro de la shell) ---

# Inicia el servidor FastAPI con recarga automática
run:
	@echo "-> Iniciando servidor en http://localhost:8000"
	uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# Aplica formato al código (corrige los archivos)
format:
	@echo "-> Formateando código con black e isort..."
	isort $(PYTHON_FILES)
	black $(PYTHON_FILES)

# Verifica si el formato es correcto (no corrige, solo avisa)
format-check:
	@echo "-> Verificando formato..."
	isort --check-only $(PYTHON_FILES)
	black --check $(PYTHON_FILES)

# Chequeo de Tipos Estáticos (Linting con Mypy)
lint:
	@echo "-> Corriendo chequeo de tipos (Mypy)..."
	mypy $(PYTHON_FILES)

# Ejecuta tanto format-check como lint
check:
	@echo "-> Ejecutando verificaciones completas..."
	$(MAKE) format-check
	$(MAKE) lint

# Ejecuta tests unitarios y aceptacion con pytest

test:
	@echo "-> Ejecutando tests: unitarios y de aceptación con umbrales separados..."
	$(MAKE) test-unit
	$(MAKE) test-acceptance

# Tests unitarios solamente
test-unit:
	@echo "-> Ejecutando tests UNITARIOS (coverage sobre src/domain, fail-under=75)..."
	pytest --cov=src/domain --cov-report=term-missing --cov-report=xml:coverage-unit.xml --cov-fail-under=75 tests/domain

# Tests de aceptación (BDD) solamente
test-acceptance:
	@echo "-> Ejecutando tests de ACEPTACIÓN (BDD) (coverage sobre: $(ACCEPTANCE_COV_DIRS))"
	# Medimos cobertura de la capa de API / rutas y de los repositorios para validar
	# que los features persisten correctamente. Puedes sobrescribir
	# ACCEPTANCE_COV_DIRS al invocar make si quieres otro scope.
	pytest $(COVER_FLAGS) --cov-report=term-missing --cov-report=xml:coverage-acceptance.xml --cov-fail-under=60 tests/acceptance

# Objetivo de CI: calidad + tests
ci:
	@echo "-> Ejecutando CI local (check + test)..."
	$(MAKE) check
	$(MAKE) test
	@echo "✅ CI OK: formato, tipos y tests pasaron."

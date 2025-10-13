# Variable que apunta a nuestra carpeta de código fuente
PYTHON_FILES = src

.PHONY: up down shell run format format-check check

# --- Comandos para el Host (tu máquina) ---

# Levanta el servicio de Docker en segundo plano
up:
	docker-compose up -d --build

# Detiene y elimina el servicio
down:
	docker-compose down

# El comando principal para empezar a trabajar: levanta y entra a la shell
shell: up
	@echo "-> Ingresando a la shell del contenedor..."
	@echo "   (Una vez dentro, usa 'make run' o 'make format')"
	@echo "----------------------------------------------------------------------"
	docker exec -it backend-backend-1 /bin/bash


# --- Comandos para el Contenedor (dentro de la shell) ---

# Inicia el servidor FastAPI con recarga automática
run:
	@echo "-> Iniciando servidor en http://localhost:8000"
	uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# Aplica formato al código (corrige los archivos)
format:
	@echo "-> Formateando código con black e isort..."
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)

# Verifica si el formato es correcto (no corrige, solo avisa)
format-check:
	@echo "-> Verificando formato..."
	black --check $(PYTHON_FILES)
	isort --check-only $(PYTHON_FILES)

# Chequeo de Tipos Estáticos (Linting con Mypy)
lint:
	@echo "-> Corriendo chequeo de tipos (Mypy)..."
	mypy $(PYTHON_FILES)

# Ejecuta tanto format-check como lint
check:
	@echo "-> Ejecutando verificaciones completas..."
	$(MAKE) format-check
	$(MAKE) lint
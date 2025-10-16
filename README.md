# Backend Base

Plantilla base para construir APIs REST con FastAPI usando Arquitectura Hexagonal (Ports & Adapters). A continuación encontrarás explicación de las tecnologías, guía de desarrollo, arquitectura de la fachada, tests, comandos Make, Docker, CI/CD y recomendaciones sobre secrets.

## Tabla de contenidos

- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tecnologias y herramientas](#tecnologias-y-herramientas)
- [Como desarrollar](#como-desarrollar)
- [Arquitectura - Fachada](#arquitectura---fachada)
- [Tests](#tests)
- [Makefile](#makefile)
- [Docker](#docker)
- [CI/CD y deploy automatico](#cicd-y-deploy-automatico)
- [.env / .env.example](#env--envexample)
- [Recomendaciones y proximos pasos](#recomendaciones-y-proximos-pasos)

## Arquitectura

Este proyecto implementa **Arquitectura Hexagonal** (también conocida como Ports & Adapters), que separa la lógica de negocio de los detalles de infraestructura.

### Capas de la Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    ADAPTADORES DE ENTRADA                   │
│              (API Routes, CLI, Web UI, etc.)               │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   FACHADA DE APLICACIÓN                    │
│            (Orquestación y Coordinación)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                      DOMINIO                               │
│              (Lógica de Negocio Pura)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  ADAPTADORES DE SALIDA                     │
│              (DB, APIs Externas, etc.)                     │
└─────────────────────────────────────────────────────────────┘
```

### Componentes Principales

#### 1. **Adaptadores de Entrada** (`src/adapters/api/`)
- **Responsabilidad**: Reciben requests externos y los adaptan al dominio
- **Rutas HTTP**: Cada endpoint está en su propio archivo en `routes/`
- **Sin lógica de negocio**: Solo validación de entrada y formateo de respuesta

#### 2. **Fachada de Aplicación** (`src/adapters/api/facade.py`)
- **Responsabilidad**: Punto de entrada único para todos los adaptadores
- **Orquestación**: Coordina llamadas entre dominio y adaptadores de salida
- **Manejo de dependencias**: Inyecta configuración e infraestructura al dominio

#### 3. **Dominio** (`src/domain/`)
- **Lógica de negocio pura**: Sin dependencias de infraestructura
- **User Service**: Fachada del dominio que expone operaciones de alto nivel
- **Modelos de dominio**: Entidades y reglas de negocio

#### 4. **Adaptadores de Salida** (Futuro)
- Base de datos, APIs externas, servicios de terceros
- Implementan interfaces definidas por el dominio

### Flujo de Datos

1. **Request HTTP** → `routes/health.py` o `routes/status.py`
2. **Adaptador** → `facade.py` (Fachada de Aplicación)
3. **Fachada** → `domain/user_service.py` (Fachada de Dominio)
4. **Dominio** → `domain/user.py` (Lógica de negocio)
5. **Response** ← Se devuelve por el mismo camino

## Estructura del proyecto

```
backend-base/
├── src/                           # Código fuente principal
│   ├── __init__.py               # Hace que src sea un paquete Python
│   ├── app.py                    # Configuración principal de FastAPI
│   ├── config.py                 # Configuración de la aplicación
│   ├── log.py                    # Configuración de logging
│   │
│   ├── adapters/                 # ADAPTADORES (Capa Externa)
│   │   ├── __init__.py
│   │   └── api/                  # Adaptadores de entrada HTTP
│   │       ├── __init__.py
│   │       ├── facade.py         # Fachada de Aplicación
│   │       └── routes/           # Rutas HTTP organizadas por funcionalidad
│   │           ├── __init__.py
```

---

## Tecnologias y herramientas

- Python 3.12 — lenguaje principal; usaremos tipado estático con mypy.
- FastAPI — framework ASGI para endpoints y documentación automática (OpenAPI/Swagger).
- Uvicorn — servidor ASGI para ejecutar la app.
- pydantic / pydantic-settings — validación de datos y gestión de configuración desde `.env`.
- Docker & Docker Compose — reproducibilidad del entorno y facilitan CI/CD.
- pytest / pytest-bdd — testing unitario y pruebas de aceptación (BDD).
- black, isort, mypy — formateo y chequeo estático de tipos.
- Render (ejemplo) — plataforma de despliegue utilizada en el workflow de ejemplo.

---

## Como desarrollar

1. Clonar el repositorio y posicionarse en la carpeta:

```bash
git clone <repo-url>
cd backend-base
```

2. Copiar el ejemplo de variables y ajustar localmente:

```bash
cp .env.example .env
# editar .env con tus valores si hace falta
```

3. Levantar el entorno y entrar a la shell del contenedor:

- PowerShell (manual):

```powershell
docker compose up -d --build
docker compose exec backend sh
```

- Git Bash / WSL (script):

```bash
bash ./scripts/enter_dev.sh
```

4. Dentro del contenedor, iniciar el servidor (si no arrancó automáticamente):

```bash
make run
```

5. Acceder a `http://localhost:8000` y a `http://localhost:8000/docs`.

Consejos:
- Edita el código en el host; los cambios se reflejan inmediatamente por el volume `.:/app`.
- Usa `make check` para validar formato y tipos antes de commitear.

---

## Arquitectura - Fachada
 
El proyecto centraliza la lógica de orquestación en una *Fachada de Aplicación* (`src/adapters/api/facade.py`). Las rutas HTTP actúan como adaptadores de entrada y delegan en la fachada, que a su vez llama al Dominio (`src/domain/`).

Beneficios:

- Rutas limpias y sin lógica de negocio.
- La fachada es el único lugar que conoce cómo componer servicios del dominio.
- Facilita testing unitario de dominio y testing de integración de adaptadores.

---

## Tests

Este proyecto contiene dos tipos principales de pruebas:

- Tests unitarios (unidad): se enfocan en funciones y clases del dominio sin dependencias externas.
- Tests de aceptación (BDD): prueban el comportamiento desde la perspectiva del usuario/cliente, usando escenarios escritos en formato Gherkin (archivos `.feature`) y pasos definidos con `pytest-bdd`.

Ubicación en el repo:

- Tests unitarios: `tests/domain/` — verifican la lógica del dominio.
- Tests de aceptación: `tests/acceptance/` — contiene `features/` (Gherkin) y `steps/` con los step-implementations.

Cómo están configurados y por qué es correcto

- `pytest.ini` configura `pythonpath = src` para que los tests puedan importar `src.*` sin manipular `sys.path`. Esto es correcto para un proyecto donde `src` contiene el paquete de la aplicación.
- `testpaths = tests` centraliza la búsqueda de tests en la carpeta `tests`.
- `python_files = test_*.py` hace que pytest descubra archivos que empiezan con `test_`
- `markers = bdd: pruebas BDD con pytest-bdd` declara el marcador BDD (útil para etiquetar y filtrar pruebas BDD en el CI o localmente).
- `addopts` actualmente incluye opciones para coverage y un umbral mínimo; es adecuado para CI.

En resumen: la configuración de `pytest.ini` es correcta para el layout actual del repo y permitirá ejecutar tanto tests unitarios como los de aceptación.

Ejecutar pruebas

- Ejecutar todos los tests y generar cobertura (local):
    ```bash
    make test
    ```

- Ejecutar solo tests unitarios:
    ```bash
    make test-unit
    ```

- Ejecutar solo tests de aceptación (BDD):
    ```bash
    make test-acceptance
    ```

- Ejecutar un escenario específico (BDD) o un step:
    ```bash
    pytest tests/acceptance -k "status"
    ```

Notas prácticas sobre los acceptance tests del repo

- Los acceptance tests definidos usan `fastapi.testclient.TestClient` (sin arrancar un servidor separado). Esto es correcto: TestClient monta la aplicación en memoria y permite realizar peticiones HTTP simuladas rápidamente sin depender de procesos externos.
- En `tests/acceptance/steps/test_status_steps.py` se usa `scenarios("../features/status.feature")` para cargar las feature files; la ruta relativa está bien (desde `steps/` hacia `features/`).
- Como los steps devuelven responses del `TestClient`, no necesitas levantar el contenedor para ejecutar los acceptance tests localmente.

Recomendaciones y mejoras

- Mantener `pytest.ini` tal como está. Si en el futuro añades tests que requieren servicios externos (por ejemplo, Postgres), crea un marker o un perfil (`-m integration`) para distinguir tests que necesitan infraestructura de los que no.
- Considera añadir un objetivo Make como `make test-acceptance` y `make test-unit` (si no lo tienes) para facilitar la ejecución desde la raíz; actualmente los targets existen (`test-unit`, `test-acceptance`).
- Si sueles ejecutar tests desde el contenedor, asegúrate de que el contenedor tenga las mismas dependencias que tu `requirements.txt` y que `PYTHONPATH` o instalación editable apunten a `src`.
- Para debugging de BDD: ejecuta `pytest -k <escenario> -s -vv` para ver salida completa y detener buffering.

---

En CI se ejecutan `make check` y `make test` (ver `.github/workflows/main.yml`).

---

## Makefile (comandos clave)

- `make up` — construye y levanta contenedores (detached): `docker compose up -d --build`.
- `make down` — detiene y limpia: `docker compose down`.
- `make shell` — entra en la shell del servicio `backend`.
- `make run` — arranca uvicorn en `0.0.0.0:8000 --reload`.
- `make format` / `make format-check` — aplica o verifica `black` + `isort`.
- `make lint` — ejecuta `mypy`.
- `make check` — ejecuta `format-check` + `lint`.
- `make test` — ejecuta tests.

Uso recomendado durante dev: `make shell` → `make run`.

---

## Docker (detalle operativo)

- `Dockerfile` genera la imagen basada en `python:3.12-slim`.
- `docker-compose.yml` define el servicio `backend` con:
  - puerto `8000:8000`
  - volumen `.:/app` para hot reload
  - comando que ejecuta `uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000} --reload`

Consejos:

- En producción evita `--reload` y no montes el código como volumen.
- Si necesitas DB en dev, añade un servicio `postgres` en `docker-compose.yml` y ajusta `DATABASE_URL`.

---

## CI/CD y Deploy automático (GitHub Actions → Render)

El workflow en `.github/workflows/main.yml` realiza:

1. Checkout y setup Python.
2. Instala dependencias y ejecuta `make check` + `make test`.
3. Si los checks pasan y el push es a `main`, dispara un deploy en Render usando la API.
4. Hace health-check a la `RENDER_URL` para verificar que el servicio responde.

Variables usadas en el workflow (definirlas en GitHub Secrets):

- `RENDER_API_KEY` — token para la API de Render.
- `RENDER_SERVICE_ID` — ID del servicio a desplegar.
- `RENDER_URL` — URL pública para el health check.

Variables sensibles adicionales que conviene guardar en Secrets:

- `DATABASE_URL` — cadena de conexión para la base de datos en producción.
- `SECRET_KEY` — clave secreta para JWT/firmas.

No guardes valores reales en `.env.example`; usa este archivo sólo como referencia.

---

## .env / .env.example (qué variables incluir)

Ejemplo mínimo en `.env.example`:

```
PROJECT_NAME=BackendBase
ENVIRONMENT=dev
PORT=8000
```

En producción añade al menos:

```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
SECRET_KEY=<valor-secreto>
```

---

## Recomendaciones y próximos pasos

- Añadir migraciones con Alembic para DB relacional.
- Añadir tests de integración con una DB real en CI.
- Configurar logging estructurado y métricas para producción.
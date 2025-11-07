# 🧩 backend-base — Plantilla profesional para APIs con FastAPI y SQLAlchemy

> **Arquitectura hexagonal (Ports & Adapters) · Base de datos integrada · Migraciones Alembic · Tests BDD y CI/CD listos**

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python version" />
  <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLAlchemy-async-orange?logo=python" alt="SQLAlchemy async" />
  <img src="https://img.shields.io/badge/Alembic-migrations-yellow" alt="Alembic" />
  <img src="https://img.shields.io/badge/tests-pytest%20%2B%20BDD-green?logo=pytest" alt="Testing" />
  <img src="https://img.shields.io/badge/docker-ready-2496ED?logo=docker" alt="Docker" />
<img src="https://github.com/pgallino/backend-base/actions/workflows/main.yml/badge.svg?branch=main" alt="GitHub Actions CI" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License MIT" />
</p>

---

## 📚 Índice

1. [Resumen](#-resumen)
2. [Arquitectura](#-arquitectura)
3. [Estructura del proyecto](#-estructura-del-proyecto)
4. [Requisitos y stack](#-requisitos-y-stack)
5. [Configuración y entorno](#-configuración-y-entorno)
6. [Base de datos y migraciones](#-base-de-datos-y-migraciones)
7. [Ejecución en desarrollo](#-ejecución-en-desarrollo)
8. [Pruebas (TDD y BDD)](#-pruebas-tdd-y-bdd)
9. [Makefile y comandos útiles](#-makefile-y-comandos-útiles)
10. [CI/CD y despliegue](#-cicd-y-despliegue)
11. [Reutilización y buenas prácticas](#-reutilización-y-buenas-prácticas)

---

## 🚀 Resumen

`backend-base` es una plantilla profesional para construir **backends escalables en Python**, con **FastAPI**, **SQLAlchemy asíncrono** y **Alembic** para la gestión de base de datos.

Sigue los principios de **Arquitectura Hexagonal (Ports & Adapters)**, garantizando una separación clara entre dominio, infraestructura y orquestación.

Incluye configuración lista para **tests unitarios y de aceptación (BDD)**, y ejemplos de **despliegue con Docker, Render y AWS**.

### 🎯 Objetivo
Proporcionar una base sólida, extensible y educativa para proyectos reales, enfocada en:

- Diseño limpio y mantenible (DDD + Hexagonal)
- Tests integrados desde el inicio (unit + BDD)
- Configuración y despliegue reproducibles con Docker
- Separación clara entre dominio, adaptadores y orquestación

---

## 🧱 Arquitectura

El proyecto implementa una **Arquitectura Hexagonal (Ports & Adapters)**, donde cada capa tiene una responsabilidad bien definida.

```text
Adaptador de Entrada (HTTP/CLI)
        ↓
[Fachada de Aplicación (Orquestador)]
        ↓ (Usa uno o varios)
[Servicios de Aplicación/Dominio]
        ↓ (Interactúan con)
[Adaptadores de Salida: Repositorios]
        ↓
Base de Datos (PostgreSQL / SQLite)
```

### Capas principales

### 🗂️ Capas y Componentes Clave

| Capa/Componente | Rol Principal | Interacciones Clave |
| :--- | :--- | :--- |
| **Adaptadores de Entrada** | Reciben peticiones (HTTP, CLI), validan los datos y delegan en la Fachada. | Solo interactúan con la **Fachada de Aplicación**. |
| **Fachada de Aplicación** | Actúa como **orquestador principal** de un caso de uso. | Invoca a uno o más **Servicios de Aplicación/Dominio** para ejecutar la lógica. |
| **Servicios de Aplicación/Dominio** | Contienen la lógica de negocio específica y utilizan los Repositorios para datos. | Utilizan los **Repositorios** (Adaptadores de Salida) para obtener o guardar datos. |
| **Dominio** | Contiene **Entidades** y **Reglas de Negocio Puras**. | Son utilizados e implementados por los **Servicios** (las Entidades viajan entre capas). |
| **Adaptadores de Salida: Repositorios** | Implementan la interfaz de persistencia (el Puerto) utilizando tecnología específica (**SQLAlchemy async**). | Interactúan con la **Base de Datos**. |
| **Infraestructura** | Servicios transversales: configuración, *logging*, *fixtures*, etc. | Provee herramientas de soporte al resto de las capas. |

Esta separación facilita el testing, la evolución del código y la independencia del framework o base de datos.

---

## 🗂️ Estructura del proyecto

```bash
src/
├── app.py                  # Punto de entrada (FastAPI)
├── config.py               # Configuración central
├── adapters/
│   ├── api/                # Endpoints + fachada
│   └── db/                 # Modelos y repositorios SQLAlchemy
├── domain/                 # Entidades y servicios de dominio
alembic/                    # Migraciones de esquema
tests/                      # Tests unitarios y BDD
```

---

## 💻 Requisitos y stack

- Python **3.11+** (preparado para 3.12)
- **FastAPI** — framework principal
- **SQLAlchemy async** — ORM asíncrono
- **Alembic** — migraciones de base de datos
- **pytest + pytest-bdd** — testing unitario y de aceptación
- **Docker Compose** — entorno reproducible
- **GitHub Actions** — CI/CD de ejemplo

---

## ⚙️ Configuración y entorno

El proyecto usa un archivo `.env` para variables de entorno. Ejemplo (`.env.example`):

```bash
ENVIRONMENT=dev
PORT=8000
DB_URL_SYNC=sqlite:///dev.db
DB_URL_ASYNC=sqlite+aiosqlite:///dev.db
ALLOWED_ORIGINS=http://localhost:3000
SECRET_KEY=super-secret-key
```

> ⚠️ **No subas secretos reales al repositorio.** Usa secrets en CI/CD o servicios como Render o AWS.

### Configuración en desarrollo (recomendado)

Para facilitar el desarrollo local, incluimos un archivo de ejemplo `.env.example` en la raíz del proyecto.

Flujo recomendado para nuevos desarrolladores:

1. Copia el ejemplo a `.env` (archivo local, nunca comiteado):

```bash
cp .env.example .env
```

---

## 🗄️ Base de datos y migraciones

Alembic se utiliza para versionar el esquema de la base de datos.

### Alembic

Alembic es la herramienta de migrations para SQLAlchemy: permite crear "revisiones" que describen cambios en el esquema (crear tablas, columnas, índices) y aplicarlas de forma ordenada en cualquier entorno. En este proyecto usamos Alembic para mantener el historial del esquema y aplicarlo en CI / despliegues.

Hemos añadido objetivos en el `Makefile` para envolver Alembic y simplificar el flujo. Usa los objetivos `make` desde tu máquina o dentro del contenedor:

```bash
# Inicializar (solo la primera vez en un repo nuevo):
make alembic-init

# Crear una nueva migración (autogenerate + archivo en alembic/versions):
make alembic-migrate

# Aplicar migraciones (upgrade hasta head):
make alembic-upgrade

# Deshacer la última migración (downgrade -1):
make alembic-downgrade
```

Usar `make` garantiza que `PYTHONPATH` y el contexto de ejecución estén correctamente definidos para que Alembic encuentre el módulo `src`.

### Variables relevantes

- `DB_URL_SYNC` — URL sincrónica (usada por Alembic)
- `DB_URL_ASYNC` — URL asíncrona (usada por la app)

Nota: Alembic requiere un driver sincrónico; la app usa un driver asíncrono (ej: `postgresql+asyncpg://`). En CI y despliegue define ambas variables de entorno según corresponda.

---

## 🧑‍💻 Ejecución en desarrollo

Con **Docker Compose** (recomendado):

```bash

# Levantar los servicios de desarrollo (api + cli)
docker compose -f docker-compose.dev.yml up -d

# Entrar al contenedor CLI (para ejecutar comandos Typer / make)
docker compose -f docker-compose.dev.yml exec cli sh

# Entrar al contenedor API (uvicorn corre en segundo plano)
docker compose -f docker-compose.dev.yml exec api sh
```

### Desarrollo — hay dos aplicaciones (API y CLI)

En este repositorio conviven dos "apps" distintas que comparten la misma base de código y la misma fachada de aplicación:

- API (FastAPI): el servidor HTTP que expone los endpoints REST/OpenAPI. El entrypoint de la API está en `src.application.api_app` y en desarrollo se ejecuta con `uvicorn`.
- CLI (Typer): una interfaz de línea de comandos que reutiliza la lógica de la aplicación (fachada). El entrypoint del CLI está en `src.cli_app`.

Por qué dos aplicaciones?
- Muestra que, reutilizando la misma fachada de aplicación y sin modificar el código interno del dominio, se pueden exponer múltiples interfaces (por ejemplo HTTP y CLI) que comparten exactamente la misma lógica. 

Arquitectura de Docker / dependencias

- Archivos de requirements:
        - `requirements-dev.txt` — dependencias para desarrollo (typer, pytest, herramientas de formateo). Se usa en la imagen `Dockerfile.dev`.
        - `requirements-prod.txt` — dependencias mínimas para producción. Se usa en `Dockerfile`.

- Dockerfiles:
        - `Dockerfile.dev` — imagen pensada para desarrollo: incluye herramientas de testing/format y utilidades para iterar rápido.
        - `Dockerfile` — imagen optimizada para producción: minimal, no incluye herramientas de desarrollo y usa `requirements-prod.txt`.

- Compose para desarrollo:
        - `docker-compose.dev.yml` — orquesta los servicios locales para desarrollo (normalmente `api` y `cli`).

Cómo usar la API y la CLI (paso a paso)

1) Construir la imagen de desarrollo y levantar los servicios

```bash
docker compose -f docker-compose.dev.yml up -d --build
```

2) Entrar a la shell del CLI (útil para ejecutar comandos Typer):

```bash
docker compose -f docker-compose.dev.yml exec cli sh
# dentro del contenedor:
python -m src.cli_app list-tools
python -m src.cli_app create "AWS" --description "Despliegue en la nube" --link "https://aws.com"
```

3) Usar la API desde el host (documentación interactiva en /docs):

```bash
curl http://localhost:8000/  # o la ruta health/ según la app
# Abrir la UI de OpenAPI en el navegador:
http://localhost:8000/docs
```

4) Ejecutar migraciones (Alembic) usando el contenedor CLI (usa `.env` para DB_URL_SYNC):

```bash
docker compose -f docker-compose.dev.yml exec cli alembic upgrade head
```

Consejos rápidos
- Si quieres menos ruido en logs, define en tu `.env`:

```
LOG_LEVEL=INFO
```

---

## 🧪 Pruebas (TDD y BDD)

El proyecto incluye **tests unitarios y de aceptación**.

### Estructura

```
tests/
├── domain/           # Tests unitarios (lógica pura)
└── acceptance/       # Tests BDD (pytest-bdd + Gherkin)
```

### Comandos

```bash
make test            # Ejecuta todos los tests
make test-unit       # Solo tests unitarios
make test-acceptance # Solo tests BDD
```

> Las pruebas BDD usan `TestClient` de FastAPI y se ejecutan sin servidor externo.

Detalles prácticos sobre `TestClient` y los acceptance tests

- Qué hace `TestClient`: monta la aplicación ASGI (FastAPI) en memoria y permite hacer peticiones HTTP a la app desde pytest sin necesidad de arrancar un proceso externo. Esto habilita pruebas rápidas e independientes del entorno.

- Inicio y eventos de aplicación: `TestClient` dispara los eventos de `startup` y `shutdown` de FastAPI, por lo que cualquier inicialización (conexión a DB en tests, carga de fixtures) definida en el `lifespan` o `startup` se ejecuta automáticamente.

- Fixtures y preparación de la DB: en `tests/acceptance/conftest.py` hay fixtures que crean/aseguran las tablas, limpian filas entre escenarios y reinician secuencias (SQLite). Asegúrate de que las fixtures hagan _arranque limpio_ (crear tablas si hace falta y truncar) para que cada escenario sea determinista.

- Cómo ejecutar los acceptance tests:

```bash
# desde el host (usa las variables de entorno del entorno de desarrollo):
make test-acceptance

# ejecutar un escenario o un conjunto especifico (más verboso):
pytest tests/acceptance -k "herramientas" -s -vv
```

- Ejecutar dentro del contenedor (recomendado para reproducibilidad):

```bash
make shell        # levanta y entra al contenedor
# dentro del contenedor:
make test-acceptance
```

Con esto las pruebas BDD permanecen rápidas, deterministas y fáciles de ejecutar tanto en tu máquina como en CI.

---

## 🧰 Makefile y comandos útiles

| Comando | Descripción |
|----------|--------------|
| `make up` | Construye y levanta contenedores |
| `make down` | Detiene y elimina servicios |
| `make test` | Ejecuta toda la suite de tests |
| `make format` | Formatea el código con black/isort |
| `make lint` | Ejecuta linters y type-checks |
| `make check` | Corre `format-check` + `lint` |
| `make shell` | Abre una shell en el contenedor backend |

---

## ☁️ CI/CD y despliegue

Esta plantilla incluye workflows de ejemplo en `.github/workflows/` y patrones recomendados para desplegar en Render, AWS (App Runner/ECS) o usando Neon como base de datos.

### Neon (Postgres serverless)

- Define en GitHub Secrets la URL de Neon. En este proyecto conviene publicar ambas variantes según uso:
   - `DB_URL_ASYNC` — p. ej. `postgresql+asyncpg://user:pass@host/db` (usada por la app FastAPI)
   - `DB_URL_SYNC` — p. ej. `postgresql+psycopg2://user:pass@host/db` (útil para ejecutar Alembic desde un job/contenedor sync)

### AWS (ECR + App Runner)

Los workflows de despliegue en este repositorio ya se encargan de ejecutar las migraciones en Neon antes de promover la nueva versión, por lo que no es necesario ejecutar migraciones manualmente durante el despliegue. Para desplegar en AWS normalmente sólo necesitas construir y subir la imagen a ECR, configurar el servicio App Runner y asegurarte de que los secrets/variables estén presentes en GitHub Actions o en el entorno de ejecución.

Variables/Secrets clave en AWS:

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `ECR_REPOSITORY`
- `DB_URL_ASYNC`, `SECRET_KEY`, `ALLOWED_ORIGINS`


### Render

El pipeline de despliegue de este repositorio invoca el workflow de migraciones en Neon, de modo que no es necesario ejecutar comandos de migración manualmente en Render. Configura el servicio en Render para que use la imagen que publica el workflow y añade los secrets/variables necesarios.

Variables/Secrets a configurar en Render:

- `RENDER_API_KEY`, `RENDER_SERVICE_ID`, `DB_URL_ASYNC`, `ALLOWED_ORIGINS`

### GitHub Actions

Workflows incluidos (ejemplos):

- `main.yml` — checks y tests (`make check`, `make test`).
- `deploy-render.yml` — ejemplo para disparar un deploy en Render.
- `deploy-aws.yml` — ejemplo para build/push a ECR y despliegue;

Nota importante: los workflows están listos como ejemplos; para que funcionen define los secrets mencionados en Settings → Secrets. En este repositorio los pipelines de despliegue ya invocan el workflow de migraciones (`deploy-neon.yml`) y por tanto las migraciones se ejecutan automáticamente contra Neon durante el proceso de despliegue — no hace falta ejecutarlas manualmente. Asegúrate de que `DB_URL_SYNC`/`DB_URL_ASYNC` y demás secrets estén definidos en GitHub Actions para que el job de migraciones pueda conectarse a Neon.

### Secrets a crear (copia/pega)

A continuación tienes una tabla con los secrets y variables que aparecen en los workflows; crea estos secrets en GitHub (Settings → Secrets and variables → Actions) y configura las variables de entorno equivalentes en tu proveedor (Render, ECS, App Runner) para runtime:

| Secret / Variable | Usado por | Descripción |
|---|---|---|
| NEON_DB_SYNC | `deploy-neon.yml` (job `migrate`) | URL síncrona de Neon (ej. `postgresql+psycopg2://user:pass@host:port/db`) — usada por Alembic en el job de migraciones |
| DB_URL_ASYNC | runtime (Render / ECS / App Runner) | URL asíncrona para la app FastAPI (ej. `postgresql+asyncpg://user:pass@host/db`) |
| DB_URL_SYNC | (opcional) runtime / CI | Variante síncrona si alguna tarea la necesita en runtime; `NEON_DB_SYNC` se pasa a los workflows para migraciones |
| AWS_ACCESS_KEY_ID | `deploy-aws.yml` | Credencial AWS (user con permisos ECR/Push) |
| AWS_SECRET_ACCESS_KEY | `deploy-aws.yml` | Credencial AWS |
| AWS_ACCOUNT_ID | `deploy-aws.yml` | ID de la cuenta AWS (usado para tag de la imagen) |
| ECR_REPOSITORY | `deploy-aws.yml` | Nombre del repositorio en ECR (se puede dejar en env del workflow) |
| RENDER_API_KEY | `deploy-render.yml` | API key para la cuenta Render (usar secret) |
| RENDER_SERVICE_ID | `deploy-render.yml` | ID del servicio en Render que se va a desplegar |
| RENDER_URL | `deploy-render.yml` | URL pública para health-check (opcional; usada por el workflow) |
| SECRET_KEY | runtime | Clave secreta de la aplicación (runtime) |
| ALLOWED_ORIGINS | runtime | Orígenes permitidos para CORS (runtime) |

> Nota: `NEON_DB_SYNC` es el secret requerido por `deploy-neon.yml` y el workflow lo exporta como `DB_URL_SYNC` para ejecutar `make alembic-upgrade`. `DB_URL_ASYNC` debe establecerse en el entorno del servicio para que la app use el driver asíncrono en producción.

---

## ♻️ Reutilización y buenas prácticas

La arquitectura está pensada para ser **reutilizable y desacoplada**:

- El **dominio** y la **fachada** no dependen de frameworks.
- Se puede cambiar la base de datos sin modificar la lógica de negocio.
- Permite testear el dominio de forma aislada.
- Facilita extender a otros tipos de adaptadores (gRPC, CLI, eventos, etc.).

> Mantén las entidades puras, define interfaces en el dominio y deja las implementaciones en `adapters/`.

---

📘 **Con esta plantilla tendrás un backend modular, testeable y preparado para producción, sin sacrificar claridad ni mantenibilidad.**

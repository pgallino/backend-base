# Backend Base

Un proyecto base para desarrollo de APIs REST con FastAPI implementando **Arquitectura Hexagonal** (Ports & Adapters), con un ambiente de desarrollo completamente containerizado.

## 📋 Tabla de Contenidos

- [Arquitectura](#-arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Ambiente de Desarrollo](#-ambiente-de-desarrollo)
- [Comandos Disponibles](#-comandos-disponibles)
- [CI/CD y Calidad de Código](#-cicd-y-calidad-de-código)
- [Configuración](#-configuración)

## 🏗️ Arquitectura

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
- **System Service**: Fachada del dominio que expone operaciones de alto nivel
- **Modelos de dominio**: Entidades y reglas de negocio

#### 4. **Adaptadores de Salida** (Futuro)
- Base de datos, APIs externas, servicios de terceros
- Implementan interfaces definidas por el dominio

### Flujo de Datos

1. **Request HTTP** → `routes/health.py` o `routes/status.py`
2. **Adaptador** → `facade.py` (Fachada de Aplicación)
3. **Fachada** → `domain/system_service.py` (Fachada de Dominio)
4. **Dominio** → `domain/system.py` (Lógica de negocio)
5. **Response** ← Se devuelve por el mismo camino

## 📁 Estructura del Proyecto

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
│   │           ├── health.py     # Endpoint de salud básico
│   │           └── status.py     # Endpoint de estado del sistema
│   │
│   └── domain/                   # DOMINIO (Núcleo de Negocio)
│       ├── __init__.py
│       ├── system_service.py     # Fachada del dominio
│       └── system.py             # Lógica de negocio del sistema
│
├── docker-compose.yml            # Configuración del ambiente
├── Dockerfile                    # Imagen del contenedor
├── Makefile                      # Comandos de desarrollo
├── requirements.txt              # Dependencias Python
└── README.md                     # Este archivo
```

### Detalles de Componentes

#### **`src/app.py`**
- Configuración principal de FastAPI
- Registro de rutas y middleware
- Eventos de startup/shutdown

#### **`src/adapters/api/facade.py`**
- **Patrón Facade**: Simplifica la interfaz hacia el dominio
- **Único punto de entrada**: Todas las rutas usan esta fachada
- **Inyección de dependencias**: Pasa configuración al dominio

#### **`src/adapters/api/routes/`**
- **Separación por funcionalidad**: Cada archivo maneja un área específica
- **Responsabilidad única**: Solo adaptación HTTP ↔ Dominio
- **Sin lógica de negocio**: Delegan todo a la fachada

#### **`src/domain/`**
- **Independiente de infraestructura**: No conoce HTTP, DB, etc.
- **Testeable**: Lógica pura sin dependencias externas
- **Reutilizable**: Puede usarse desde cualquier adaptador

## 🐳 Ambiente de Desarrollo

El proyecto está completamente containerizado para garantizar consistencia entre desarrolladores.

### Tecnologías Utilizadas

- **Python 3.12**: Lenguaje principal
- **FastAPI**: Framework web moderno y rápido
- **Docker**: Containerización del ambiente
- **SQLite**: Base de datos para desarrollo
- **Uvicorn**: Servidor ASGI para FastAPI

### Configuración del Ambiente

El ambiente se configura automáticamente con:

```yaml
# docker-compose.yml
services:
  backend:
    build: .
    ports:
      - "8000:8000"         # API disponible en localhost:8000
    volumes:
      - .:/app              # Hot reload: cambios se reflejan inmediatamente
    environment:
      DATABASE_URL: sqlite+aiosqlite:///dev.db
      PROJECT_NAME: BackendBase
      ENVIRONMENT: dev
```

### Dockerfile Optimizado

```dockerfile
FROM python:3.12-slim

# Herramientas necesarias
RUN apt-get update && apt-get install -y build-essential make

WORKDIR /app

# Instalación de dependencias (aprovecha caché de Docker)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Código fuente
COPY src ./src
```

## 🚀 Comandos Disponibles

Todos los comandos están definidos en el `Makefile` para facilidad de uso.

### Comandos del Host (tu máquina)

```bash
# Levantar el ambiente completo
make up

# Detener y limpiar el ambiente
make down

# Entrar al contenedor para desarrollo
make shell
```

### Comandos del Contenedor (dentro de la shell)

```bash
# Iniciar el servidor de desarrollo
make run               # Servidor en http://localhost:8000 con hot reload

# Formateo de código
make format            # Aplica black e isort al código
make format-check      # Verifica formato sin modificar

# Análisis estático
make lint              # Ejecuta mypy para verificar tipos

# Verificación completa
make check             # Ejecuta format-check + lint
```

### Flujo de Trabajo Típico

```bash
# 1. Levantar y entrar al ambiente
make shell

# 2. Dentro del contenedor, iniciar el servidor
make run

# 3. En otra terminal, hacer cambios y verificar calidad
make check
```

## 🔍 CI/CD y Calidad de Código

### Herramientas de Calidad

#### **Black** - Formateo de Código
- Formato consistente y automático
- Configuración estándar sin personalización
- Elimina debates sobre estilo de código

#### **isort** - Organización de Imports
- Ordena y agrupa imports automáticamente
- Compatible con black
- Mejora legibilidad del código

#### **MyPy** - Verificación de Tipos
- Análisis estático de tipos
- Detecta errores antes de runtime
- Mejora la mantenibilidad del código

### Pipeline de Verificación

```bash
# El comando 'make check' ejecuta:
1. make format-check  # Verifica formato de código
2. make lint          # Verifica tipos estáticos
```

## 🧪 Tests y Cobertura

Este proyecto usa pytest para pruebas unitarias del Dominio.

La cobertura está configurada para omitir `src/domain/__init__.py` mediante `.coveragerc`.

### Ejecutar tests

```bash
make test
```

Por defecto, se incluye reporte de cobertura en consola para `src/domain`.

### Ver cobertura en CI

El objetivo `ci` genera `coverage.xml` para integraciones con CI.

```bash
make ci
```

## ⚙️ Configuración

### Variables de Ambiente

La configuración se maneja a través de `src/config.py` usando Pydantic Settings:

```python
# Configuración principal
PROJECT_NAME: str = "BackendBase"
ENVIRONMENT: str = "dev"
DATABASE_URL: str = "sqlite+aiosqlite:///dev.db"
SECRET_KEY: str = "secret-key"
```

### Ambientes

#### Desarrollo (por defecto)
- Base de datos SQLite en archivo
- Hot reload habilitado
- Logs detallados
- Puerto 8000 expuesto

#### Producción (configuración futura)
- Base de datos PostgreSQL
- Logs estructurados
- Variables de ambiente desde secrets
- Configuración de seguridad adicional

### Logging

```python
# src/log.py
import logging

logger = logging.getLogger("backend-base")
# Configuración centralizada de logs
```

## 🧪 Endpoints Disponibles

### Health Check
```http
GET /
```
Respuesta básica para verificar que el servicio está funcionando.

### System Status
```http
GET /status
```
Estado detallado del sistema con información de configuración.

### Documentación Automática
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔄 Próximos Pasos

1. **Tests**: Implementar testing con pytest
2. **Base de datos**: Configurar migraciones con Alembic
3. **Autenticación**: JWT + OAuth2
4. **Monitoreo**: Métricas y observabilidad
5. **CI/CD**: Pipeline completo con GitHub Actions

---

Este proyecto sirve como base sólida para APIs REST escalables, mantenibles y bien estructuradas.
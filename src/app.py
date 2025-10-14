from contextlib import asynccontextmanager

from fastapi import FastAPI

# Importamos el nuevo router
from src.adapters.api.routes import health, status
from src.config import settings
from src.log import logger


@asynccontextmanager
def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación (startup/shutdown)."""
    # Startup
    logger.info(f"La aplicación se está iniciando en ambiente: {settings.ENVIRONMENT}")
    logger.info(f"Usando DB: {settings.DATABASE_URL}")
    yield
    # Shutdown
    logger.info("La aplicación se ha apagado.")


# La instancia principal de la aplicación
app = FastAPI(
    title=f"{settings.PROJECT_NAME} ({settings.ENVIRONMENT})",
    description="Aplicación Backend con Arquitectura Hexagonal.",
    lifespan=lifespan,
)

# --- Inclusión de Rutas (Adaptadores de Entrada) ---

# Incluimos el router de health check
app.include_router(health.router)
app.include_router(status.router)

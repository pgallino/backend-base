from fastapi import FastAPI

# Importamos el nuevo router
from src.adapters.api.routes import health, status
from src.config import settings
from src.log import logger

# La instancia principal de la aplicación
app = FastAPI(
    title=f"{settings.PROJECT_NAME} ({settings.ENVIRONMENT})",
    description="Aplicación Backend con Arquitectura Hexagonal.",
)

# --- Eventos de Aplicación (Infraestructura) ---


@app.on_event("startup")
async def startup_event():
    """Se ejecuta al iniciar la aplicación."""
    # Este log confirma que la app se levantó y cargó la configuración.
    logger.info(f"La aplicación se está iniciando en ambiente: {settings.ENVIRONMENT}")
    logger.info(f"Usando DB: {settings.DATABASE_URL}")


@app.on_event("shutdown")
async def shutdown_event():
    """Se ejecuta al cerrar la aplicación."""
    logger.info("La aplicación se ha apagado.")


# --- Inclusión de Rutas (Adaptadores de Entrada) ---

# Incluimos el router de health check
app.include_router(health.router)
app.include_router(status.router)

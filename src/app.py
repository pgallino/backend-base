from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.api.routes import health, herramientas
from src.config import settings
from src.log import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"La aplicación se está iniciando en ambiente: {settings.ENVIRONMENT}")
    # CORS handling has been intentionally disabled for now. Reintroduce
    # startup-time validation and middleware when we decide to enable CORS.
    yield
    logger.info("La aplicación se ha apagado.")


app = FastAPI(
    title=f"{settings.PROJECT_NAME} ({settings.ENVIRONMENT})",
    description="Aplicación Backend con Arquitectura Hexagonal.",
    lifespan=lifespan,
)

# Note: CORS middleware intentionally removed to keep the app minimal and
# avoid requiring ALLOWED_ORIGINS in CI/deploy for now. If you want to enable
# CORS later, re-add CORSMiddleware and read origins from `settings.ALLOWED_ORIGINS`.

app.include_router(health.router)  # type: ignore
# User routes removed — application only exposes herramientas
app.include_router(herramientas.router)  # type: ignore

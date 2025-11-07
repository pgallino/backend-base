import json
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.api.middleware import add_middlewares
from src.adapters.api.routes import health, tools
from src.application.factory import create_facade
from src.config import settings
from src.log import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"La aplicación se está iniciando en ambiente: {settings.ENVIRONMENT}")
    yield
    logger.info("La aplicación se ha apagado.")


# Instantiate facade for the API adapter
api_facade = create_facade(
    project_name=settings.PROJECT_NAME, environment=settings.ENVIRONMENT
)


app = FastAPI(
    title=f"{settings.PROJECT_NAME} ({settings.ENVIRONMENT})",
    description="Aplicación Backend con Arquitectura Hexagonal.",
    lifespan=lifespan,
)

# Configure middleware (CORS + request-id)
add_middlewares(app, settings)

# Include routers
app.include_router(health.router)  # type: ignore
app.include_router(tools.router)  # type: ignore

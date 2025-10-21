from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.api.facade_instance import api_facade
from src.adapters.api.routes import health, user
from src.config import settings
from src.log import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"La aplicación se está iniciando en ambiente: {settings.ENVIRONMENT}")
    yield
    logger.info("La aplicación se ha apagado.")


app = FastAPI(
    title=f"{settings.PROJECT_NAME} ({settings.ENVIRONMENT})",
    description="Aplicación Backend con Arquitectura Hexagonal.",
    lifespan=lifespan,
)

app.include_router(health.router)  # type: ignore
app.include_router(user.router)  # type: ignore

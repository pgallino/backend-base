from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api.facade_instance import api_facade
from src.adapters.api.routes import health, herramientas, user
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

# CORS middleware: añade orígenes permitidos aquí
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # agrega aquí el origen de tu frontend desplegado si corresponde, p.e.
    # "https://pgallino.github.io/backend-base-front/",
    # Si solo debugueas puedes usar "*" (no recomendado en producción)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # permite OPTIONS, GET, POST, PUT, DELETE...
    allow_headers=["*"],  # permite Content-Type, Authorization, etc.
)

app.include_router(health.router)  # type: ignore
app.include_router(user.router)  # type: ignore
app.include_router(herramientas.router)  # type: ignore

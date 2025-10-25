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

# CORS middleware: read allowed origins from settings.ALLOWED_ORIGINS (env var)
raw = getattr(settings, "ALLOWED_ORIGINS", "") or ""
origins = []
if raw:
    ra = raw.strip()
    if ra.startswith("["):
        try:
            import json

            origins = json.loads(ra)
        except Exception:
            origins = [o.strip() for o in ra.strip("[]").split(",") if o.strip()]
    else:
        origins = [o.strip() for o in ra.split(",") if o.strip()]

# If no origins configured:
# - in non-production we allow localhost for convenience
# - in production we intentionally keep origins empty and log a warning so
#   the deploy must explicitly set ALLOWED_ORIGINS (safer than allowing '*')
if not origins:
    if settings.ENVIRONMENT != "production":
        origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    else:
        # In production, prefer failing closed (no allowed origins) and log
        logger.warning(
            "ALLOWED_ORIGINS is not set and ENVIRONMENT=production. "
            "CORS will not allow browser origins until ALLOWED_ORIGINS is configured."
        )
        origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    max_age=3600,
)

app.include_router(health.router)  # type: ignore
app.include_router(user.router)  # type: ignore
app.include_router(herramientas.router)  # type: ignore

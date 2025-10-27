from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api.routes import health, herramientas
from src.config import settings
from src.log import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"La aplicación se está iniciando en ambiente: {settings.ENVIRONMENT}")
    # Validate ALLOWED_ORIGINS at startup time for non-development environments.
    # We avoid failing during module import (which breaks tests/CI that import
    # settings) and instead enforce the requirement when the app actually
    # starts accepting traffic.
    env = (settings.ENVIRONMENT or "").lower()
    # Treat test/ci as development-like so CI jobs that set ENVIRONMENT=test
    # don't trigger startup failure when using TestClient or importing the app.
    non_dev = env not in ("dev", "development", "test", "ci")
    raw_allowed = getattr(settings, "ALLOWED_ORIGINS", "") or ""
    if non_dev:
        # If origins is empty or the literal '*' is used, fail the startup so
        # deployments must explicitly configure allowed origins.
        if not origins or raw_allowed.strip() == "*":
            raise RuntimeError(
                "ENVIRONMENT is not 'dev' and ALLOWED_ORIGINS is not configured or is '*'.\n"
                "Set ALLOWED_ORIGINS to a comma-separated list of allowed origins (example: 'https://app.example.com')."
            )
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
# - only allow localhost defaults when running in development
# - in any other environment, leave origins as provided (and startup will
#   raise if they're missing or wildcarded)
if not origins:
    if settings.ENVIRONMENT in ("dev", "development"):
        origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    else:
        logger.warning(
            "ALLOWED_ORIGINS is not set and ENVIRONMENT is not 'dev'. "
            "The app will fail to start unless ALLOWED_ORIGINS is configured."
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    max_age=3600,
)

app.include_router(health.router)  # type: ignore
# User routes removed — application only exposes herramientas
app.include_router(herramientas.router)  # type: ignore

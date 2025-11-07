import json
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api.routes import health, tools
from src.config import settings
from src.log import logger, new_request_id, request_id_ctx_var


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
raw = getattr(settings, "ALLOWED_ORIGINS", None) or ""
allow_all = getattr(settings, "ALLOW_ALL_ORIGINS", False)

# Decide origins according to configuration:
origins = []
if allow_all:
    # Allow any origin. When using a wildcard, browsers will refuse cookies/credentials.
    origins = ["*"]
else:
    if raw:
        ra = raw.strip()
        if ra.startswith("["):
            try:
                origins = json.loads(ra)
            except Exception:
                origins = [o.strip() for o in ra.strip("[]").split(",") if o.strip()]
        else:
            origins = [o.strip() for o in ra.split(",") if o.strip()]

# If running in development and no origins are provided, allow localhost for convenience
if not origins and settings.ENVIRONMENT in ("dev", "development"):
    origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

if origins:
    # If origins contains the wildcard, do not enable credentials (browsers block
    # wildcard + credentials). Otherwise allow credentials.
    allow_credentials = not (len(origins) == 1 and origins[0] == "*")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
        max_age=3600,
    )

    @app.middleware("http")
    async def add_request_id_middleware(request: Request, call_next):
        """Middleware que garantiza un request id por petición y lo propaga a los logs.

        - Si el cliente envía X-Request-ID lo reutiliza.
        - Si no, genera uno nuevo y lo añade a la respuesta en X-Request-ID.
        """
        # Prefer header from client if present
        rid = request.headers.get("X-Request-ID") or new_request_id()
        # Set in context var so the formatter picks it up
        request_id_ctx_var.set(rid)
        logger.debug(
            "HTTP request start %s %s request_id=%s",
            request.method,
            request.url.path,
            rid,
        )
        try:
            response = await call_next(request)
        finally:
            # Clear contextvar to avoid leaking between requests in the same loop
            request_id_ctx_var.set("-")
        # Echo back the request id
        response.headers["X-Request-ID"] = rid
        logger.debug(
            "HTTP request end %s %s request_id=%s status=%s",
            request.method,
            request.url.path,
            rid,
            getattr(response, "status_code", "-"),
        )
        return response


app.include_router(health.router)  # type: ignore
# User routes: expose tools
app.include_router(tools.router)  # type: ignore

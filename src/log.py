import contextvars
import logging
import os
import sys
from uuid import uuid4

# Formato de log legible para desarrollo. Incluimos request_id para trazar
# peticiones a través de capas. Nivel por defecto: DEBUG (desarrollo).
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] [%(request_id)s] [%(module)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Context var para propagar el request id entre corutinas
request_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


class RequestIdFormatter(logging.Formatter):
    def format(self, record):
        # Ensure record has request_id attribute for formatting
        try:
            record.request_id = request_id_ctx_var.get()
        except Exception:
            record.request_id = "-"
        return super().format(record)


def setup_logging():
    """Configura el sistema de logging para la aplicación."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(RequestIdFormatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    root = logging.getLogger()
    # Clear default handlers to avoid duplicate logs
    for h in list(root.handlers):
        root.removeHandler(h)
    root.addHandler(handler)
    # Allow overriding the log level from environment (useful for .env in dev)
    # Expected values: DEBUG, INFO, WARNING, ERROR, CRITICAL
    level_name = os.environ.get("LOG_LEVEL", "DEBUG").upper()
    try:
        level = getattr(logging, level_name)
    except Exception:
        level = logging.DEBUG
    root.setLevel(level)

    # Reduce noise from very chatty third-party libraries unless debugging
    if level > logging.DEBUG:
        logging.getLogger("aiosqlite").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        logging.getLogger("uvicorn").setLevel(logging.WARNING)


# Inicializa el logging al cargar el módulo
setup_logging()
logger = logging.getLogger("fastapi_backend")


# Helper to generate a new request id
def new_request_id() -> str:
    return uuid4().hex

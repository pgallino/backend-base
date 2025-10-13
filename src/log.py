import logging
import sys

# Formato de log legible para desarrollo
LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(name)s] [%(module)s:%(lineno)d] - %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging():
    """Configura el sistema de logging para la aplicación."""
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
    )


# Inicializa el logging al cargar el módulo
setup_logging()
logger = logging.getLogger("fastapi_backend")

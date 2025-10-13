from typing import final

from pydantic_settings import BaseSettings


# Usamos final para evitar que esta clase sea heredada o modificada.
@final
class Settings(BaseSettings):
    """
    Configuración base de la aplicación.
    Los valores se cargan automáticamente desde variables de entorno.
    """

    PROJECT_NAME: str = "BackendBase"
    SECRET_KEY: str
    DATABASE_URL: str
    ENVIRONMENT: str = "dev"


# Instancia global de configuración.
# La ignoramos para que mypy no pida argumentos que Pydantic carga de ENV.
settings = Settings()  # type: ignore

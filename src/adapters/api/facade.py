# Contenido para src/adapters/api/facade.py

from dataclasses import asdict
from typing import final

from src.config import settings
from src.domain.user_service import UserService

# Instanciamos la Fachada del Dominio centrada en User
user_service = UserService()


@final
class ApplicationFacade:
    """
    Fachada de la Aplicación.

    Es el punto de entrada para los adaptadores de entrada (rutas).
    Orquesta las llamadas a la capa de Dominio y a otros adaptadores
    (ej: base de datos).
    """

    def health_check(self) -> dict:
        return {
            "project_name": settings.PROJECT_NAME,
            "environment": settings.ENVIRONMENT,
        }

    def get_user(self) -> dict:
        """Obtiene un usuario de ejemplo delegando a UserService."""
        user = user_service.get_user(
            project_name=settings.PROJECT_NAME,
            environment=settings.ENVIRONMENT,
        )
        # user is a dataclass instance; serialize to dict for API
        return asdict(user)


# Creamos una instancia global para que las rutas la usen.
api_facade = ApplicationFacade()

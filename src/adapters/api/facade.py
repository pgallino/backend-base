# Contenido para src/adapters/api/facade.py

from typing import final

from src.config import settings
from src.domain.system_service import SystemService

# Instanciamos la Fachada del Dominio
system_service = SystemService()


@final
class ApplicationFacade:
    """
    Fachada de la Aplicación.

    Es el punto de entrada para los adaptadores de entrada (rutas).
    Orquesta las llamadas a la capa de Dominio y a otros adaptadores
    (ej: base de datos).
    """

    def get_status(self) -> dict:
        """
        Obtiene el estado general del sistema.

        Delega la llamada al Dominio, pasando la configuración de infraestructura.
        """
        # La Fachada de Aplicación llama a la Fachada de Dominio
        return system_service.get_system_status(
            project_name=settings.PROJECT_NAME,
            environment=settings.ENVIRONMENT,
        )


# Creamos una instancia global para que las rutas la usen.
api_facade = ApplicationFacade()

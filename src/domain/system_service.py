# Contenido para src/domain/system_service.py

from typing import final

from .system import build_status_message


@final
class SystemService:
    """
    Fachada del Dominio (Service Layer)

    Es el punto de contacto entre la Fachada de Aplicación y la lógica interna del Dominio.
    No tiene dependencias de infraestructura.
    """

    def get_system_status(self, project_name: str, environment: str) -> dict:
        """
        Orquesta la lógica interna para generar el estado del sistema.
        """
        # La Fachada llama a la lógica atómica del dominio
        return build_status_message(project_name, environment)

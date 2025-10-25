# Contenido para src/adapters/api/facade.py
from typing import final

from src.adapters.db.repositories.tool_repository import SqlAlchemyToolRepository
from src.domain.tool_service import ToolService


@final
class ApplicationFacade:
    """
    Fachada de la Aplicación.
    Es el punto de entrada para los adaptadores de entrada (rutas).
    Orquesta las llamadas a la capa de Dominio y a otros adaptadores (ej: base de datos).
    """

    def __init__(self, project_name, environment, tool_repository=None):
        self.project_name = project_name
        self.environment = environment
        self.tool_service = ToolService(tool_repository or SqlAlchemyToolRepository())

    def health_check(self):
        # Devuelve datos puros, no dict ni JSON
        return self.project_name, self.environment

    # user operations removed: this application only exposes tools

    async def get_tool(self, tool_id: int):
        """Obtiene una herramienta por id delegando a ToolService."""
        return await self.tool_service.get_tool(tool_id)

    async def create_tool(self, name: str, description: str, link: str):
        """Crea una herramienta delegando al servicio."""
        return await self.tool_service.create_tool(name, description, link)

    async def list_tools(self):
        """Devuelve todas las herramientas."""
        return await self.tool_service.list_tools()

# Contenido para src/adapters/api/facade.py

from dataclasses import asdict
from typing import final

from src.adapters.db.repositories.tool_repository import SqlAlchemyToolRepository
from src.adapters.db.repositories.user_repository import SqlAlchemyUserRepository
from src.config import settings
from src.domain.tool_service import ToolService
from src.domain.user_service import UserService


@final
class ApplicationFacade:
    """
    Fachada de la Aplicación.
    Es el punto de entrada para los adaptadores de entrada (rutas).
    Orquesta las llamadas a la capa de Dominio y a otros adaptadores (ej: base de datos).
    """

    def __init__(
        self, project_name, environment, user_repository=None, tool_repository=None
    ):
        self.project_name = project_name
        self.environment = environment
        self.user_service = UserService(user_repository or SqlAlchemyUserRepository())
        self.tool_service = ToolService(tool_repository or SqlAlchemyToolRepository())

    def health_check(self):
        # Devuelve datos puros, no dict ni JSON
        return self.project_name, self.environment

    async def get_user(self, user_id: int):
        """Obtiene un usuario por id delegando a UserService."""
        return await self.user_service.get_user(user_id)

    async def create_user(self, username: str, name: str, email: str):
        """Crea un usuario delegando al servicio."""
        return await self.user_service.create_user(username, name, email)

    async def get_tool(self, tool_id: int):
        """Obtiene una herramienta por id delegando a ToolService."""
        return await self.tool_service.get_tool(tool_id)

    async def create_tool(self, name: str, description: str):
        """Crea una herramienta delegando al servicio."""
        return await self.tool_service.create_tool(name, description)

    async def list_tools(self):
        """Devuelve todas las herramientas."""
        return await self.tool_service.list_tools()

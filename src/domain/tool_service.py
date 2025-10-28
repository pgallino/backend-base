from typing import final

from .tool import Tool


@final
class ToolService:
    """Servicio de dominio para la entidad Tool (herramientas)."""

    def __init__(self, tool_repository=None):
        self.tool_repository = tool_repository

    async def get_tool(self, tool_id: int) -> Tool | None:
        if self.tool_repository is None:
            raise RuntimeError("No hay repositorio de tool configurado")
        return await self.tool_repository.get_by_id(tool_id)

    async def create_tool(self, name: str, description: str, link: str) -> Tool:
        if self.tool_repository is None:
            raise RuntimeError("No hay repositorio de tool configurado")
        tool = Tool.from_input(name=name, description=description, link=link)
        return await self.tool_repository.create(tool)

    async def list_tools(self) -> list[Tool]:
        if self.tool_repository is None:
            raise RuntimeError("No hay repositorio de tool configurado")
        return await self.tool_repository.list_all()

    async def update_tool(
        self,
        tool_id: int,
        name: str | None = None,
        description: str | None = None,
        link: str | None = None,
    ) -> Tool | None:
        if self.tool_repository is None:
            raise RuntimeError("No hay repositorio de tool configurado")
        existing = await self.tool_repository.get_by_id(tool_id)
        if existing is None:
            return None
        # construct updated tool (preserve existing values when None)
        updated = Tool(
            id=existing.id,
            name=name or existing.name,
            description=(
                description if description is not None else existing.description
            ),
            link=link if link is not None else existing.link,
        )
        return await self.tool_repository.update(updated)

    async def delete_tool(self, tool_id: int) -> bool:
        if self.tool_repository is None:
            raise RuntimeError("No hay repositorio de tool configurado")
        return await self.tool_repository.delete(tool_id)

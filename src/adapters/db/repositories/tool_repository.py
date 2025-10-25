from typing import Optional

from sqlalchemy.future import select

from src.adapters.db.models.models import ToolModel
from src.adapters.db.session import AsyncSessionLocal
from src.domain.repositories.tool_repository import ToolRepository
from src.domain.tool import Tool


class SqlAlchemyToolRepository(ToolRepository):
    async def get_by_id(self, tool_id: int) -> Optional[Tool]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ToolModel).where(ToolModel.id == tool_id)
            )
            row = result.scalar_one_or_none()
            if row:
                return Tool(
                    id=getattr(row, "id"),
                    name=getattr(row, "name"),
                    description=getattr(row, "description"),
                )
            return None

    async def create(self, tool: Tool) -> Tool:
        async with AsyncSessionLocal() as session:
            model = ToolModel(name=tool.name, description=tool.description)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return Tool(
                id=getattr(model, "id"),
                name=getattr(model, "name"),
                description=getattr(model, "description"),
            )

    async def list_all(self) -> list[Tool]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(ToolModel))
            rows = result.scalars().all()
            tools: list[Tool] = []
            for row in rows:
                tools.append(
                    Tool(
                        id=getattr(row, "id"),
                        name=getattr(row, "name"),
                        description=getattr(row, "description"),
                    )
                )
            return tools

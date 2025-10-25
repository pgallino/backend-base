from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.tool import Tool


class ToolRepository(ABC):
    @abstractmethod
    async def get_by_id(self, tool_id: int) -> Optional[Tool]:
        raise NotImplementedError()

    @abstractmethod
    async def create(self, tool: Tool) -> Tool:
        raise NotImplementedError()

    @abstractmethod
    async def list_all(self) -> list[Tool]:
        """Return a list with all tools."""
        raise NotImplementedError()

import pytest

from src.domain.tool_service import ToolService
from src.domain.tool import Tool


class FakeToolRepository:
    def __init__(self):
        self._store = {}
        self._id = 1

    async def get_by_id(self, tool_id):
        return self._store.get(tool_id)

    async def create(self, tool: Tool):
        tool.id = self._id
        self._store[self._id] = tool
        self._id += 1
        return tool

    async def list_all(self):
        return list(self._store.values())

    async def update(self, tool: Tool):
        # Replace existing tool if present
        if tool.id in self._store:
            self._store[tool.id] = tool
            return tool
        return None

    async def delete(self, tool_id: int) -> bool:
        if tool_id in self._store:
            del self._store[tool_id]
            return True
        return False


@pytest.mark.asyncio
async def test_tool_service_create_and_get_and_list():
    repo = FakeToolRepository()
    service = ToolService(tool_repository=repo)

    created = await service.create_tool("fastapi", "web framework", "")
    assert created.id == 1
    assert created.name == "fastapi"

    fetched = await service.get_tool(1)
    assert fetched is not None
    assert fetched.name == "fastapi"

    all_tools = await service.list_tools()
    assert isinstance(all_tools, list)
    assert len(all_tools) == 1


@pytest.mark.asyncio
async def test_tool_service_no_repository_error():
    service = ToolService()
    with pytest.raises(RuntimeError):
        await service.get_tool(1)
    with pytest.raises(RuntimeError):
        await service.create_tool("n", "d", "")
    with pytest.raises(RuntimeError):
        await service.list_tools()


@pytest.mark.asyncio
async def test_tool_service_update_and_delete():
    repo = FakeToolRepository()
    service = ToolService(tool_repository=repo)

    created = await service.create_tool("fastapi", "web framework", "")
    assert created.id == 1

    # Update the tool
    updated = await service.update_tool(created.id, name="fastapi-v2", description="wf", link="https://ex")
    assert updated is not None
    assert updated.name == "fastapi-v2"

    # Delete the tool
    deleted = await service.delete_tool(created.id)
    assert deleted is True

    # Ensure it's gone
    fetched = await service.get_tool(created.id)
    assert fetched is None

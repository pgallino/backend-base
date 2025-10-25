import pytest
from src.adapters.db.models.models import Base, ToolModel
from src.adapters.db.repositories.tool_repository import SqlAlchemyToolRepository
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.domain.tool import Tool


@pytest.mark.asyncio
async def test_sqlalchemy_tool_repository_create_and_list():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    repo = SqlAlchemyToolRepository()
    # Patch module-level session to use our test DB if code expects attribute on instance
    try:
        repo.AsyncSessionLocal = async_session
    except Exception:
        pass

    # Create tool
    tool = Tool(id=0, name="fastapi", description="web framework")
    created = await repo.create(tool)
    assert created.id == 1
    assert created.name == "fastapi"

    # List tools
    all_tools = await repo.list_all()
    assert isinstance(all_tools, list)
    assert len(all_tools) == 1
    assert all_tools[0].name == "fastapi"

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.adapters.db.models.models import Base
from src.adapters.db.repositories.tool_repository import SqlAlchemyToolRepository
from src.domain.tool import Tool


@pytest.mark.asyncio
async def test_get_by_id_and_list_empty_and_update_delete_not_found(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    import importlib

    repo_module = importlib.import_module("src.adapters.db.repositories.tool_repository")
    monkeypatch.setattr(repo_module, "AsyncSessionLocal", async_session)

    repo = SqlAlchemyToolRepository()

    # get_by_id on empty DB
    res = await repo.get_by_id(1)
    assert res is None

    # list_all on empty DB
    all_tools = await repo.list_all()
    assert isinstance(all_tools, list)
    assert len(all_tools) == 0

    # update non-existing tool
    nonexist = Tool(id=999, name="x", description=None, link=None)
    updated = await repo.update(nonexist)
    assert updated is None

    # delete non-existing tool
    deleted = await repo.delete(999)
    assert deleted is False
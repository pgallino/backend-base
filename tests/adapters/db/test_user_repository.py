import pytest
import asyncio
from src.adapters.db.models.models import Base, UserModel
from src.adapters.db.repositories.user_repository import SqlAlchemyUserRepository
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.domain.user import User

@pytest.mark.asyncio
async def test_sqlalchemy_user_repository_create_and_get():
    # Setup in-memory SQLite DB
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    repo = SqlAlchemyUserRepository()
    # Patch session to use our test DB
    repo.AsyncSessionLocal = async_session

    # Create user
    user = User(id=0, username="testuser", name="Test User", email="test@example.com")
    created = await repo.create(user)
    assert created.id == 1
    assert created.username == "testuser"

    # Get user
    fetched = await repo.get_by_id(1)
    assert fetched is not None
    assert fetched.username == "testuser"
    assert fetched.email == "test@example.com"

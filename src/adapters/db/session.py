import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DB_URL = os.getenv("DB_URL_ASYNC", "sqlite+aiosqlite:///./dev.db")

engine = create_async_engine(DB_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

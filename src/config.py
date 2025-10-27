from typing import final

from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    PROJECT_NAME: str = "BackendBase"
    ENVIRONMENT: str = "dev"
    ALLOWED_ORIGINS: str = ""
    # Database URLs
    DB_URL_ASYNC: str = "sqlite+aiosqlite:///./dev.db"
    DB_URL_SYNC: str = "sqlite:///./dev.db"

    # SQLAlchemy echo flag (enable SQL logging). Use env SQL_ECHO=true to enable
    SQL_ECHO: bool = False


settings = Settings()

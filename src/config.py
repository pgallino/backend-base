from typing import final

from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    PROJECT_NAME: str = "BackendBase"
    ENVIRONMENT: str = "dev"


settings = Settings()

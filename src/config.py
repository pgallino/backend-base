import os
from pathlib import Path
from typing import List, Optional, final

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class Settings(BaseSettings):
    # Do NOT load a .env file here. All values must come from the environment.
    model_config = SettingsConfigDict(extra="ignore")

    # All settings are required and must be provided via environment variables.
    PROJECT_NAME: str
    ENVIRONMENT: str
    # ALLOWED_ORIGINS removed: CORS is intentionally disabled by default.

    # Database URLs
    DB_URL_ASYNC: str
    # DB_URL_SYNC is optional at runtime: required only for migration jobs
    # (the `deploy-neon.yml` workflow will pass NEON_DB_SYNC -> DB_URL_SYNC).
    DB_URL_SYNC: Optional[str] = None

    # SQLAlchemy echo flag (enable SQL logging). Provide SQL_ECHO in env (true/false)
    SQL_ECHO: bool = False


# Developer convenience: if a local .env file exists in the repo root, load it
# into the process environment before instantiating Settings. This allows
# developers to keep a local `.env` (ignored by git) for convenience while
# keeping the application code free of defaults.
env_path = Path(".env")
if env_path.exists():
    # load_dotenv does not override existing environment variables by default
    load_dotenv(env_path)


# Recreate settings now that .env may have been loaded
class MissingEnvironmentVariables(RuntimeError):
    """Raised when required environment variables are not present.

    This is raised early (during import) so the application fails fast
    with a clear, actionable message instead of a cryptic validation
    error later on.
    """


def _ensure_required_env_vars(required: List[str]) -> None:
    missing = [v for v in required if not os.environ.get(v)]
    if missing:
        msg_lines = [
            "Missing required environment variables:",
            ", ".join(missing),
            "",
            "To fix locally: copy .env.example -> .env and set the values, or",
            "export the variables in your shell. In CI/production inject the",
            "variables via your secrets manager (GitHub Actions, Render, etc.).",
        ]
        raise MissingEnvironmentVariables("\n".join(msg_lines))


# List the settings names we expect to find in the environment. Keep this in
# sync with the fields defined on `Settings` above.
# Only require the core settings for the app to run; keep CORS optional to
# avoid requiring ALLOWED_ORIGINS configuration during CI and simple dev runs.
_required_env_vars = [
    "PROJECT_NAME",
    "ENVIRONMENT",
    "DB_URL_ASYNC",
]

# Fail fast with a clear message if any required env var is missing.
_ensure_required_env_vars(_required_env_vars)

# Instantiate settings now that we've ensured the environment contains the
# required values. Mypy may still complain about missing constructor args
# because the class declares required attributes, but at runtime the values
# are supplied from the environment; use an inline ignore for the call site.
settings = Settings()  # type: ignore[call-arg]

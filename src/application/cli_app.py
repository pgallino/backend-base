from src.adapters.cli.cli import app as cli_app
from src.application.factory import create_facade
from src.config import settings

# Instantiate facade for the CLI adapter
cli_facade = create_facade(
    project_name=settings.PROJECT_NAME, environment=settings.ENVIRONMENT
)

# Re-export Typer app
app = cli_app

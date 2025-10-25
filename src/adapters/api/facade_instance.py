from src.adapters.api.facade import ApplicationFacade
from src.adapters.db.repositories.tool_repository import SqlAlchemyToolRepository
from src.config import settings

tool_repository = SqlAlchemyToolRepository()
api_facade = ApplicationFacade(
    project_name=settings.PROJECT_NAME,
    environment=settings.ENVIRONMENT,
    tool_repository=tool_repository,
)

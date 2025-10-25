from src.adapters.api.facade import ApplicationFacade
from src.adapters.db.repositories.tool_repository import SqlAlchemyToolRepository
from src.adapters.db.repositories.user_repository import SqlAlchemyUserRepository
from src.config import settings

user_repository = SqlAlchemyUserRepository()
tool_repository = SqlAlchemyToolRepository()
api_facade = ApplicationFacade(
    project_name=settings.PROJECT_NAME,
    environment=settings.ENVIRONMENT,
    user_repository=user_repository,
    tool_repository=tool_repository,
)

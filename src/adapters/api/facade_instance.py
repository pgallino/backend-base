from src.adapters.api.facade import ApplicationFacade
from src.adapters.db.repositories.user_repository import SqlAlchemyUserRepository
from src.config import settings

user_repository = SqlAlchemyUserRepository()
api_facade = ApplicationFacade(
    project_name=settings.PROJECT_NAME,
    environment=settings.ENVIRONMENT,
    user_repository=user_repository,
)

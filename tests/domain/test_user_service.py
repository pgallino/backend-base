from src.domain.user_service import UserService
from src.domain.user import User


def test_user_service_returns_user():
    service = UserService()
    user = service.get_user("BackendBase", "dev")

    assert isinstance(user, User)
    assert user.username == "backendbase_user"
    assert user.email == "backendbase_user@dev.com"

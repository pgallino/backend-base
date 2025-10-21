
import pytest
from src.domain.user_service import UserService
from src.domain.user import User

class FakeUserRepository:
    async def get_by_id(self, user_id):
        return User(id=user_id, username="testuser", name="Test User", email="test@example.com")

    async def create(self, user):
        # Simula creación, retorna el usuario con id asignado
        return User(id=99, username=user.username, name=user.name, email=user.email)

@pytest.mark.asyncio
async def test_user_service_returns_user():
    service = UserService(user_repository=FakeUserRepository())
    user = await service.get_user(42)

    assert isinstance(user, User)
    assert user.id == 42
    assert user.username == "testuser"
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_user_service_create_user():
    service = UserService(user_repository=FakeUserRepository())
    user = await service.create_user("newuser", "Nuevo", "nuevo@example.com")
    assert isinstance(user, User)
    assert user.id == 99
    assert user.username == "newuser"
    assert user.email == "nuevo@example.com"


@pytest.mark.asyncio
async def test_user_service_no_repository_error():
    service = UserService()
    try:
        await service.get_user(1)
    except RuntimeError as e:
        assert "No hay repositorio de usuario" in str(e)
    else:
        assert False, "No lanzó RuntimeError cuando falta el repositorio"

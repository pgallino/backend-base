from typing import final

from .user import User, build_user


@final
class UserService:
    """Fachada del Dominio para el caso de Usuario (User)."""

    def __init__(self, user_repository=None):
        self.user_repository = user_repository

    async def get_user(self, user_id: int) -> User | None:
        """Busca un usuario por id usando el repositorio."""
        if self.user_repository is None:
            raise RuntimeError("No hay repositorio de usuario configurado")
        return await self.user_repository.get_by_id(user_id)

    async def create_user(self, username: str, name: str, email: str) -> User:
        """Crea un usuario usando el repositorio."""
        if self.user_repository is None:
            raise RuntimeError("No hay repositorio de usuario configurado")
        user = User(id=0, username=username, name=name, email=email)
        return await self.user_repository.create(user)

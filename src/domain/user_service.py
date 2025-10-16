from typing import final

from .user import User, build_user


@final
class UserService:
    """Fachada del Dominio para el caso de Usuario (User)."""

    def get_user(self, project_name: str, environment: str) -> User:
        """Devuelve un usuario de ejemplo."""
        return build_user(project_name, environment)

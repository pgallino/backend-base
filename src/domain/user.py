"""
Dominio: user

Define la entidad de dominio `User` como dataclass y un helper para crear
una instancia a partir del nombre del proyecto.
"""

from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    name: str
    email: str

    @classmethod
    def from_project(cls, project_name: str, environment: str) -> "User":
        username = f"{project_name.lower()}_user"
        return cls(
            id=1,
            username=username,
            name=f"{project_name} Default User",
            email=f"{username}@{environment}.com",
        )


def build_user(project_name: str, environment: str) -> User:
    """Compatibilidad: devuelve una instancia de User."""
    return User.from_project(project_name, environment)

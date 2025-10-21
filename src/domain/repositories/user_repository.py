from abc import ABC, abstractmethod
from typing import Optional

from src.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

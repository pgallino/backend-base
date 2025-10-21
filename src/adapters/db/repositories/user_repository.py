from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from src.adapters.db.models.models import UserModel
from src.adapters.db.session import AsyncSessionLocal
from src.domain.repositories.user_repository import UserRepository
from src.domain.user import User


class SqlAlchemyUserRepository(UserRepository):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            user_row = result.scalar_one_or_none()
            if user_row:
                return User(
                    id=getattr(user_row, "id"),
                    username=getattr(user_row, "username"),
                    name=getattr(user_row, "name"),
                    email=getattr(user_row, "email"),
                )
            return None

    async def create(self, user: User) -> User:
        async with AsyncSessionLocal() as session:
            user_model = UserModel(
                username=user.username,
                name=user.name,
                email=user.email,
            )
            session.add(user_model)
            await session.commit()
            await session.refresh(user_model)
            return User(
                id=getattr(user_model, "id"),
                username=getattr(user_model, "username"),
                name=getattr(user_model, "name"),
                email=getattr(user_model, "email"),
            )

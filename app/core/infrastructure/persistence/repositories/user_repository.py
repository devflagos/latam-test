import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.ports.output.user_output_port import UserOutputPort
from app.core.domain.entities.user import User
from app.core.infrastructure.database import async_session_maker
from app.core.infrastructure.persistence.models.user_model import UserModel

logger = logging.getLogger(__name__)


class UserRepository(UserOutputPort):
    def __init__(self) -> None:
        self.session_maker = async_session_maker

    async def _get_session(self) -> AsyncSession:
        async with self.session_maker() as session:
            yield session

    async def save(self, user: User) -> User:
        async with self.session_maker() as session:
            model = UserModel.from_domain(user)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            logger.info(f"User created: {model.id}")
            return model.to_domain()

    async def find_by_id(self, id: UUID) -> Optional[User]:
        async with self.session_maker() as session:
            result = await session.execute(select(UserModel).where(UserModel.id == id))
            model = result.scalar_one_or_none()
            return model.to_domain() if model else None

    async def find_all(self) -> list[User]:
        async with self.session_maker() as session:
            result = await session.execute(select(UserModel))
            models = result.scalars().all()
            return [model.to_domain() for model in models]

    async def find_by_username(self, username: str) -> Optional[User]:
        async with self.session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            model = result.scalar_one_or_none()
            return model.to_domain() if model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        async with self.session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            model = result.scalar_one_or_none()
            return model.to_domain() if model else None

    async def delete(self, id: UUID) -> bool:
        async with self.session_maker() as session:
            result = await session.execute(
                sql_delete(UserModel).where(UserModel.id == id)
            )
            await session.commit()
            deleted = result.rowcount > 0
            if deleted:
                logger.info(f"User deleted: {id}")
            return deleted

    async def update(self, user: User) -> User:
        async with self.session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user.id)
            )
            model = result.scalar_one()
            model.username = user.username
            model.email = user.email
            model.first_name = user.first_name
            model.last_name = user.last_name
            model.role = user.role.value
            model.active = user.active
            await session.commit()
            await session.refresh(model)
            logger.info(f"User updated: {model.id}")
            return model.to_domain()
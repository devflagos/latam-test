import logging
from uuid import UUID

from sqlalchemy import delete as sql_delete
from sqlalchemy import select

from app.core.application.ports.output.user_output_port import UserOutputPort
from app.core.domain.entities.user import User
from app.core.infrastructure.database import async_session_maker
from app.core.infrastructure.persistence.models.user_model import UserModel

logger = logging.getLogger(__name__)


class UserRepository(UserOutputPort):
    def __init__(self) -> None:
        self.session_maker = async_session_maker

    async def save(self, user: User) -> User:
        async with self.session_maker() as session:
            model = UserModel.from_domain(user)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            logger.info(f"User created: {model.id}")
            return model.to_domain()

    async def find_by_id(self, id: UUID) -> User | None:
        async with self.session_maker() as session:
            result = await session.execute(select(UserModel).where(UserModel.id == id))
            model = result.scalar_one_or_none()
            return model.to_domain() if model else None

    async def find_all(
        self, active_only: bool = True, limit: int = 50, offset: int = 0
    ) -> list[User]:
        async with self.session_maker() as session:
            stmt = select(UserModel)
            if active_only:
                stmt = stmt.where(UserModel.active)
            stmt = stmt.limit(limit).offset(offset)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [model.to_domain() for model in models]

    async def find_by_username(self, username: str) -> User | None:
        async with self.session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            model = result.scalar_one_or_none()
            return model.to_domain() if model else None

    async def find_by_email(self, email: str) -> User | None:
        async with self.session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            model = result.scalar_one_or_none()
            return model.to_domain() if model else None

    async def delete(self, id: UUID) -> bool:
        async with self.session_maker() as session:
            await session.execute(sql_delete(UserModel).where(UserModel.id == id))
            await session.commit()
            logger.info(f"User deleted: {id}")
            return True

    async def update(self, user: User) -> User:
        async with self.session_maker() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user.id)
            )
            model = result.scalar_one()
            model_username: str = user.username
            model_email: str = user.email
            model_first_name: str = user.first_name
            model_last_name: str = user.last_name
            model_role: str = user.role.value
            model_active: bool = user.active
            model.username = model_username
            model.email = model_email
            model.first_name = model_first_name
            model.last_name = model_last_name
            model.role = model_role
            model.active = model_active
            await session.commit()
            await session.refresh(model)
            logger.info(f"User updated: {model.id}")
            return model.to_domain()

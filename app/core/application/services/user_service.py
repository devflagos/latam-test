import logging
from typing import Optional
from uuid import UUID

from app.api.v1.schemas.user_create import UserCreate
from app.api.v1.schemas.user_update import UserUpdate
from app.core.application.ports.output.user_output_port import UserOutputPort
from app.core.domain.entities.user import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repository: UserOutputPort) -> None:
        self._repository = repository

    @property
    def repository(self) -> UserOutputPort:
        return self._repository

    async def create_user(self, data: UserCreate) -> User:
        existing = await self._repository.find_by_username(data.username)
        if existing:
            raise ValueError(f"Username '{data.username}' already exists")

        existing_email = await self._repository.find_by_email(data.email)
        if existing_email:
            raise ValueError(f"Email '{data.email}' already exists")

        user = User(
            username=data.username,
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            role=data.role,
            active=data.active,
        )
        return await self._repository.save(user)

    async def get_user(self, user_id: UUID) -> Optional[User]:
        return await self._repository.find_by_id(user_id)

    async def list_users(self, active_only: bool = True) -> list[User]:
        all_users = await self._repository.find_all()
        if active_only:
            return [user for user in all_users if user.active]
        return all_users

    async def update_user(self, user_id: UUID, data: UserUpdate) -> User:
        user = await self._repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with id '{user_id}' not found")

        if data.username is not None and data.username != user.username:
            existing = await self._repository.find_by_username(data.username)
            if existing and existing.id != user.id:
                raise ValueError(f"Username '{data.username}' already exists")
            user.update(username=data.username)

        if data.email is not None and data.email != user.email:
            existing = await self._repository.find_by_email(data.email)
            if existing and existing.id != user.id:
                raise ValueError(f"Email '{data.email}' already exists")
            user.update(email=data.email)

        if data.first_name is not None:
            user.update(first_name=data.first_name)
        if data.last_name is not None:
            user.update(last_name=data.last_name)
        if data.role is not None:
            user.update(role=data.role)
        if data.active is not None:
            user.update(active=data.active)

        return await self._repository.update(user)

    async def delete_user(self, user_id: UUID) -> bool:
        user = await self._repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with id '{user_id}' not found")
        return await self._repository.delete(user_id)

    async def deactivate_user(self, user_id: UUID) -> User:
        user = await self._repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with id '{user_id}' not found")
        user.deactivate()
        return await self._repository.update(user)
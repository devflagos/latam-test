from abc import ABC, abstractmethod
from uuid import UUID

from app.core.domain.entities.user import User


class UserOutputPort(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_id(self, id: UUID) -> User | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[User]:
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

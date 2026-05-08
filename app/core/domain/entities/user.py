from enum import Enum
from typing import Optional
from uuid import UUID

from app.core.domain.entities.entity import Entity


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(Entity):
    def __init__(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        role: UserRole = UserRole.USER,
        active: bool = True,
        id: Optional[UUID] = None,
    ) -> None:
        super().__init__(id)
        self._username = username
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._role = role
        self._active = active

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def role(self) -> UserRole:
        return self._role

    @property
    def active(self) -> bool:
        return self._active

    def update(
        self,
        username: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        role: Optional[UserRole] = None,
        active: Optional[bool] = None,
    ) -> None:
        if username is not None:
            self._username = username
        if email is not None:
            self._email = email
        if first_name is not None:
            self._first_name = first_name
        if last_name is not None:
            self._last_name = last_name
        if role is not None:
            self._role = role
        if active is not None:
            self._active = active
        self._set_updated_at()

    def deactivate(self) -> None:
        self._active = False
        self._set_updated_at()

    def activate(self) -> None:
        self._active = True
        self._set_updated_at()
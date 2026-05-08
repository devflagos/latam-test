import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.domain.entities.user import User, UserRole
from app.core.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    username: Mapped[String] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[String] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    first_name: Mapped[String] = mapped_column(String(100), nullable=False)
    last_name: Mapped[String] = mapped_column(String(100), nullable=False)
    role: Mapped[String] = mapped_column(
        String(20), nullable=False, default=UserRole.USER.value
    )
    active: Mapped[Boolean] = mapped_column(Boolean, nullable=False, default=True)

    def to_domain(self) -> "User":
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            role=UserRole(self.role),
            active=self.active,
        )

    @classmethod
    def from_domain(cls, user: "User") -> "UserModel":
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role.value,
            active=user.active,
        )

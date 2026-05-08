from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.infrastructure.database import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[PG_UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

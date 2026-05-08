from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.domain.entities.user import UserRole


class UserResponse(BaseModel):
    id: UUID = Field(..., description="User's unique id")
    username: str = Field(..., description="User's unique username")
    email: str = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    role: UserRole = Field(..., description="User role")
    active: bool = Field(..., description="Whether user is active")
    created_at: datetime = Field(..., description="Timestamp when user was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when user was last updated"
    )

    model_config = {"from_attributes": True}

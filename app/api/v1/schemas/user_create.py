from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.domain.entities.user import UserRole


class UserCreate(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="User's unique username"
    )
    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(
        ..., min_length=1, max_length=100, description="User's first name"
    )
    last_name: str = Field(
        ..., min_length=1, max_length=100, description="User's last name"
    )
    role: UserRole = Field(default=UserRole.USER, description="User role")
    active: bool = Field(default=True, description="Whether user is active")

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def name_no_special_chars(cls, v: str) -> str:
        if not v.replace(" ", "").replace("-", "").replace("'", "").isalpha():
            raise ValueError("Name must contain only letters")
        return v

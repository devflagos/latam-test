from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.domain.entities.user import UserRole


class UserUpdate(BaseModel):
    username: str | None = Field(
        None, min_length=3, max_length=50, description="User's unique username"
    )
    email: EmailStr | None = Field(None, description="User's email address")
    first_name: str | None = Field(
        None, min_length=1, max_length=100, description="User's first name"
    )
    last_name: str | None = Field(
        None, min_length=1, max_length=100, description="User's last name"
    )
    role: UserRole | None = Field(None, description="User role")
    active: bool | None = Field(None, description="Whether user is active")

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str | None) -> str | None:
        if v is not None and not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def name_no_special_chars(cls, v: str | None) -> str | None:
        if (
            v is not None
            and not v.replace(" ", "").replace("-", "").replace("'", "").isalpha()
        ):
            raise ValueError("Name must contain only letters")
        return v

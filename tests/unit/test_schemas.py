import pytest
from pydantic import ValidationError

from app.api.v1.schemas.user_create import UserCreate
from app.api.v1.schemas.user_update import UserUpdate
from app.api.v1.schemas.user_response import UserResponse
from app.core.domain.entities.user import UserRole


class TestUserCreateSchema:
    def test_valid_user_create(self):
        user = UserCreate(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.role == UserRole.USER
        assert user.active is True

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreate(
                username="testuser",
                email="not-an-email",
                first_name="John",
                last_name="Doe",
            )

    def test_short_username(self):
        with pytest.raises(ValidationError):
            UserCreate(
                username="ab",
                email="test@example.com",
                first_name="John",
                last_name="Doe",
            )

    def test_custom_role(self):
        user = UserCreate(
            username="admin",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
        )
        assert user.role == UserRole.ADMIN

    def test_custom_active(self):
        user = UserCreate(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            active=False,
        )
        assert user.active is False


class TestUserUpdateSchema:
    def test_partial_update(self):
        user = UserUpdate(first_name="Jane")
        assert user.first_name == "Jane"
        assert user.last_name is None

    def test_all_fields_optional(self):
        user = UserUpdate()
        assert user.username is None
        assert user.email is None


class TestUserResponseSchema:
    def test_user_response_from_dict(self):
        data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "user",
            "active": True,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }
        response = UserResponse(**data)
        assert response.username == "testuser"
        assert response.active is True
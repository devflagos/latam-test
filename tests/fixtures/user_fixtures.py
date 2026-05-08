from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.api.v1.schemas.user_create import UserCreate
from app.api.v1.schemas.user_update import UserUpdate
from app.core.domain.entities.user import User, UserRole


@pytest.fixture
def sample_user_id():
    return uuid4()


@pytest.fixture
def sample_user(sample_user_id):
    return User(
        id=sample_user_id,
        username="testuser",
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        role=UserRole.USER,
        active=True,
    )


@pytest.fixture
def mock_user_repository():
    repo = MagicMock()
    repo.save = AsyncMock()
    repo.find_by_id = AsyncMock()
    repo.find_all = AsyncMock()
    repo.find_by_username = AsyncMock()
    repo.find_by_email = AsyncMock()
    repo.delete = AsyncMock()
    repo.update = AsyncMock()
    return repo


@pytest.fixture
def user_create_data():
    return UserCreate(
        username="newuser",
        email="new@example.com",
        first_name="New",
        last_name="User",
        role=UserRole.USER,
        active=True,
    )


@pytest.fixture
def user_update_data():
    return UserUpdate(
        first_name="Updated",
        last_name="Name",
    )

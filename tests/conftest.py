import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from uuid import uuid4

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
    repo.save = MagicMock()
    repo.find_by_id = MagicMock()
    repo.find_all = MagicMock()
    repo.find_by_username = MagicMock()
    repo.find_by_email = MagicMock()
    repo.delete = MagicMock()
    repo.update = MagicMock()
    return repo


@pytest.fixture
def user_create_data():
    from app.api.v1.schemas.user_create import UserCreate
    return UserCreate(
        username="newuser",
        email="new@example.com",
        first_name="New",
        last_name="User",
    )


@pytest.fixture
def user_update_data():
    from app.api.v1.schemas.user_update import UserUpdate
    return UserUpdate(first_name="Updated", last_name="Name")
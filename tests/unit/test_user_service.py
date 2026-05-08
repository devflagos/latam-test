from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.api.v1.schemas.user_create import UserCreate
from app.api.v1.schemas.user_update import UserUpdate
from app.core.application.services.user_service import UserService
from app.core.domain.entities.user import User, UserRole


class TestUserService:
    @pytest.fixture
    def sample_user_id(self):
        return uuid4()

    @pytest.fixture
    def sample_user(self, sample_user_id):
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
    def mock_user_repository(self):
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
    def user_create_data(self):
        return UserCreate(
            username="newuser",
            email="new@example.com",
            first_name="New",
            last_name="User",
            role=UserRole.USER,
            active=True,
        )

    @pytest.fixture
    def user_update_data(self):
        return UserUpdate(
            first_name="Updated",
            last_name="Name",
        )

    @pytest.mark.asyncio
    async def test_create_user_success(self, mock_user_repository, user_create_data):
        mock_user_repository.find_by_username = AsyncMock(return_value=None)
        mock_user_repository.find_by_email = AsyncMock(return_value=None)
        mock_user_repository.save = AsyncMock()

        service = UserService(mock_user_repository)
        result = await service.create_user(user_create_data)

        mock_user_repository.save.assert_called_once()
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_user_duplicate_username(
        self, mock_user_repository, user_create_data
    ):
        existing_user = User(
            username=user_create_data.username,
            email="other@example.com",
            first_name="Other",
            last_name="User",
        )
        mock_user_repository.find_by_username = AsyncMock(return_value=existing_user)

        service = UserService(mock_user_repository)

        with pytest.raises(
            ValueError, match=f"Username '{user_create_data.username}' already exists"
        ):
            await service.create_user(user_create_data)

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(
        self, mock_user_repository, user_create_data
    ):
        existing_user = User(
            username="otheruser",
            email=user_create_data.email,
            first_name="Other",
            last_name="User",
        )
        mock_user_repository.find_by_username = AsyncMock(return_value=None)
        mock_user_repository.find_by_email = AsyncMock(return_value=existing_user)

        service = UserService(mock_user_repository)

        with pytest.raises(
            ValueError, match=f"Email '{user_create_data.email}' already exists"
        ):
            await service.create_user(user_create_data)

    @pytest.mark.asyncio
    async def test_get_user_found(self, mock_user_repository, sample_user):
        mock_user_repository.find_by_id = AsyncMock(return_value=sample_user)

        service = UserService(mock_user_repository)
        result = await service.get_user(sample_user.id)

        assert result == sample_user
        mock_user_repository.find_by_id.assert_called_once_with(sample_user.id)

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, mock_user_repository, sample_user_id):
        mock_user_repository.find_by_id = AsyncMock(return_value=None)

        service = UserService(mock_user_repository)
        result = await service.get_user(sample_user_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_list_users_active_only(self, mock_user_repository, sample_user):
        inactive_user = User(
            username="inactive",
            email="inactive@example.com",
            first_name="Inactive",
            last_name="User",
            active=False,
        )

        async def mock_find_all(active_only=True, limit=50, offset=0):
            if active_only:
                return [sample_user]
            return [sample_user, inactive_user]

        mock_user_repository.find_all = AsyncMock(side_effect=mock_find_all)

        service = UserService(mock_user_repository)
        result = await service.list_users(active_only=True)

        assert len(result) == 1
        assert result[0].active is True

    @pytest.mark.asyncio
    async def test_list_users_all(self, mock_user_repository, sample_user):
        inactive_user = User(
            username="inactive",
            email="inactive@example.com",
            first_name="Inactive",
            last_name="User",
            active=False,
        )

        async def mock_find_all(active_only=True, limit=50, offset=0):
            if active_only:
                return [sample_user]
            return [sample_user, inactive_user]

        mock_user_repository.find_all = AsyncMock(side_effect=mock_find_all)

        service = UserService(mock_user_repository)
        result = await service.list_users(active_only=False)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_list_users_empty(self, mock_user_repository):
        async def mock_find_all(active_only=True, limit=50, offset=0):
            return []

        mock_user_repository.find_all = AsyncMock(side_effect=mock_find_all)

        service = UserService(mock_user_repository)
        result = await service.list_users()

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_update_user_success(
        self, mock_user_repository, sample_user, user_update_data
    ):
        mock_user_repository.find_by_id = AsyncMock(return_value=sample_user)
        mock_user_repository.update = AsyncMock(return_value=sample_user)

        service = UserService(mock_user_repository)
        await service.update_user(sample_user.id, user_update_data)

        mock_user_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_not_found(
        self, mock_user_repository, sample_user_id, user_update_data
    ):
        mock_user_repository.find_by_id = AsyncMock(return_value=None)

        service = UserService(mock_user_repository)

        with pytest.raises(
            ValueError, match=f"User with id '{sample_user_id}' not found"
        ):
            await service.update_user(sample_user_id, user_update_data)

    @pytest.mark.asyncio
    async def test_update_user_username_already_exists(
        self, mock_user_repository, sample_user
    ):
        existing_user = User(
            username="existing",
            email="existing@example.com",
            first_name="Existing",
            last_name="User",
        )
        mock_user_repository.find_by_id = AsyncMock(return_value=sample_user)
        mock_user_repository.find_by_username = AsyncMock(return_value=existing_user)

        service = UserService(mock_user_repository)
        update_data = UserUpdate(username="existing")

        with pytest.raises(ValueError, match="Username 'existing' already exists"):
            await service.update_user(sample_user.id, update_data)

    @pytest.mark.asyncio
    async def test_deactivate_user_success(self, mock_user_repository, sample_user):
        mock_user_repository.find_by_id = AsyncMock(return_value=sample_user)
        mock_user_repository.update = AsyncMock(return_value=sample_user)

        service = UserService(mock_user_repository)
        await service.deactivate_user(sample_user.id)

        mock_user_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_deactivate_user_not_found(
        self, mock_user_repository, sample_user_id
    ):
        mock_user_repository.find_by_id = AsyncMock(return_value=None)

        service = UserService(mock_user_repository)

        with pytest.raises(
            ValueError, match=f"User with id '{sample_user_id}' not found"
        ):
            await service.deactivate_user(sample_user_id)

    @pytest.mark.asyncio
    async def test_delete_user_success(self, mock_user_repository, sample_user):
        mock_user_repository.find_by_id = AsyncMock(return_value=sample_user)
        mock_user_repository.delete = AsyncMock(return_value=True)

        service = UserService(mock_user_repository)
        result = await service.delete_user(sample_user.id)

        assert result is True
        mock_user_repository.delete.assert_called_once_with(sample_user.id)

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, mock_user_repository, sample_user_id):
        mock_user_repository.find_by_id = AsyncMock(return_value=None)

        service = UserService(mock_user_repository)

        with pytest.raises(
            ValueError, match=f"User with id '{sample_user_id}' not found"
        ):
            await service.delete_user(sample_user_id)

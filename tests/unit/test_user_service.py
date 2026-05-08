from unittest.mock import AsyncMock

import pytest

from app.core.application.services.user_service import UserService
from app.core.domain.entities.user import User


class TestUserService:
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
    async def test_list_users(self, mock_user_repository, sample_user):
        mock_user_repository.find_all = AsyncMock(return_value=[sample_user])

        service = UserService(mock_user_repository)
        result = await service.list_users()

        assert len(result) == 1
        assert result[0] == sample_user

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

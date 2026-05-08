import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas import UserCreate, UserResponse, UserUpdate
from app.core.application.services.user_service import UserService
from app.core.infrastructure.persistence.repositories.user_repository import (
    UserRepository,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

user_repository = UserRepository()
user_service = UserService(user_repository)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate):
    try:
        user = await user_service.create_user(data)
        return UserResponse.model_validate(user)
    except ValueError as e:
        logger.warning(f"User creation failed: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID):
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
async def list_users(active_only: bool = True):
    users = await user_service.list_users(active_only=active_only)
    return [UserResponse.model_validate(user) for user in users]


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, data: UserUpdate):
    try:
        user = await user_service.update_user(user_id, data)
        return UserResponse.model_validate(user)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: UUID):
    try:
        user = await user_service.deactivate_user(user_id)
        return UserResponse.model_validate(user)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

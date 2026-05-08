from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.domain.entities.user import User
from app.main import app


@pytest.fixture
async def mock_user_repository():
    repo = MagicMock()
    users_db = {}

    async def mock_save(user):
        user_id = user.id or uuid4()
        user_data = {
            "id": user_id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value if hasattr(user.role, "value") else user.role,
            "active": user.active,
        }
        users_db[str(user_id)] = user_data
        return User(**user_data)

    async def mock_find_by_id(user_id):
        user_data = users_db.get(str(user_id))
        if user_data:
            return User(**user_data)
        return None

    async def mock_find_all(active_only=True, limit=50, offset=0):
        users = [User(**u) for u in users_db.values()]
        if active_only:
            users = [u for u in users if u.active]
        return users[offset : offset + limit]

    async def mock_find_by_username(username):
        for u in users_db.values():
            if u["username"] == username:
                return User(**u)
        return None

    async def mock_find_by_email(email):
        for u in users_db.values():
            if u["email"] == email:
                return User(**u)
        return None

    async def mock_update(user):
        user_id = str(user.id)
        if user_id in users_db:
            role = user.role.value if hasattr(user.role, "value") else user.role
            users_db[user_id].update(
                {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": role,
                    "active": user.active,
                }
            )
        return User(**users_db[user_id])

    async def mock_delete(user_id):
        if str(user_id) in users_db:
            del users_db[str(user_id)]
            return True
        return False

    repo.save = mock_save
    repo.find_by_id = mock_find_by_id
    repo.find_all = mock_find_all
    repo.find_by_username = mock_find_by_username
    repo.find_by_email = mock_find_by_email
    repo.update = mock_update
    repo.delete = mock_delete
    return repo


@pytest.fixture
async def client(mock_user_repository):
    from app.api.v1.users import user_repository, user_service

    user_repository.save = mock_user_repository.save
    user_repository.find_by_id = mock_user_repository.find_by_id
    user_repository.find_all = mock_user_repository.find_all
    user_repository.find_by_username = mock_user_repository.find_by_username
    user_repository.find_by_email = mock_user_repository.find_by_email
    user_repository.update = mock_user_repository.update
    user_repository.delete = mock_user_repository.delete
    user_service._repository = mock_user_repository

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_user_success(client):
    payload = {
        "username": "newuser",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "User",
        "role": "user",
        "active": True,
    }
    response = await client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_user_invalid_email(client):
    payload = {
        "username": "baduser",
        "email": "not-an-email",
        "first_name": "Bad",
        "last_name": "User",
    }
    response = await client.post("/users", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_short_username(client):
    payload = {
        "username": "ab",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
    }
    response = await client.post("/users", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_duplicate_username(client):
    payload = {
        "username": "duplicate",
        "email": "first@example.com",
        "first_name": "First",
        "last_name": "User",
    }
    await client.post("/users", json=payload)

    payload["email"] = "second@example.com"
    response = await client.post("/users", json=payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_users(client):
    response = await client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_list_users_with_inactive(client):
    response = await client.get("/users", params={"active_only": "false"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id(client):
    create_payload = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
    }
    create_response = await client.post("/users", json=create_payload)
    user_id = create_response.json()["id"]

    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(client):
    create_payload = {
        "username": "updateuser",
        "email": "update@test.com",
        "first_name": "Update",
        "last_name": "User",
    }
    create_response = await client.post("/users", json=create_payload)
    user_id = create_response.json()["id"]

    update_payload = {"first_name": "UpdatedName"}
    response = await client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["first_name"] == "UpdatedName"


@pytest.mark.asyncio
async def test_delete_user_soft(client):
    create_payload = {
        "username": "deleteuser",
        "email": "delete@test.com",
        "first_name": "Delete",
        "last_name": "User",
    }
    create_response = await client.post("/users", json=create_payload)
    user_id = create_response.json()["id"]

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["active"] is False


@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_get_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_get_ready(client):
    response = await client.get("/ready")
    assert response.status_code == 200

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
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
    response = await client.get(
        "/users/00000000-0000-0000-0000-000000000000"
    )
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
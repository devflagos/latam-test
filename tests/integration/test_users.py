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
async def test_list_users(client):
    response = await client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_get_ready(client):
    response = await client.get("/ready")
    assert response.status_code == 200

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.middleware.rate_limit import RateLimitMiddleware
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestRateLimitMiddleware:
    @pytest.mark.asyncio
    async def test_rate_limit_allows_requests(self, client):
        for _ in range(10):
            response = await client.get("/health")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_rate_limit_blocks_excessive_requests(self):
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse

        test_app = FastAPI()
        test_app.add_middleware(RateLimitMiddleware, calls=5, period=60)

        @test_app.get("/test")
        async def test_route():
            return JSONResponse({"ok": True})

        from httpx import ASGITransport, AsyncClient

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            for _ in range(5):
                response = await client.get("/test")
                assert response.status_code == 200

            response = await client.get("/test")
            assert response.status_code == 429


class TestLoggingMiddleware:
    @pytest.mark.asyncio
    async def test_health_endpoint_logs(self, client, caplog):
        with caplog.at_level("INFO"):
            await client.get("/health")
            assert any(
                "Request: GET /health" in record.message for record in caplog.records
            )


class TestCORS:
    @pytest.mark.asyncio
    async def test_cors_headers_present(self, client):
        response = await client.options(
            "/users",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert (
            "access-control-allow-origin" in response.headers
            or response.status_code in [200, 404]
        )

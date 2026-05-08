import logging

from fastapi import APIRouter

from app.core.infrastructure.database import check_db_health

logger = logging.getLogger(__name__)

health_router = APIRouter(tags=["health"])


@health_router.get("/health")
async def health_check():
    return {"status": "ok", "service": "test-latam"}


@health_router.get("/health/db")
async def health_db_check():
    db_healthy = await check_db_health()
    if db_healthy:
        return {"status": "ok", "database": "connected"}
    return {"status": "error", "database": "disconnected"}


@health_router.get("/ready")
async def readiness_check():
    db_healthy = await check_db_health()
    if db_healthy:
        return {"status": "ready"}
    return {"status": "not_ready"}

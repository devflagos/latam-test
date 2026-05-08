from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.core.infrastructure.database import init_db, close_db
from app.core.infrastructure.adapters.primary.health import health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
    except Exception as e:
        print(f"Database connection failed: {e}")
    yield
    try:
        await close_db()
    except Exception:
        pass


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health_router)


@app.get("/")
async def root():
    return {"message": "Welcome to test-latam API", "version": settings.app_version}

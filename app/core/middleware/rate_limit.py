import logging
import time
from collections import defaultdict
from typing import Any, Protocol

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class CallNext(Protocol):
    async def __call__(self, request: Request) -> Response: ...


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware to prevent abuse."""

    def __init__(self, app: Any, calls: int = 60, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: dict = defaultdict(list)

    async def dispatch(self, request: Request, call_next: CallNext) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        self.clients[client_ip] = [
            t for t in self.clients[client_ip] if current_time - t <= self.period
        ]

        if len(self.clients[client_ip]) >= self.calls:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={"Retry-After": str(self.period)},
            )

        self.clients[client_ip].append(current_time)
        response = await call_next(request)
        return response

import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        logger.info(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {duration:.3f}s"
        )

        return response
"""
FastAPI Application Entry Point

- Initializes app
- Registers middleware
- Loads routes
"""

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger  # fixed import
from app.api.v1.router import api_router
from app.middleware.logging_middleware import LoggingMiddleware  # fixed path


# ==============================
# APP INITIALIZATION
# ==============================

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)


# ==============================
# MIDDLEWARE
# ==============================

# Logging middleware (request tracking)
app.add_middleware(LoggingMiddleware)


# ==============================
# ROUTES
# ==============================

# Include API routes (ONLY ONCE)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# ==============================
# ROOT ENDPOINT
# ==============================

@app.get("/")
def root():
    logger.info("root_endpoint_called")

    return {
        "message": "Backend is running",
        "status": "ok"
    }
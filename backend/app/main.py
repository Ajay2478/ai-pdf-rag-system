from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router


# Initialize logging
setup_logging()

app = FastAPI(title=settings.APP_NAME)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Backend running is running bro!"}
from fastapi import APIRouter
from app.api.v1.endpoints import health
from app.api.v1.endpoints import health, test_db
from app.api.v1.endpoints import health, auth
from app.api.v1.endpoints import upload
from app.api.v1.endpoints import search
from app.api.v1.endpoints import chat

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(test_db.router, prefix="/test-db", tags=["test"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
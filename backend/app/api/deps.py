from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import decode_access_token
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

security = HTTPBearer()


# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get current user from token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    # Extract token
    token = credentials.credentials

    # Decode token
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Extract user_id safely
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid user ID in token")

    # Fetch user
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
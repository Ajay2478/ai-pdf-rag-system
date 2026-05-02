from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_token_for_user,
)
from app.api.deps import get_db

router = APIRouter()


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, data.email, data.password, data.full_name)
        return {"message": "User created", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token_for_user(user)

    return {"access_token": token}
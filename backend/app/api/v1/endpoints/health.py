from fastapi import APIRouter
from app.api.deps import get_current_user
from fastapi import Depends

router = APIRouter()


@router.get("/")
def health_check():
    return {"status": "ok"}

@router.get("/protected")
def protected(user = Depends(get_current_user)):
    return {"message": f"Hello user {user.id}"}
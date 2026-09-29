from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.schemas import UserRegister, UserResponse
from app.modules.auth.service import register_user


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)


@router.post("/register", response_model=UserResponse, status_code= status.HTTP_201_CREATED,)

def register (
    data:UserRegister,
    db: Session = Depends(get_db)
):
    try:
        return register_user(data, db)
    except ValueError as exc:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exc),
    ) from exc
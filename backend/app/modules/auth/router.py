from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.schemas import (
    LoginRequest,
    TokenResponse,
    UserRegister,
    UserResponse,
)
from app.modules.auth.service import (
    authenticate_user,
    create_login_token,
    register_user,
)


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

@router.post("/login", response_model=TokenResponse,)

def login(
    data: LoginRequest, db: Session = Depends(get_db),
):
    user = authenticate_user(data, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
        )

    access_token = create_login_token(user)

    return {
        "access_token": access_token,
        "token_type":"bearer"
    }
    

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    Token,
)
from backend.app.services.user_service import (
    create_user,
    authenticate_user,
)
from backend.app.core.jwt import create_access_token
from backend.app.core.dependencies import get_current_user
from backend.app.infrastructure.database.database import get_db
from backend.app.infrastructure.database.user_model import User

router = APIRouter()


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = create_user(
        db,
        user.email,
        user.password,
    )

    return {
        "id": db_user.id,
        "email": db_user.email,
    }


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    db_user = authenticate_user(
        db,
        user.email,
        user.password,
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }
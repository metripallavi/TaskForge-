from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.core.jwt import create_access_token
from backend.app.infrastructure.database.database import get_db
from backend.app.infrastructure.database.user_model import User
from backend.app.schemas.user_schema import (
    Token,
    UserCreate,
)
from backend.app.services.user_service import (
    authenticate_user,
    create_user,
)

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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token({"sub": db_user.email})

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

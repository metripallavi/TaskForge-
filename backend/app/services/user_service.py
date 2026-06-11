from sqlalchemy.orm import Session

from backend.app.core.security import (
    hash_password,
    verify_password,
)
from backend.app.infrastructure.database.user_model import User


def create_user(
    db: Session,
    email: str,
    password: str,
) -> User:
    """
    Create a new user with a hashed password.
    """

    user = User(
        email=email,
        hashed_password=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    """
    Verify user credentials.
    Returns the user if valid, otherwise None.
    """

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user
git commit -m "Phase 08: Apply linting, formatting, and CI stabilization (Ruff + Black + MyPy)"
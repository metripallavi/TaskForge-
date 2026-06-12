from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.infrastructure.database.database import SessionLocal

router = APIRouter()


@router.get(
    "",
    summary="Application Health Check",
    description="Returns the health status of the TaskForge API.",
)
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@router.get(
    "/db",
    summary="Database Health Check",
    description="Checks PostgreSQL database connectivity.",
)
def database_health_check() -> dict[str, str]:
    db: Session = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
        }
    finally:
        db.close()
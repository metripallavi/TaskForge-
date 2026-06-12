from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.core.settings import settings
from backend.app.infrastructure.database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="""
    TaskForge is a task management backend built with FastAPI,
    PostgreSQL, JWT Authentication, RBAC, Docker, and Clean Architecture.
    """,
)


@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Returns basic information about the TaskForge API.",
)
def root() -> dict[str, str]:
    return {
        "project": settings.app_name,
        "version": settings.version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


app.include_router(api_router)

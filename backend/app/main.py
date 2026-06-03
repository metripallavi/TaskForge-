from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.core.settings import settings
from backend.app.infrastructure.database import models
from backend.app.infrastructure.database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {"message": "Welcome to TaskForge"}


app.include_router(api_router)
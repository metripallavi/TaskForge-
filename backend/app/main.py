from fastapi import FastAPI

from app.api.router import api_router
from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {"message": "Welcome to TaskForge"}


app.include_router(api_router)

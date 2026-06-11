from fastapi import APIRouter

from backend.app.api.v1.admin import router as admin_router
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.endpoints.health import router as health_router
from backend.app.api.v1.endpoints.tasks import router as tasks_router

router = APIRouter()

router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)

router.include_router(
    tasks_router,
    prefix="/tasks",
    tags=["Tasks"],
)

router.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"],
)
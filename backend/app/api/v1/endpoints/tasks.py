from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.application.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

from backend.app.application.services.task_service import TaskService
from backend.app.infrastructure.database.database import get_db
from backend.app.infrastructure.repositories.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)

from backend.app.core.dependencies import (
    get_current_user,
    require_role,
)

from backend.app.infrastructure.database.user_model import User

router = APIRouter()


# =========================
# CREATE TASK (AUTH REQUIRED)
# =========================
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = SQLAlchemyTaskRepository(db)
    service = TaskService(repository)

    task = service.create_task(payload)

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
    )


# =========================
# LIST TASKS (AUTH REQUIRED)
# =========================
@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = SQLAlchemyTaskRepository(db)
    service = TaskService(repository)

    tasks = service.list_tasks()

    return [
        TaskResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            completed=t.completed,
            created_at=t.created_at,
        )
        for t in tasks
    ]


# =========================
# GET TASK (AUTH REQUIRED)
# =========================
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = SQLAlchemyTaskRepository(db)
    service = TaskService(repository)

    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
    )


# =========================
# UPDATE TASK (AUTH REQUIRED)
# =========================
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = SQLAlchemyTaskRepository(db)
    service = TaskService(repository)

    task = service.update_task(task_id, payload)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at,
    )


# =========================
# DELETE TASK (ADMIN ONLY)
# =========================
@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    repository = SQLAlchemyTaskRepository(db)
    service = TaskService(repository)

    service.delete_task(task_id)

    return {"message": "Task deleted"}
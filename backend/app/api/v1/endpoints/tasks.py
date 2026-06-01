from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.application.services.task_service import TaskService
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.sqlalchemy_task_repository import (
    SQLAlchemyTaskRepository,
)

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=201,
)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskResponse:
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


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
) -> list[TaskResponse]:
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


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
) -> TaskResponse:
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


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
) -> TaskResponse:
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


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    repository = SQLAlchemyTaskRepository(db)
    service = TaskService(repository)

    service.delete_task(task_id)

    return {"message": "Task deleted"}

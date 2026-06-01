from datetime import datetime
from uuid import uuid4

from app.application.schemas.task import (
    TaskCreate,
    TaskUpdate,
)
from app.domain.entities.task import Task
from app.domain.repositories.task_repository import (
    TaskRepository,
)


class TaskService:
    def __init__(
        self,
        repository: TaskRepository,
    ) -> None:
        self.repository = repository

    def create_task(
        self,
        payload: TaskCreate,
    ) -> Task:
        task = Task(
            id=uuid4(),
            title=payload.title,
            description=payload.description,
            completed=False,
            created_at=datetime.utcnow(),
        )

        return self.repository.create(task)

    def get_task(
        self,
        task_id: str,
    ) -> Task | None:
        return self.repository.get_by_id(task_id)

    def list_tasks(self) -> list[Task]:
        return self.repository.list()

    def update_task(
        self,
        task_id: str,
        payload: TaskUpdate,
    ) -> Task | None:
        task = self.repository.get_by_id(task_id)

        if task is None:
            return None

        if payload.title is not None:
            task.title = payload.title

        if payload.description is not None:
            task.description = payload.description

        if payload.completed is not None:
            task.completed = payload.completed

        return self.repository.update(task)

    def delete_task(
        self,
        task_id: str,
    ) -> None:
        self.repository.delete(task_id)

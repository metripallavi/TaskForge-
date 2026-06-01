from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.entities.task import Task
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.database.models import TaskModel


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, task: Task) -> Task:
        db_task = TaskModel(
            id=str(task.id),
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
        )

        self.db.add(db_task)
        self.db.commit()

        return task

    def get_by_id(self, task_id: str) -> Task | None:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

        if db_task is None:
            return None

        return Task(
            id=UUID(db_task.id),
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            created_at=db_task.created_at,
        )

    def list(self) -> list[Task]:
        db_tasks = self.db.query(TaskModel).all()

        return [
            Task(
                id=UUID(task.id),
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
            )
            for task in db_tasks
        ]

    def update(self, task: Task) -> Task:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == str(task.id)).first()

        if db_task:
            db_task.title = task.title
            db_task.description = task.description
            db_task.completed = task.completed

            self.db.commit()

        return task

    def delete(self, task_id: str) -> None:
        db_task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

        if db_task:
            self.db.delete(db_task)
            self.db.commit()

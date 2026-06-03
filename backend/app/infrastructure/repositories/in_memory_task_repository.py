from backend.app.domain.entities.task import Task
from backend.app.domain.repositories.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}

    def create(self, task: Task) -> Task:
        self.tasks[str(task.id)] = task
        return task

    def get_by_id(self, task_id: str) -> Task | None:
        return self.tasks.get(task_id)

    def list(self) -> list[Task]:
        return list(self.tasks.values())

    def update(self, task: Task) -> Task:
        self.tasks[str(task.id)] = task
        return task

    def delete(self, task_id: str) -> None:
        self.tasks.pop(task_id, None)

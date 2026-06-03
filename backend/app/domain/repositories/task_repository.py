from abc import ABC, abstractmethod

from backend.app.domain.entities.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task | None:
        pass

    @abstractmethod
    def list(self) -> list[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: str) -> None:
        pass

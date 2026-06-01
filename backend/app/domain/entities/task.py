from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Task:
    id: UUID
    title: str
    description: str
    completed: bool
    created_at: datetime

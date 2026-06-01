from sqlalchemy import Boolean, Column, DateTime, String

from app.infrastructure.database.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String, nullable=False)

    completed = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        nullable=False,
    )

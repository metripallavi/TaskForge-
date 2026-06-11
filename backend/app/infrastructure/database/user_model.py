import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String

from backend.app.infrastructure.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    role = Column(String, nullable=False, default="user")

    created_at = Column(DateTime, default=datetime.utcnow)

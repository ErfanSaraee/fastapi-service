import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    expenses = relationship(
        "Expense", back_populates="user", cascade="all, delete-orphan")

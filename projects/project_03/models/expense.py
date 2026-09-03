import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    description = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
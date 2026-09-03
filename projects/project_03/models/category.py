from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(150), nullable=True)

    expenses = relationship("Expense", back_populates="category")
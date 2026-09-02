from sqlalchemy import (
    Column, Integer, String, Boolean, Float, Numeric, Date,
    DateTime, Time, Text, Interval, Enum, ARRAY, JSON, ForeignKey, LargeBinary, UUID
)
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum
from datetime import datetime


class RelationsTable(Base):
    __tablename__ = "users"

    # One-to-one relationship
    profile = relationship("Profile", uselist=False, back_populates="user")

    # One-to-many relationship
    addresses = relationship("Address", back_populates="user")

    # Many-to-one relationship
    orders = relationship("Order", back_populates="user")

    # Many-to-many relationship
    roles = relationship("Role", secondary="user_roles",
                         back_populates="users")


class UserType(PythonEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class SampleModel(Base):
    __tablename__ = "sample_model"

    id = Column(Integer, primary_key=True)
    string_field = Column(String(100))
    text_field = Column(Text)
    boolean_field = Column(Boolean)
    integer_field = Column(Integer)
    float_field = Column(Float)
    numeric_field = Column(Numeric(10, 2))
    date_field = Column(Date)
    datetime_field = Column(DateTime)
    time_field = Column(Time)
    interval_field = Column(Interval)
    enum_field = Column(Enum(UserType))
    array_field = Column(ARRAY(Integer))
    json_field = Column(JSON)
    uuid_field = Column(UUID)
    foreign_key_field = Column(Integer, ForeignKey('related_table.id'))
    binary_field = Column(LargeBinary)
